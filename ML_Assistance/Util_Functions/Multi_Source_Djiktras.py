import heapq
def multi_source_dijkstra(graph_obj, sources):
    dist = {node: float('inf') for node in graph_obj.graph}
    prev = {node: None for node in graph_obj.graph}
    pq = []
    for src in sources:
        if src in graph_obj.graph:
            dist[src] = 0
            heapq.heappush(pq, (0, src))
    while pq:
        cost, node = heapq.heappop(pq)
        for neighbor, weight in graph_obj.graph[node]:
            new_cost = cost + weight
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                prev[neighbor] = node
                heapq.heappush(pq, (new_cost, neighbor))
    return dist, prev
#for showing the path we need to reconstruct it
def reconstruct_path(graph_obj, prev, destination):
    path = []
    while destination:
        path.append(destination)
        destination = prev[destination]
    return path[::-1]#returning the backward path