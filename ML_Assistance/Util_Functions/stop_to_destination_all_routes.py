def find_all_routes(graph_obj, start, destination):
    def dfs(curr, visited, path, all_paths):
        visited.add(curr)
        path.append(curr)
        if curr == destination:
            all_paths.append(path.copy())
        else:
            for neighbour, _ in graph_obj.graph.get(curr, []):
                if neighbour not in visited:
                    dfs(neighbour, visited, path, all_paths)
        path.pop()
        visited.remove(curr)
    all_paths = []
    dfs(start, set(), [], all_paths)
    return all_paths