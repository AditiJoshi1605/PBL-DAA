import heapq

def dijkstra(graph_obj, start, end):
    graph = graph_obj.graph  # access internal graph dictionary
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0

    queue = [(0, start)]
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break
        
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Reconstruct path
    path = []
    current = end
    while current:
        path.insert(0, current)
        current = previous[current]
    
    if distances[end] == float('inf'):
        return None, None
    
    return path, round(distances[end], 2)
