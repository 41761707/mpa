import heapq
from itertools import combinations
import random
import time
import sys
import numpy as np

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = [[] for _ in range(vertices)]

    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

def generate_complete_graph(vertices):
    graph = Graph(vertices)
    for u, v in combinations(range(vertices), 2):
        weight = np.random.normal(10,1)
        graph.add_edge(u, v, weight)
    return graph

def prim(graph):
    start_vertex = 0
    visited = [False] * graph.vertices
    min_heap = [(0, start_vertex, None)]
    mst_edges = []

    while min_heap:
        weight, current_vertex, parent_vertex = heapq.heappop(min_heap)

        if not visited[current_vertex]:
            visited[current_vertex] = True
            if parent_vertex is not None:
                mst_edges.append((parent_vertex, current_vertex, weight))

            for neighbor, neighbor_weight in graph.graph[current_vertex]:
                if not visited[neighbor]:
                    heapq.heappush(min_heap, (neighbor_weight, neighbor, current_vertex))

    return mst_edges

def kruskal(graph):
    edges = []
    for u in range(graph.vertices):
        for v, weight in graph.graph[u]:
            edges.append((weight, u, v))

    edges.sort()

    parent = list(range(graph.vertices))

    def find_set(v):
        if parent[v] != v:
            parent[v] = find_set(parent[v])
        return parent[v]

    def union_sets(u, v):
        root_u = find_set(u)
        root_v = find_set(v)
        if root_u != root_v:
            parent[root_u] = root_v

    mst_edges = []
    for weight, u, v in edges:
        if find_set(u) != find_set(v):
            mst_edges.append((u, v, weight))
            union_sets(u, v)

    return mst_edges

def main():
    lower_bound = int(sys.argv[1])
    upper_bound = int(sys.argv[2])
    step = int(sys.argv[3])
    reps = int(sys.argv[4])

    print("PRIM")
    for i in range(lower_bound, upper_bound + 1, step):
        print(i,": ",end="")
        for j in range(reps):
            graph = generate_complete_graph(i)
            # Algorytm Prima
            start_time = time.time()
            mst_prim = prim(graph)
            end_time = time.time() 
            execution_time = end_time - start_time
            #print(execution_time, "; ",end="")
            print(sum(item[2] for item in mst_prim), "; ",end="")
        print("")
    
    print("\nKRUSKAL")
    for i in range(lower_bound, upper_bound + 1, step):
        print(i,":",end="")
        for j in range(reps):
            graph = generate_complete_graph(i)
            # Algorytm Kruskala
            start_time = time.time()
            mst_kruskal = kruskal(graph)
            end_time = time.time() 
            execution_time = end_time - start_time
            #print(execution_time, ";",end="")
            print(sum(item[2] for item in mst_kruskal), "; ",end="")
        print("")

if __name__ == '__main__':
    main()