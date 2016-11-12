$(document).ready(function(){

    /* --- Toggling between views --- */

    // Pre hide all sections
    $('section').hide();

    function displaySection(newSectionDisplay){
        // Toggle section display based on sectionDisplay value
        var sectionId = 'section-' + newSectionDisplay;
        var section = document.getElementById(sectionId);
        $(section).addClass('section--display')
        $(section).show();
    }

    // Display default section information on page load
    displaySection(0);

    // Function to toggle visibleSection
    function toggleSection(newSectionToggle){
        var visibleSection = document.getElementsByClassName('section--display');
        $(visibleSection).hide();
        $(visibleSection).removeClass('section--display');
        displaySection(newSectionToggle);
    }

    // Override nav links with js toggling of CSS visibility
    var navLinks = document.getElementsByClassName('nav-link');
    $(navLinks).click(function(event){
        event.preventDefault();
        var linkId = $(this).attr('id').slice(-1);
        toggleSection(linkId);
    });

    // Reset page with clicking on logo
    var logo = document.getElementsByClassName('logo');
    $(logo).click(function(event){
        event.preventDefault();
        toggleSection(0);
    });

});

