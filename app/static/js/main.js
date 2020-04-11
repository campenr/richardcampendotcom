window.onload = main();

function main() {
    initCopyright();
}

function initCopyright() {
    document.getElementById('copyright-year').textContent = String(new Date().getFullYear());
}
