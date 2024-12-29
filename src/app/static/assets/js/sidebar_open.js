var enterPressed = false;
var ctrlPressed = false;

document.onkeydown = function(e) {
    if (e.which == 17) {
        // Ctrl key is pressed
        ctrlPressed = true;
    } else if (e.which == 70 && ctrlPressed) {
        e.preventDefault();
        // 'F' key is pressed while Ctrl is held down
        if (enterPressed) {
            $('.sidebar:not(#sidebar_form, #lg_sidebar_form)').removeClass('sidebar-open');
            enterPressed = false;
        } else {
            $('.sidebar:not(#sidebar_form, #lg_sidebar_form)').addClass('sidebar-open');
            enterPressed = true;
        }
    }
};

document.onkeyup = function(e) {
    if (e.which == 17) {
        // Ctrl key is released
        ctrlPressed = false;
    }
};

function filter_button(){
    $('.sidebar:not(#sidebar_form,#lg_sidebar_form)').toggleClass('sidebar-open');
}