import heapq
from itertools import combinations
import random
import time
import sys
import numpy as np
from networkx import Graph
import networkx as nx
import matplotlib.pyplot as plt

class PrintGraph(Graph):
    """
    Example subclass of the Graph class.

    Prints activity log to file or standard output.
    """

    def __init__(self, data=None, name="", file=None, **attr):
        super().__init__(data=data, name=name, **attr)
        if file is None:
            import sys

            self.fh = sys.stdout
        else:
            self.fh = open(file, "w")

    def add_node(self, n, attr_dict=None, **attr):
        super().add_node(n, attr_dict=attr_dict, **attr)
        self.fh.write(f"Add node: {n}\n")

    def add_nodes_from(self, nodes, **attr):
        for n in nodes:
            self.add_node(n, **attr)

    def remove_node(self, n):
        super().remove_node(n)
        self.fh.write(f"Remove node: {n}\n")

    def remove_nodes_from(self, nodes):
        for n in nodes:
            self.remove_node(n)

    def add_edge(self, u, v, attr_dict=None, **attr):
        super().add_edge(u, v, attr_dict=attr_dict, **attr)
        self.fh.write(f"Add edge: {u}-{v}\n")

    def add_edges_from(self, ebunch, attr_dict=None, **attr):
        for e in ebunch:
            u, v = e[0:2]
            self.add_edge(u, v, attr_dict=attr_dict, **attr)

    def remove_edge(self, u, v):
        super().remove_edge(u, v)
        self.fh.write(f"Remove edge: {u}-{v}\n")

    def remove_edges_from(self, ebunch):
        for e in ebunch:
            u, v = e[0:2]
            self.remove_edge(u, v)

    def clear(self):
        super().clear()
        self.fh.write("Clear graph\n")

def create_graph_from_dict(graph_dict):
    # Tworzenie pustego grafu nieskierowanego
    G = nx.Graph()

    # Dodawanie wierzchołków do grafu
    G.add_nodes_from(graph_dict.keys())

    # Dodawanie krawędzi do grafu
    for vertex, neighbors in graph_dict.items():
        G.add_edges_from((vertex, neighbor) for neighbor in neighbors)

    return G

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

def generate_neighbourhood(graph):
    n = {}

    for v1, v2, _ in graph:
        if v1 in n:
            n[v1].append((v2))
        else:
            n[v1] = [(v2)]

        if v2 in n:
            n[v2].append((v1))
        else:
            n[v2] = [(v1)]

    return n


def find_tree_height(graph, start_vertex, parent):
    visited = set()

    def dfs(vertex, depth, parent):
        visited.add(vertex)
        visited.add(parent)
        max_depth = depth

        for neighbor in graph[vertex]:
            if neighbor not in visited:
                max_depth = max(max_depth, dfs(neighbor, depth + 1, vertex))

        return max_depth

    return dfs(start_vertex, 0, parent)

'''def propagate_wrapper(mst,n, begin):
    has_info = [begin]
    no_rounds = 0
    print(n[begin])
    path = []
    w_per_v = {}
    while len(has_info) > 0:
        for start in has_info:
            w = []
            for v in n[start]:
                tmp = find_tree_height(n, v, start)
                print(v, ": ", tmp)
                w.append([start, v, tmp])
            sorted_w = sorted(w, key=lambda x: x[2])
            w_per_v[start] = sorted_w
            print(w_per_v)
            round = []
            for key, values in w_per_v.items():
                no_rounds = no_rounds + 1
                if(len(values)) == 0:
                    del w_per_v[key]
                else:
                    current = values.pop()
                    round.append([current[0],current[1]])
                    start = current[1]
            path.append(round)
'''

def propagate(mst, n, start):
    pairs = []
    no_rounds = 0
    nexts = [start]
    heights = {}
    while len(nexts) > 0:
        for v in nexts:
            current_h = []
            nexts.remove(v)
            for y in n[v]:
                if([y, v] not in pairs):
                    pairs.append([v,y])
                    current_h.append((v, y, find_tree_height(n, y, v)+1))
                    nexts.append(y)
            if len(current_h) > 0:
                heights[v] = sorted(current_h, key=lambda x: x[2])
    path = []
    has_info_global = [start]
    while len(has_info_global) > 0:
        has_info = has_info_global[:]
        current_path = []
        no_rounds = no_rounds + 1
        for s in has_info_global:
            current = heights[s].pop()
            current_path.append([s,current[1]])
            if len(heights[s]) == 0:
                    has_info.remove(s)
            for keys in heights:
                if keys == current[1]:
                    has_info.append(current[1])
        heights = {key: value for key, value in heights.items() if value}
        path.append(current_path)
        has_info_global = has_info[:]
    return no_rounds, path
            

    

def main():
    lower_bound = int(sys.argv[1])
    upper_bound = int(sys.argv[2])
    step = int(sys.argv[3])
    reps = int(sys.argv[4])

    #graph = generate_complete_graph(10)
    #mst = kruskal(graph)
    #print(mst)
    #mst = [(5,8,0), (4,5,0), (1,7,0), (5,7,0), (2,7,0), (6,8,0), (1,9,0), (0,9,0), (3,9,0)] - mst do grafu z folderu info
    #n = generate_neighbourhood(mst)
    #no_rounds, path = propagate(mst, n, 5)
    #print(n)
    #for i in range(10):
    #    no_rounds, path = propagate(mst, n, i)
    #    print("Wierzchołek: {}, Liczba rund: {}, droga: {}".format(i,no_rounds, path))

    #rysowanie grafu
    '''
    graph = create_graph_from_dict(n)
    pos = nx.spring_layout(graph)  # Układ wierzchołków
    colored_nodes = [5]
    color_map = ['red' if node in colored_nodes else 'skyblue' for node in graph.nodes]
    nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color=color_map, font_color='black', font_size=10, edge_color='gray')
    plt.savefig('info/start_graph.png')
    plt.clf()
    color_map = []
    mark_as_red = []
    mark_as_green = []
    mark_as_blue = []
    for i in range(len(path)):
        #print("{} runda".format(i+1))
        #print(path[i])
        for element in path[i]:
            if element[1] not in colored_nodes:
                colored_nodes.append(element[1])
        print(colored_nodes)
        pos = nx.spring_layout(graph)  # Układ wierzchołków
        color_map = ['red' if node in colored_nodes else 'skyblue' for node in graph.nodes]
        nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color=color_map, font_color='black', font_size=10, edge_color='gray')
        plt.savefig('info/start_graph_{}.png'.format(i+1))
        plt.clf()
    '''

    #print("PRIM")
    for i in range(lower_bound, upper_bound + 1, step):
        print(i,": ",end="")
        for j in range(reps):
            graph = generate_complete_graph(i)
            # Algorytm Prima
            start_time = time.time()
            mst = prim(graph)
            n = generate_neighbourhood(mst)
            start_time = time.time()
            no_rounds, path = propagate(mst, n, random.randint(0,i-1))
            end_time = time.time() 
            execution_time = end_time - start_time
            print(execution_time, "; ",end="")
            #print(n)
            #print(execution_time, "; ",end="")
        print("")
    
    '''
    
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
    '''

if __name__ == '__main__':
    main()