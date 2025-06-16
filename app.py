from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import pandas as pd
from ML_Assistance.Util_Functions.load_coordinates import load_coordinates
from ML_Assistance.Util_Functions.knn import nearest
from ML_Assistance.Util_Functions.calculate_shortest_path import dijkstra
from ML_Assistance.Util_Functions.create_graph_from_csv import create_graph_from_csv
from ML_Assistance.Util_Functions.schedule import get_bus_details

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

# @app.route('/api/nearest_stop')
# def api_nearest_stop():
#     from geopy.geocoders import Nominatim
#     from geopy.extra.rate_limiter import RateLimiter
#     from ML_Assistance.Util_Functions.haversine import haversine

#     user_location = request.args.get("location")
#     geolocator = Nominatim(user_agent="bus_locator")
#     geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
#     location = geocode(f"{user_location}, Dehradun, India")
#     if not location:
#         return jsonify({"error": "Location not found"}), 404
    
#     user_lat, user_lon = location.latitude, location.longitude

#     # Find nearest stop using Haversine distance
#     nearest_stop = None
#     min_distance = float("inf")
#     for name, loc in coord_dict.items():
#         dist = haversine(user_lat, user_lon, loc["Latitude"], loc["Longitude"])
#         if dist < min_distance:
#             nearest_stop = name
#             min_distance = dist

#     result = {
#         "stop": nearest_stop,
#         "lat": coord_dict[nearest_stop]["Latitude"],
#         "lng": coord_dict[nearest_stop]["Longitude"],
#         "distance_km": min_distance
#     }
#     return jsonify(result)
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
        "buses": []  # Optional: Fetch from `get_bus_details()` if needed
    }

    return jsonify(result)

# @app.route('/api/running_buses')
# def running_buses():
#     import os
#     BASE_DIR = os.path.dirname(__file__)
#     file_path = os.path.join(BASE_DIR, 'assets', 'bus_schedule.csv')
#     df = pd.read_csv(file_path)
#     running = []
#     for _, row in df.iterrows():
#         running.append({
#             "id": row['Bus_No'],
#             "route": row['Current_Location'] + " → " + row['Next_Stop'],
#             "lat": coord_dict.get(row['Current_Location'].strip().lower(), {}).get("Latitude", 30.3),
#             "lng": coord_dict.get(row['Current_Location'].strip().lower(), {}).get("Longitude", 78.0),
#             "status": "On Route"
#         })
#     return jsonify(running)
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
