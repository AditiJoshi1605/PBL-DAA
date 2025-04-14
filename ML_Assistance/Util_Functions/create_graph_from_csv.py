import pandas as pd

class Graph:
    def __init__(self):
        self.graph = {}
    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
    def add_edge(self, node1, node2, distance):
        if node1 not in self.graph:
            self.add_node(node1)
        if node2 not in self.graph:
            self.add_node(node2)
        if (node2, distance) not in self.graph[node1]:
            self.graph[node1].append((node2, distance))
        if (node1, distance) not in self.graph[node2]:
            self.graph[node2].append((node1, distance))
    def display_graph(self):
        for node, edges in self.graph.items():
            connected_nodes = []
            for edge in edges:
                connected_node = f"{edge[0]} ({edge[1]})"
                connected_nodes.append(connected_node)
            print(f"{node}->{','.join(connected_nodes)}")
def create_graph_from_csv(file_path):
    # Read csv
    df = pd.read_csv(file_path)
    df['name'] = df['name'].str.strip().str.lower()
    # Graph
    g = Graph()
    # Add nodes and edges to graph
    for i, row in df.iterrows():
        from_location = row['name']
        g.add_node(from_location)
        # Iterate through other columns to add edges
        for to_location in df.columns:
            if to_location != 'name':  # Skip the 'name' column itself
                distance = row[to_location]
                if pd.notnull(distance) and isinstance(distance, (int, float)) and distance > 0:
                    g.add_edge(from_location, to_location, distance)
    return g
