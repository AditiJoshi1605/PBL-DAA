import pandas as pd

class Graph :
    def __init__(self):
        self.graph = {}
    def add_node(self,node):
        if node not in self.graph:
            self.graph[node] = []
    def add_edge(self,node1,node2,distance):
        if node1 not in self.graph:
            self.add_node(node1)
        if node2 not in self.graph:
            self.add_node(node2)

            # Add connections in both directions
            self.graph[node1].append((node2,distance))
            self.graph[node2].append((node1,distance))
    
    def display_graph(self):
        for node , edges in self.graph.items():
            connected_nodes = []
            for edge in edges:
                connected_node = f"{edge[0]} ({edge[1]})"
                connected_nodes.append(connected_node)
            print(f"{node}->{','.join(connected_nodes)}")

def create_graph_from_csv(file_path):
    
    # Read csv
    df = pd.read_csv(file_path)
    
