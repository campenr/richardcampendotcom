$(document).ready(function(){

    function displaySection(newSectionDisplay){
        // Toggle section display based on sectionDisplay value
        var sectionId = 'section-' + newSectionDisplay;
        var section = document.getElementById(sectionId);
        $(section).addClass('section--display')
    }

    // Display default section information on page load
    displaySection(0);

    // Function to toggle visibleSection
    function toggleSection(newSectionToggle){
        var visibleSection = document.getElementsByClassName('section--display');
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
    var navLogo = document.getElementById('nav-logo-link');
    $(navLogo).click(function(event){
        event.preventDefault();
        toggleSection(0);
    });

});

