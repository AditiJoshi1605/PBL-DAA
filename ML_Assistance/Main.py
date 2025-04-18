from Util_Functions.create_graph_from_csv import create_graph_from_csv
from Util_Functions.load_coordinates import load_coordinates
from Util_Functions.calculate_shortest_path import dijkstra, get_path_weight
from Util_Functions.stop_to_destination_all_routes import find_all_routes
from Util_Functions.plot_map import plot_route_map
from Util_Functions.Multi_Source_Djiktras import multi_source_dijkstra,reconstruct_path
import os
def display_graph(graph_obj):
    for node, edges in graph_obj.graph.items():
        connected_nodes = []
        for edge in edges:
            connected_node = f"{edge[0]} ({edge[1]})"
            connected_nodes.append(connected_node)
        print(f"{node} -> {', '.join(connected_nodes)}")
def main():
    # Load Data
    base_path = os.path.dirname(__file__)
    graph_file = os.path.join(base_path, '../assets/distances_log.csv')
    coord_file = os.path.join(base_path, '../assets/location_coordinates_final.csv')
    if not os.path.exists(graph_file):
        print(f"Graph file not found at: {graph_file}")
        return
    if not os.path.exists(coord_file):
        print(f"Coordinate file not found at: {coord_file}")
        return
    # Create graph
    graph_obj = create_graph_from_csv(graph_file)
    # Load coordinates
    coord_dict = load_coordinates(coord_file)
    print(f"Available stops in the graph: {list(graph_obj.graph.keys())}")
    # User input
    #start_point = input("Enter pickup point: ").strip().lower()
    end_point = input("Enter drop point: ").strip().lower()
    # Validate input
    #if start_point not in graph_obj.graph:
    #    print(f"Pickup point '{start_point}' not found in graph.")
    #   return
    if end_point not in graph_obj.graph:
        print(f"Drop point '{end_point}' not found in graph.")
        return
    # Shortest path using Dijkstra
    #print("\nShortest path using Dijkstra:")
    #print(dijkstra(graph_obj, start_point, end_point))
    #Updates
    # User input for sources
    sources = input("Enter pickup points (comma-separated): ").strip().lower().split(',')
    sources = [source.strip() for source in sources] # Remove any leading/trailing whitespace from inputs
    # Validate input
    for source in sources:
        if source not in graph_obj.graph:
            print(f"Pickup point '{source}' not found in graph.")
            return
    dis,prev=multi_source_dijkstra(graph_obj,sources)
    path=reconstruct_path(graph_obj,prev,end_point)
    # Print prev (path reconstruction info) and distance to end_point
    print(f"Prev (Previous node information): {prev}")
    print(f"Shortest Distance to '{end_point}': {dis[end_point]}")
    print(f"Path: {path}")
if __name__ == "__main__":
    main()
