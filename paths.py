

def dfs(graph,visited,key,path,paths):

    singlePath = tuple(path)
    paths.append(singlePath)

    visited.add(key)
    for nxt in list(graph[key]):

        if nxt in visited:
            continue
        path.append(nxt)

        dfs(graph,visited,nxt,path,paths)
        path.pop()

def GetAllPaths(graph):
    paths = []

    for key in graph.keys():
        path = [key]
        visited = set()
        dfs(graph,visited,key,path,paths)
    
    return paths