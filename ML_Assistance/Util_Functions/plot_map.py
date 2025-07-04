import folium

from ML_Assistance.Util_Functions.load_coordinates import load_coordinates
from ML_Assistance.Util_Functions.create_graph_from_csv import create_graph_from_csv
from ML_Assistance.Util_Functions.calculate_shortest_path import dijkstra

def plot_route_map(coord_dict,graph_obj,start_point,end_point):

    graph_dict = {node: dict(graph_obj.graph[node]) for node in graph_obj.graph}

    # Calculate Dijkstra path and distance
    dijkstra_path, _ = dijkstra(graph_obj, start_point, end_point)

    # Center map on the starting point or fallback
    start_coords = coord_dict.get(dijkstra_path[0], {'Latitude': 30.3165, 'Longitude': 78.0322})

    # Initialize map
    m = folium.Map(location=[start_coords['Latitude'], start_coords['Longitude']], zoom_start=12)

    '''------------------------------------------------Design-----------------------------------------------------'''
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
    return m

def selective_line(coord_dict, graph_obj, names_list):
    m = None
    for i in range(len(names_list) - 1):
        start_location = names_list[i]
        end_location = names_list[i + 1]
        
        # Create a route map from the start location to the current end location
        route_map = plot_route_map(coord_dict, graph_obj, start_location, end_location)
        
        # If it's the first map, initialize m with it, else combine with existing map
        if m is None:
            m = route_map
        else:
            # To combine maps, we'll need to add new markers and lines to the existing map
            for marker in route_map._children.values():
                m.add_child(marker)

    return m