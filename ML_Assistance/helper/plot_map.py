import folium
import pandas as pd

from helper.load_coordinates import load_coordinates
from helper.create_graph_from_csv import create_graph_from_csv
from helper.calculate_shortest_path import dijkstra

# Load coordinates and graph data
coord_dict, _ = load_coordinates("../assets/location_coordinates_final.csv")
graph_obj = create_graph_from_csv("../assets/distances_log.csv")
graph_dict = {node: dict(graph_obj.graph[node]) for node in graph_obj.graph}

# Define source and destination
start_point, end_point = "clock tower", "isbt dehradun"

# Calculate Dijkstra path and distance
dijkstra_path, _ = dijkstra(graph_dict, start_point, end_point)

# Center map on the starting point or fallback
start_coords = coord_dict.get(dijkstra_path[0], {'Latitude': 30.3165, 'Longitude': 78.0322})

# Initialize map
m = folium.Map(location=[start_coords['Latitude'], start_coords['Longitude']], zoom_start=12)

# Plot path on the map
path_coords = [
    (coord_dict.get(stop, {}).get("Latitude"), coord_dict.get(stop, {}).get("Longitude"))
    for stop in dijkstra_path
    if coord_dict.get(stop)
]

# Draw path line
if path_coords:
    folium.PolyLine(locations=path_coords, color="blue", weight=4, opacity=0.6).add_to(m)

# Add markers with color coding
for i, stop in enumerate(dijkstra_path):
    coords = coord_dict.get(stop)
    if coords:
        color = "green" if i == 0 else "red" if i == len(dijkstra_path) - 1 else "blue"
        folium.Marker(
            [coords['Latitude'], coords['Longitude']], popup=stop, icon=folium.Icon(color=color)
        ).add_to(m)

# Display the map
m
