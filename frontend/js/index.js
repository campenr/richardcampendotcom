import 'bootstrap/js/dist/util';
import 'bootstrap/js/dist/collapse';


window.onload = init();

function init() {
    initCopyright();
}

function initCopyright() {
    document.getElementById('copyright-year').textContent = String(new Date().getFullYear());
}
