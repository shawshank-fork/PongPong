import heapq, networkx as nx, matplotlib.pyplot as plt

def ucs(graph, start, goal):
    pq = [(0, start)]
    parent = {start: None}
    cost = {start: 0}

    while pq:
        c, node = heapq.heappop(pq)
        if node == goal:
            return c, build_path(parent, goal)
        for nb, w in graph[node]:
            nc = c + w
            if nb not in cost or nc < cost[nb]:
                cost[nb] = nc
                parent[nb] = node
                heapq.heappush(pq, (nc, nb))
    return None

def build_path(parent, end):
    path = []
    while end:
        path.append(end)
        end = parent[end]
    return path[::-1]

def draw(graph, path=None):
    G = nx.DiGraph()
    for u in graph:
        for v, w in graph[u]:
            G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'weight'))
    if path:
        nx.draw_networkx_edges(G, pos, edgelist=list(zip(path, path[1:])), edge_color='red', width=3)
    plt.show()

# Example graph
graph = {
    'A': [('B',1),('C',4)],
    'B': [('D',1),('E',3)],
    'C': [('F',5)],
    'D': [('G',2)],
    'E': [('G',1)],
    'F': [('G',2)],
    'G': []
}

res = ucs(graph, 'A', 'G')
if res:
    cost, path = res
    print("Path:", " -> ".join(path), "Cost:", cost)
    draw(graph, path)
else:
    print("No path found")
