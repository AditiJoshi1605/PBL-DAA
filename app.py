from flask import Flask, render_template, request, jsonify,send_file
from flask_socketio import SocketIO, emit
import pandas as pd
from ML_Assistance.Util_Functions.load_coordinates import load_coordinates
from ML_Assistance.Util_Functions.knn import nearest
from ML_Assistance.Util_Functions.calculate_shortest_path import dijkstra
from ML_Assistance.Util_Functions.create_graph_from_csv import create_graph_from_csv
from ML_Assistance.Util_Functions.schedule import get_bus_details
# from ML_Assistance.Util_Functions.plot_map import plot_route_map
from ML_Assistance.Main import get_shortest_route
import io
import os

app = Flask(__name__)

# Load coordinate data once at startup
#coord_dict, coords = load_coordinates("assets/location_coordinates_final.csv")
coord_dict, coords = load_coordinates("C:/Users/Lenovo/Documents/GitHub/PBL-DAA/assets/location_coordinates_final.csv")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/student')
def student_dashboard():
    return render_template("student_dashboard.html")

@app.route('/admin')
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route('/api/nearest_stops')
def api_nearest_stops():
    from ML_Assistance.Util_Functions.knn import nearest
    from ML_Assistance.Util_Functions.load_coordinates import load_coordinates
    import geopy
    from geopy.geocoders import Nominatim
    location = request.args.get('location')
    clean_location = location.strip().lower()
    parts = location.split()
    location = " ".join(parts[:2])
    geolocator = Nominatim(user_agent="bus_finder")
    loc = geolocator.geocode(f"{location}, Dehradun, India")

    if not loc:
        return jsonify({"error": "Location not found"}), 400

    # Load nearest stops
    all_stops = list(coord_dict.keys())

    from ML_Assistance.Util_Functions.haversine import haversine
    stop_distances = []
    for stop in all_stops:
        lat, lon = coord_dict[stop]["Latitude"], coord_dict[stop]["Longitude"]
        distance = haversine(loc.latitude, loc.longitude, lat, lon)
        stop_distances.append((stop, lat, lon, distance))

    stop_distances.sort(key=lambda x: x[3])
    top_stops = stop_distances[:5]  # show 5 nearest

    result = {
        "stops": [
            {"name": s[0], "lat": s[1], "lng": s[2], "distance_km": s[3]}
            for s in top_stops
        ],
        "buses": []  # to be done: Fetch from `get_bus_details()` if needed
    }

    return jsonify(result)


@app.route("/api/route")
def api_route():
    source = request.args.get("source")
    destination = request.args.get("destination")

    if not source or not destination:
        return jsonify({"error": "Missing source or destination"}), 400

    path, distance, error = get_shortest_route(source, destination)

    if error:
        return jsonify({"error": error}), 400

    # Convert path to coordinates
    coord_path = [
        {
            "name": stop,
            "lat": coord_dict[stop]["Latitude"],
            "lng": coord_dict[stop]["Longitude"]
        }
        for stop in path if stop in coord_dict
    ]

    return jsonify({
        "path": path,
        "coordinates": coord_path,
        "distance_km": round(distance, 2)
    })


@app.route("/render_map")
def render_map():
    source = request.args.get("source")
    destination = request.args.get("destination")

    if not source or not destination:
        return "Missing source or destination", 400

    source = source.strip().lower()
    destination = destination.strip().lower()

    # Build graph object from distance log
    graph = create_graph_from_csv("assets/distances_log.csv")

    # Generate Folium map
    folium_map = plot_route_map(coord_dict, graph, source, destination)

    # Export Folium map to HTML
    map_html = folium_map._repr_html_()

    return map_html

@app.route('/api/running_buses')
def running_buses():
    try:
        df = pd.read_csv("assets/bus_schedule.csv")
        running = df[df['Status'].str.lower() == 'running']
        buses = []
        for _, row in running.iterrows():
            buses.append({
                'id': row['Bus_ID'],
                'route': row['Route'],
                'lat': row['Latitude'],
                'lng': row['Longitude'],
                'status': row['Status']
            })
        return jsonify({'buses': buses})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/emergency_alert', methods=['POST'])
def emergency_alert():
    SocketIO.emit('emergency', {'message': 'Emergency Alert from Admin!'} )
    return jsonify({'status': 'alert_sent'})

if __name__ == "__main__":
    app.run(debug=True)
