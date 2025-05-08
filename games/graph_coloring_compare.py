import time
import matplotlib.pyplot as plt
import networkx as nx
import random


def is_valid_coloring(node, graph, colors, color):
    for neighbor in range(len(graph)):
        if graph[node][neighbor] == 1 and colors[neighbor] == color:
            return False
    return True

def solve_graph_coloring_backtracking(graph, m_colors, colors, node):
    if node == len(graph):
        return True
    for color in range(1, m_colors + 1):
        if is_valid_coloring(node, graph, colors, color):
            colors[node] = color
            if solve_graph_coloring_backtracking(graph, m_colors, colors, node + 1):
                return True
            colors[node] = 0
    return False

def dfs_coloring(graph, m_colors):
    n = len(graph)
    colors = [0] * n
    def dfs(u):
        available = set(range(1, m_colors + 1))
        for v in range(n):
            if graph[u][v] == 1 and colors[v] in available:
                available.remove(colors[v])
        if available:
            colors[u] = min(available)
            for v in range(n):
                if graph[u][v] == 1 and colors[v] == 0:
                    dfs(v)
    for u in range(n):
        if colors[u] == 0:
            dfs(u)
    return colors

def greedy_coloring(graph):
    n = len(graph)
    result = [-1] * n
    result[0] = 0
    for u in range(1, n):
        used_colors = set()
        for v in range(n):
            if graph[u][v] == 1 and result[v] != -1:
                used_colors.add(result[v])
        color = 0
        while color in used_colors:
            color += 1
        result[u] = color
    return result

def generate_random_graph(size, edge_prob=0.3):
    graph = [[0]*size for _ in range(size)]
    for i in range(size):
        for j in range(i+1, size):
            if random.random() < edge_prob:
                graph[i][j] = graph[j][i] = 1
    return graph

sizes = [5, 6, 7, 8, 9, 10]
bt_times, dfs_times, greedy_times = [], [], []

for size in sizes:
    graph = generate_random_graph(size)
    m_colors = 4

    # Backtracking
    colors_bt = [0] * size
    start = time.time()
    solve_graph_coloring_backtracking(graph, m_colors, colors_bt, 0)
    bt_times.append(time.time() - start)

    # DFS
    start = time.time()
    dfs_coloring(graph, m_colors)
    dfs_times.append(time.time() - start)

    # Greedy
    start = time.time()
    greedy_coloring(graph)
    greedy_times.append(time.time() - start)

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(sizes, bt_times, marker='o', label='Backtracking')
plt.plot(sizes, dfs_times, marker='s', label='DFS')
plt.xlabel('Кількість вершин')
plt.ylabel('Час виконання (с)')
plt.title('Backtracking vs DFS (Graph Coloring)')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(sizes, bt_times, marker='o', label='Backtracking')
plt.plot(sizes, greedy_times, marker='^', label='Greedy')
plt.xlabel('Кількість вершин')
plt.ylabel('Час виконання (с)')
plt.title('Backtracking vs Greedy (Graph Coloring)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt
