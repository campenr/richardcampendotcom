$(document).ready(function(){

    /* --- Toggle between different sections while giving the appearance
            of normal website navigation. --- */

    // Pre-hide all sections
    $('.section-toggleable').hide();

    // Change header to a nav-link to override default behaviour
    var headerLink = document.getElementsByClassName('header-logo');
    $(headerLink).addClass('nav-link');
    $(headerLink).attr('id', 'nav-link-0');

    function displaySection(n){
        // Toggle section display based on sectionDisplay value
        var sectionNumber = 'section-' + n;
        var section = document.getElementsByClassName(sectionNumber);
        $(section).addClass('section-display')
        $(section).show();
    }

    // Display correct information on page load
    var path = window.location.pathname;
    switch(path) {
        case('/'):
            displaySection(0)
            break
        case('/publications'):
            displaySection(1);
            break
        case('/software'):
            displaySection(2);
            break
    }

    // Function to toggle visibleSection
    function toggleSection(n){
        var visibleSection = document.getElementsByClassName('section-display');
        $(visibleSection).hide();
        $(visibleSection).removeClass('section-display');
        displaySection(n);
    }

    // Amend URL history
    function setUrl(sectionId) {
        history.pushState('', '', sectionId);
    }

    // Change content and URL path on link clicks.
    var navLinks = document.getElementsByClassName('nav-link');
    $(navLinks).click(function(event){
        event.preventDefault();
        var linkId = $(this).attr('id').slice(-1);
        switch(linkId) {
            case('0'):
                setUrl('/');
                break
            case('1'):
                setUrl('publications');
                break
            case('2'):
                setUrl('software');
                break
        }
        toggleSection(linkId);
    });

});     // end document.ready()
