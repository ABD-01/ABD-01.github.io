// Reference repo   : https://github.com/cs50/jekyll-theme-cs50 filename: jekyll-theme-cs50.js

$(document).on('DOMContentLoaded', function () {
    $('[data-marker]').each(function (index, element) {

        // Add .fa-ul to parent ul
        $(element).parent().addClass('fa-ul');

        // Filter
        const filter = function () {
            return !$(this).is('ol, ul');
        };

        // Listener
        const click = function (eventObject) {

            // If it wasn't a descendent link that was clicked
            if (!$(eventObject.target).is('a')) {

                // Don't propgate to nested lists
                eventObject.stopPropagation();

                // Toggle marker
                const marker = $(element).attr('data-marker');
                if (marker === '+') {
                    $(element).attr('data-marker', '-');
                    $(element).find('> .fa-li > .fa-plus-square').removeClass('fa-plus-square').addClass('fa-minus-square');
                }
                else if (marker === '-') {
                    $(element).attr('data-marker', '+');
                    $(element).find('> .fa-li > .fa-minus-square').removeClass('fa-minus-square').addClass('fa-plus-square');
                }
                $(window).trigger('resize');
            }
        };

        // Icons
        const plus = $('<span class="fa-li"><i class="far fa-plus-square"></i></span>').click(click);
        const minus = $('<span class="fa-li"><i class="far fa-minus-square"></i></span>').click(click);
        const square = $('<span class="fa-li"><i class="fas fa-square"></i></span>');

        // Wrapper
        const $span = $('<span>').click(click);

        // If +
        if ($(element).attr('data-marker') === '+') {
            $(element).contents().filter(filter).wrap($span);
            $(element).prepend(plus);
        }

        // If -
        else if ($(element).attr('data-marker') === '-') {
            $(element).contents().filter(filter).wrap($span);
            $(element).prepend(minus);
        }

        // If *
        else if ($(element).attr('data-marker') === '*') {
            $(element).prepend(square);
        }
    });
});