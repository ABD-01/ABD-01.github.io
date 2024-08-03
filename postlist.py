from math import log
import re
from turtle import pos
from numpy import tile
from sphinx.util.nodes import explicit_title_re
from sphinx.util.matching import Matcher, patfilter
from sphinx.util import docname_join, logging, url_re
from sphinx.locale import _, __

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective
from docutils.nodes import Element, Node
from sphinx import addnodes
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util import logging
from docutils.parsers.rst import directives
from sphinx.domains.std import StandardDomain

logger = logging.getLogger(__name__)

class Postlist(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        posts_list = nodes.bullet_list()
        env = self.env

        for post in self.content:
            try:
                doc = frozenset(StandardDomain._virtual_doc_names)
                metadata = env.metadata[post]
                logger.error("Post: %s", type(post))

                _list_item = nodes.list_item()
                list_item = nodes.paragraph()
                _list_item += list_item
                
                # Title
                title = nodes.title(level = 3)
                title += nodes.paragraph(text="Hello World")
                # title += nodes.refersence('', post, internal=True, refuri=post+".html")
                # title += nodes.strong(text=doc.traverse(nodes.title)[0].astext())
                _list_item += title

                # Tags
                if 'tags' in metadata:
                    tags = nodes.paragraph()
                    tags += nodes.strong(text="Tags: ")
                    tags += nodes.inline(text=metadata['tags'])
                    list_item += tags

                # Category
                if 'category' in metadata:
                    category = nodes.paragraph()
                    category += nodes.strong(text="Category: ")
                    category += nodes.inline(text=metadata['category'])
                    list_item += category

                # Date
                if 'date' in metadata:
                    date = nodes.paragraph()
                    date += nodes.strong(text="Date: ")
                    date += nodes.inline(text=metadata['date'])
                    list_item += date

                # Excerpt
                if 'excerpt' in metadata:
                    excerpt = nodes.paragraph()
                    excerpt += nodes.inline(text=metadata['excerpt'])
                    list_item += excerpt

                # Read more link
                read_more = nodes.paragraph()
                ref = nodes.reference('', 'Read more', internal=True, refuri=post)
                read_more += ref
                list_item += read_more

                posts_list += list_item

            except Exception as e:
                logger.warning(f"Error processing post {post}: {str(e)}")

        return [posts_list]

def int_or_nothing(argument: str) -> int:
    if not argument:
        return 999
    return int(argument)

glob_re = re.compile(r'.*[*?\[].*')


class DummyPostlist(SphinxDirective):
    """
    Directive to notify Sphinx about the hierarchical structure of the docs,
    and to include a table-of-contents like tree in the current document.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'maxdepth': int,
        'name': directives.unchanged,
        'class': directives.class_option,
        'caption': directives.unchanged_required,
        'glob': directives.flag,
        'hidden': directives.flag,
        'includehidden': directives.flag,
        'numbered': int_or_nothing,
        'titlesonly': directives.flag,
        'reversed': directives.flag,
    }

    def run(self) -> list[Node]:
        subnode = addnodes.toctree()
        subnode['parent'] = self.env.docname

        # (title, ref) pairs, where ref may be a document, or an external link,
        # and title may be None if the document's title is to be used
        subnode['entries'] = []
        subnode['includefiles'] = []
        subnode['maxdepth'] = self.options.get('maxdepth', -1)
        subnode['caption'] = self.options.get('caption')
        subnode['glob'] = 'glob' in self.options
        subnode['hidden'] = 'hidden' in self.options
        subnode['includehidden'] = 'includehidden' in self.options
        subnode['numbered'] = self.options.get('numbered', 0)
        subnode['titlesonly'] = 'titlesonly' in self.options
        self.set_source_info(subnode)
        wrappernode = nodes.compound(
            classes=['toctree-wrapper', *self.options.get('class', ())],
        )
        wrappernode.append(subnode)
        self.add_name(wrappernode)

        ret = self.parse_content(subnode)
        ret.append(wrappernode)
        return ret

    def parse_content(self, toctree: addnodes.toctree) -> list[Node]:
        generated_docnames = frozenset(StandardDomain._virtual_doc_names)
        suffixes = self.config.source_suffix
        current_docname = self.env.docname
        glob = toctree['glob']

        # glob target documents
        all_docnames = self.env.found_docs.copy() | generated_docnames
        all_docnames.remove(current_docname)  # remove current document
        frozen_all_docnames = frozenset(all_docnames)

        ret: list[Node] = []
        excluded = Matcher(self.config.exclude_patterns)
        for entry in self.content:
            logger.error(entry)
            logger.error(ret)
            if not entry:
                continue

            # look for explicit titles ("Some Title <document>")
            explicit = explicit_title_re.match(entry)
            url_match = url_re.match(entry) is not None
            if glob and glob_re.match(entry) and not explicit and not url_match:
                pat_name = docname_join(current_docname, entry)
                doc_names = sorted(patfilter(all_docnames, pat_name))
                for docname in doc_names:
                    if docname in generated_docnames:
                        # don't include generated documents in globs
                        continue
                    all_docnames.remove(docname)  # don't include it again
                    toctree['entries'].append((None, docname))
                    toctree['includefiles'].append(docname)
                if not doc_names:
                    logger.warning(__("toctree glob pattern %r didn't match any documents"),
                                   entry, location=toctree)
                continue

            if explicit:
                ref = explicit.group(2)
                title = explicit.group(1)
                docname = ref
            else:
                ref = docname = entry
                title = None
            logger.error(f"Title: {title}, Ref: {ref}")

            # remove suffixes (backwards compatibility)
            for suffix in suffixes:
                if docname.endswith(suffix):
                    docname = docname.removesuffix(suffix)
                    break

            # absolutise filenames
            docname = docname_join(current_docname, docname)
            if url_match or ref == 'self':
                toctree['entries'].append((title, ref))
                continue

            if docname not in all_docnames:
                if excluded(self.env.doc2path(docname, False)):
                    message = __('toctree contains reference to excluded document %r')
                    subtype = 'excluded'
                else:
                    message = __('toctree contains reference to nonexisting document %r')
                    subtype = 'not_readable'

                logger.warning(message, docname, type='toc', subtype=subtype,
                               location=toctree)
                self.env.note_reread()
                continue

            if docname in all_docnames:
                all_docnames.remove(docname)
            else:
                logger.warning(__('duplicated entry found in toctree: %s'), docname,
                               location=toctree)

            toctree['entries'].append((title, docname))
            toctree['includefiles'].append(docname)

        # entries contains all entries (self references, external links etc.)
        if 'reversed' in self.options:
            toctree['entries'] = list(reversed(toctree['entries']))
            toctree['includefiles'] = list(reversed(toctree['includefiles']))

        return ret