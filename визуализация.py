import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import math
import time

INF = math.inf

class Edge:
    def __init__(self, to, weight):
        self.to = to
        self.weight = weight

def levit_algorithm(graph, start, visualize=False):
    n = len(graph)
    distances = [INF] * n
    distances[start] = 0
    
    fast_queue = deque()   
    slow_queue = deque()   
    infast = [False] * n 
    inslow = [False] * n   
    
    
    fast_queue.append(start)
    infast[start] = True
    
    if visualize:
        G = nx.DiGraph()
        for i in range(n):
            for edge in graph[i]:
                G.add_edge(i, edge.to, weight=edge.weight)
        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 8))
    
    step = 0
    while fast_queue or slow_queue:
        step += 1
        if visualize:
            plt.clf()
            plt.title(f"Шаг {step}\nАлгоритм Левита")
            
            
            node_colors = []
            for node in G.nodes():
                if infast[node]:
                    node_colors.append('lightcoral') 
                elif inslow[node]:
                    node_colors.append('yellow')      
                elif distances[node] != INF:
                    node_colors.append('lightgreen')  
                else:
                    node_colors.append('lightblue')   
            
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800)
            nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=1)
            nx.draw_networkx_labels(G, pos)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
            
            
            distance_labels = {node: f"d={distances[node]}" if distances[node] != INF else "d=∞" 
                             for node in G.nodes()}
            label_pos = {k: [v[0], v[1]-0.1] for k, v in pos.items()}
            nx.draw_networkx_labels(G, label_pos, labels=distance_labels, font_color='red')
            
            plt.axis('off')
            plt.draw()
            plt.pause(1)
        
        
        current = None
        if fast_queue:
            current = fast_queue.popleft()
            infast[current] = False
        elif slow_queue:
            current = slow_queue.popleft()
            inslow[current] = False
        
        
        for edge in graph[current]:
            if distances[edge.to] > distances[current] + edge.weight:
                distances[edge.to] = distances[current] + edge.weight
                
                if not infast[edge.to]:
                    if inslow[edge.to]:
                        inslow[edge.to] = False
                    fast_queue.append(edge.to)
                    infast[edge.to] = True
    
    if visualize:
        plt.clf()
        plt.title(f"Завершено! Всего шагов: {step}\nКратчайшие расстояния из вершины {start}")
        
        
        node_colors = ['lightgreen' if distances[node] != INF else 'lightblue' for node in G.nodes()]
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=1)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
        
        distance_labels = {node: f"d={distances[node]}" if distances[node] != INF else "d=∞" 
                         for node in G.nodes()}
        label_pos = {k: [v[0], v[1]-0.1] for k, v in pos.items()}
        nx.draw_networkx_labels(G, label_pos, labels=distance_labels, font_color='red')
        
        plt.axis('off')
        plt.show()
    
    return distances


if __name__ == "__main__":
    n = 5
    graph = [[] for _ in range(n)]
    
    graph[0] = [Edge(1, 10), Edge(2, 5)]
    graph[1] = [Edge(2, 2), Edge(3, 1)]
    graph[2] = [Edge(1, 3), Edge(3, 9), Edge(4, 2)]
    graph[3] = [Edge(4, 4)]
    graph[4] = [Edge(3, 6), Edge(0, 7)]
    
    distances = levit_algorithm(graph, 0, visualize=True)
    
    print("\nКратчайшие расстояния:")
    for i in range(n):
        print(f"До вершины {i}: {distances[i] if distances[i] != INF else 'нет пути'}")