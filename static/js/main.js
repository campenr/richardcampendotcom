// $(document).ready(function(){
//
//     /* --- Sticky Navigation Bar --- */
//
//     function stickNav() {
//         var headerHeight = 115; // in pixels
//         if ($(this).scrollTop() > headerHeight) {
//             $('.nav').addClass('fixed-header');
//             $('.nav-buffer').show();
//         } else {
//             $('.nav').removeClass('fixed-header');
//             $('.nav-buffer').hide();
//         }
//     }
//
//     $(function () {
//         $(window).scroll(stickNav);
//         stickNav();
//     });


    /*<script type="text/javascript">if (typeof jQuery != 'undefined'){jQuery(document).ready(function($){var filetypes = /\.(zip|exe|dmg|pdf|doc.*|xls.*|ppt.*|mp3|txt|rar|wma|mov|avi|wmv|flv|wav)$/i;var baseHref = '';if (jQuery('base').attr('href') != undefined) baseHref = jQuery('base').attr('href');jQuery('a').on('click', function(event) {var el = jQuery(this);var track = true;var href = (typeof(el.attr('href')) != 'undefined' ) ? el.attr('href') :"";var isThisDomain = href.match(document.domain.split('.').reverse()[1] + '.' + document.domain.split('.').reverse()[0]);if (!href.match(/^javascript:/i)) {var elEv = []; elEv.value=0, elEv.non_i=false;if (href.match(/^mailto\:/i)) {elEv.category = "email";elEv.action = "click";elEv.label = href.replace(/^mailto\:/i, '');elEv.loc = href;}else if (href.match(filetypes)) {var extension = (/[.]/.exec(href)) ? /[^.]+$/.exec(href) : undefined;elEv.category = "download";elEv.action = "click-" + extension[0];elEv.label = href.replace(/ /g,"-");elEv.loc = baseHref + href;}else if (href.match(/^https?\:/i) && !isThisDomain) {elEv.category = "external";elEv.action = "click";elEv.label = href.replace(/^https?\:\/\//i, '');elEv.non_i = true;elEv.loc = href;}else if (href.match(/^tel\:/i)) {elEv.category = "telephone";elEv.action = "click";elEv.label = href.replace(/^tel\:/i, '');elEv.loc = href;}else track = false;if (track) {_gaq.push(['_trackEvent', elEv.category.toLowerCase(), elEv.action.toLowerCase(), elEv.label.toLowerCase(), elEv.value, elEv.non_i]);if ( el.attr('target') == undefined || el.attr('target').toLowerCase() != '_blank') {setTimeout(function() { location.href = elEv.loc; }, 400);return false;}}}});});}</script>*/
    /*<script type="text/javascript">var _gaq = _gaq || []; _gaq.push(['_setAccount', 'UA-67087023-1']);_gaq.push(['_trackPageview']);(function(){var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);})();</script>*/


    /* --- Toggling between views --- */

    // // Pre hide all sections
    // $('section').hide();
    //
    // function displaySection(newSectionDisplay){
    //     // Toggle section display based on sectionDisplay value
    //     var sectionId = 'section-' + newSectionDisplay;
    //     var section = document.getElementById(sectionId);
    //     $(section).addClass('section--display')
    //     $(section).show();
    // }

    // // Display default section information on page load
    // displaySection(0);
    //
    // // Function to toggle visibleSection
    // function toggleSection(newSectionToggle){
    //     var visibleSection = document.getElementsByClassName('section--display');
    //     $(visibleSection).hide();
    //     $(visibleSection).removeClass('section--display');
    //     displaySection(newSectionToggle);
    // }
    //
    // // Override nav links with js toggling of CSS visibility
    // var navLinks = document.getElementsByClassName('nav-link');
    // $(navLinks).click(function(event){
    //     event.preventDefault();
    //     var linkId = $(this).attr('id').slice(-1);
    //     toggleSection(linkId);
    // });
    //
    // // Reset page with clicking on logo
    // var logo = document.getElementsByClassName('logo');
    // $(logo).click(function(event){
    //     event.preventDefault();
    //     toggleSection(0);
    // });

// });
