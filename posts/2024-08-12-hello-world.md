---
myst:
    html_meta:
        "property=og:title": "Hello World"
        "language": "en"
---
```{post} Aug 12, 2024
---
author: me
title: Hello World
language: English
exclude:
---

Hi!! I have made a website and if you are seeing this, it is live

```

{.hiddenh1}
# Hello World

## Hello World! 🎉

This is my new website. It is built using [Sphinx](https://www.sphinx-doc.org/) and [MyST - Markedly Structured Text](https://myst-parser.readthedocs.io/en/latest/index.html). The theme you are seeing is a custom blend of [CS50](https://cs50.harvard.edu/college/) and [Furo](https://pradyunsg.me/furo/). 

I'm also using [Ablog](https://ablog.readthedocs.io/en/stable/index.html) with some tweak (because it [does not work with furo](https://github.com/sunpy/ablog/issues/108)) for my blog posts. 

You can visit the older versions <a href="/index_barron.html" target="_blank">(April 2023)</a> and <a href="/index_bedimcode.html" target="_blank">(Nov 2021)</a>.

The source code for this site lives at [github.com/ABD-01/abd-01.github.io](https://github.com/ABD-01/abd-01.github.io). Feel free to check it out if you're curious about the inner workings.


## Seeing if things are working

### Code Highlighting

`````{tab-set}

````{tab-item} C

```{code-block} c
:linenos:

int main() {
    printf("Hello World\n");
}

```

````

````{tab-item} Python

```{code-block} python

print("Hello World")

```

````

````{tab-item} Rust
```{code-block} rust
fn main() {
    println!("Hello World");
}
````

`````

### $\LaTeX$, coz why not?

Mass-energy equivalence: $E = mc^2$.


The Cauchy–Schwarz inequality:

$$
\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)
$$

### Nice List

<ul class="fa-ul">
  <li data-marker="-">Fruits
    <ul class="fa-ul">
      <li data-marker="+">Citrus Fruits
        <ul>
          <li data-marker="*">Oranges</li>
          <li data-marker="*">Lemons</li>
          <li data-marker="*">Limes</li>
        </ul>
      </li>
      <li data-marker="-">Berries
        <ul  class="fa-ul">
          <li data-marker="*">Strawberries</li>
          <li data-marker="*">Blueberries</li>
          <li data-marker="*">Raspberries</li>
        </ul>
      </li>
    </ul>
  </li>
  <li data-marker="+">Vegetables
    <ul class="fa-ul">
      <li data-marker="-">Leafy Greens
        <ul>
          <li data-marker="*">Lettuce</li>
          <li data-marker="*">Spinach</li>
          <li data-marker="*">Kale</li>
        </ul>
      </li>
      <li data-marker="+">Root Vegetables
        <ul class="fa-ul">
          <li data-marker="*">Carrots</li>
          <li data-marker="*">Beets</li>
          <li data-marker="*">Potatoes</li>
        </ul>
      </li>
    </ul>
  </li>
</ul>
