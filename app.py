# from flask import Flask, render_template, request, jsonify
# from flask_socketio import SocketIO

# app = Flask(__name__)
# socketio = SocketIO(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/student')
# def student_dashboard():
#     return render_template('student_dashboard.html')

# @app.route('/admin')
# def admin_dashboard():
#     return render_template('admin_dashboard.html')

# # Mock API: Return route info (not complete)
# @app.route('/api/routes', methods=['GET'])
# def get_routes():
#     return jsonify([
#         {"data  variables"},
#         {"data variables"}
#     ])

# if __name__ == '__main__':
#     socketio.run(app, debug=True)
from flask import Flask, render_template, request, jsonify
from ML_Assistance.Util_Functions.knn import nearest
from ML_Assistance.Util_Functions.load_coordinates import load_coordinates
from ML_Assistance.Util_Functions.schedule import get_bus_details
import pandas as pd

app = Flask(__name__)

# Load coordinate data once at startup
# coord_dict, coords = load_coordinates("assets/location_coordinates_final.csv")
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

@app.route('/api/nearest_stop')
def api_nearest_stop():
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
    from ML_Assistance.Util_Functions.haversine import haversine

    user_location = request.args.get("location")
    geolocator = Nominatim(user_agent="bus_locator")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    location = geocode(f"{user_location}, Dehradun, India")
    if not location:
        return jsonify({"error": "Location not found"}), 404
    
    user_lat, user_lon = location.latitude, location.longitude

    # Find nearest stop using Haversine distance
    nearest_stop = None
    min_distance = float("inf")
    for name, loc in coord_dict.items():
        dist = haversine(user_lat, user_lon, loc["Latitude"], loc["Longitude"])
        if dist < min_distance:
            nearest_stop = name
            min_distance = dist

    result = {
        "stop": nearest_stop,
        "lat": coord_dict[nearest_stop]["Latitude"],
        "lng": coord_dict[nearest_stop]["Longitude"],
        "distance_km": min_distance
    }
    return jsonify(result)

@app.route('/api/running_buses')
def running_buses():
    import os
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'assets', 'bus_schedule.csv')
    df = pd.read_csv(file_path)
    running = []
    for _, row in df.iterrows():
        running.append({
            "id": row['Bus_No'],
            "route": row['Current_Location'] + " → " + row['Next_Stop'],
            "lat": coord_dict.get(row['Current_Location'].strip().lower(), {}).get("Latitude", 30.3),
            "lng": coord_dict.get(row['Current_Location'].strip().lower(), {}).get("Longitude", 78.0),
            "status": "On Route"
        })
    return jsonify(running)

if __name__ == "__main__":
    app.run(debug=True)
