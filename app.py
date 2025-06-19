from flask import Flask, render_template, request, jsonify,send_file
from flask_socketio import SocketIO, emit
import pandas as pd
from ML_Assistance.Util_Functions.load_coordinates import load_coordinates
from ML_Assistance.Util_Functions.knn import nearest
from ML_Assistance.Util_Functions.calculate_shortest_path import dijkstra
from ML_Assistance.Util_Functions.create_graph_from_csv import create_graph_from_csv
from ML_Assistance.Util_Functions.schedule import get_bus_details
from ML_Assistance.Util_Functions.Multi_Source_Djiktras import multi_source_dijkstra, reconstruct_path
from ML_Assistance.Util_Functions.plot_map import plot_route_map
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
    from ML_Assistance.Main import get_shortest_route 
    source_param = request.args.get("source")
    destination = request.args.get("destination")

    if not source_param or not destination:
        return jsonify({"error": "Missing source or destination"}), 400

    # Handle multiple sources (comma-separated)
    sources = [s.strip().lower() for s in source_param.split(',')]
    destination = destination.strip().lower()

    path, distance, error = get_shortest_route(sources, destination)

    if error:
        return jsonify({"error": error}), 400

    # Convert path to coordinates
    coord_path = []
    for stop in path:
        if stop in coord_dict:
            coord_path.append({
                "name": stop,
                "lat": coord_dict[stop]["Latitude"],
                "lng": coord_dict[stop]["Longitude"]
            })

    # Fetch bus data for stops on this path
    buses = []
    try:
        df = pd.read_csv("assets/bus_schedule.csv")
        for stop in path:
            buses_at_stop = df[df['Current_Stop'].str.lower() == stop.lower()]
            for _, row in buses_at_stop.iterrows():
                buses.append({
                    'id': row['Bus_ID'],
                    'route': row['Route'],
                    'status': row['Status'],
                    'stop': stop
                })
    except Exception as e:
        print(f"Error loading bus data: {e}")

    return jsonify({
        "path": path,
        "coordinates": coord_path,
        "distance_km": round(distance, 2),
        "buses": buses
    })

@app.route('/api/running_buses')
def running_buses():
    try:
        csv_path = os.path.join(os.path.dirname(__file__), 'assets', 'bus_schedule.csv')
        df = pd.read_csv(csv_path)

        buses = []
        for _, row in df.iterrows():
            buses.append({
                'bus_no': row['Bus_No'],
                'time': f"{row['Time']} {row['Arc']}",
                'current_location': row['Current_Location'],
                'next_stop': row['Next_Stop'],
                'driver': row['Driver_Name'],
                'contact': row['Contact_No']
            })

        return jsonify({'buses': buses})
    except Exception as e:
        print("Error loading bus data:", e)
        return jsonify({'error': str(e)}), 500


    

@app.route('/api/emergency_alert', methods=['POST'])
def emergency_alert():
    SocketIO.emit('emergency', {'message': 'Emergency Alert from Admin!'} )
    return jsonify({'status': 'alert_sent'})

if __name__ == "__main__":
    app.run(debug=True)
