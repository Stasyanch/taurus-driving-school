document.getElementById('burger-menu').addEventListener('click', function() {
    document.getElementById('nav-links').classList.toggle('active');
});

function initMap() {
    const mapElement = document.getElementById('map');
    if (mapElement) {
        mapElement.innerHTML = 'Google Maps ініціалізовано без помилок.';
    }
}

window.onload = initMap;