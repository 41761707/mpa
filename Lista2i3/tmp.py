from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

def dfs_order(graph, root, visited, order):
    visited[root] = True

    for neighbor in graph[root]:
        if not visited[neighbor]:
            dfs_order(graph, neighbor, visited, order)

    order.append(root)

def inform_order(graph, root):
    visited = [False] * graph.vertices
    order = []

    dfs_order(graph.graph, root, visited, order)

    round_number = 1
    inform_order_by_round = {}

    for i in range(graph.vertices - 1, -1, -1):
        vertex = order[i]
        children = [child for child in graph.graph[vertex] if visited[child]]
        inform_order_by_round[vertex] = (round_number, children)
        round_number += 1

    return inform_order_by_round


# Przykład użycia
if __name__ == "__main__":
    #mst = [(5,8,0), (4,5,0), (1,7,0), (5,7,0), (2,7,0), (6,8,0), (1,9,0), (0,9,0), (3,9,0)]
    g = Graph(10)
    g.add_edge(5, 8)
    g.add_edge(4, 5)
    g.add_edge(1, 7)
    g.add_edge(5, 7)
    g.add_edge(2, 7)
    g.add_edge(6, 8)
    g.add_edge(1, 9)
    g.add_edge(0, 9)
    g.add_edge(3, 9)

    root = 5
    order_by_round = inform_order(g, root)

    print("Kolejność informowania dzieci dla każdego wierzchołka:")
    for vertex, (round_number, children) in order_by_round.items():
        print(f"Wierzchołek {vertex} (Runda {round_number}): {children}")