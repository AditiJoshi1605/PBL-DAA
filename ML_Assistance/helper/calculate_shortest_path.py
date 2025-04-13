'''
Graph Representation: Uses a dictionary to represent the graph. In the dictionary version, each key is a node, and its corresponding value is another dictionary where keys are neighboring nodes and values are edge weights.
    Parameters:
    graph (dict): {Node: {Neighbor: shortest_distance}}
    origin (any): Starting point node
    destination (any): Target node

        Returns:
        tuple: (path list, total cost) or (None, None) if no path exists

'''
import sys
import heapq

def calculate_shortest_path(graph,start,end):
    
    # Used Dijkstra's

    if not graph:
        return None , None
    
    # Early exit for identical start/end
    if start == end:
        return [start] , 0
    
    # Initialize tracking structures

    # Creates a dictionary where every node starts with "infinite" distance
    shortest_distance = {}
    for node in graph:
        shortest_distance[node] = float('inf')
    '''
    Dictionary created -
    graph = {'A': {}, 'B': {}, 'C': {}}
    {'A': inf, 'B': inf, 'C': inf}
    
    '''
    previous_node = {}
    for node in graph:
        previous_node[node] = None  # No previous node yet
    '''
    Dictionary created -
    Output: {'A': None, 'B': None, 'C': None}
    
    '''
     
    priority_queue = [(0,start)] # Start with (distance=0, node=start)

    # Set starting point
    shortest_distance[start] = 0
    heapq.heappush(priority_queue,(0,start))

    
    while priority_queue:

        current_distance , current_node = heapq.heappop(priority_queue)

        if current_distance > shortest_distance[current_distance]:
            continue

        # Found our target! Build the path
        if current_distance == end:
            path = []
            temp = end

            # Backtrack using previous_node
            while temp is not None:
                path.append(temp)
                temp = previous_node[temp]
                
            return path[::-1] , current_distance # Reverse to get start->end order
        
        # Check Neghbours
        for neighbour , weight in graph[current_node].items():
            new_distance = current_distance + weight

            if new_distance < shortest_distance[neighbour]:
                shortest_distance[neighbour]  = new_distance
                previous_node[neighbour] = current_node
                heapq.heappush(priority_queue,(new_distance,neighbour))
    
    return None , None
