let map = L.map('map').setView([30.3165, 78.0322], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data © OpenStreetMap contributors'
}).addTo(map);

// Sample marker (this would be replaced by real mobile GPS updates)
L.marker([30.3165, 78.0322]).addTo(map)
    .bindPopup('Bus 1 Current Location')
    .openPopup();
