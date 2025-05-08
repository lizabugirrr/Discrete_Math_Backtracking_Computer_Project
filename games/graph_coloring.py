import argparse
import matplotlib.pyplot as plt
import networkx as nx
import sys
import pygame
from colorama import init, Fore, Back, Style

init(autoreset=True)

# Sample graph
graph = [
    [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1],
    [0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0]
]

m_colors = 4

def print_console_graph(graph, colors):
    print("\nGraph Coloring:")
    for i, color_index in enumerate(colors):
        color_name = ["Gray", "Teal", "Green", "Blue", "Pink", "Red", "Orange"][color_index]
        print(f"Vertex {i}: {color_name}")

def visualize_graph(graph, colors, title="Graph Coloring", pos=None, first_draw=False):
    if first_draw:
        plt.ion()
        plt.figure(figsize=(8, 6))

    plt.clf()
    G = nx.Graph()

    for i in range(len(graph)):
        G.add_node(i)

    for i, neighbors in enumerate(graph):
        for j in range(i + 1, len(neighbors)):
            if neighbors[j] == 1:
                G.add_edge(i, j)

    color_map = []
    color_list = ['gray', 'teal', 'lightgreen', 'lightblue', 'pink', 'red', 'orange']
    for color in colors:
        color_map.append(color_list[color % len(color_list)])

    if pos is None:
        pos = nx.spring_layout(G)

    nx.draw(G, pos, node_color=color_map, with_labels=True, node_size=700, font_size=12)
    plt.title(title)
    plt.pause(0.5)

    return pos

def is_valid_coloring(node, graph, colors, color):
    for neighbor in range(len(graph)):
        if graph[node][neighbor] == 1 and colors[neighbor] == color:
            return False
    return True

def solve_graph_coloring_console(graph, m_colors, colors, node):
    if node == len(graph):
        return True

    for color in range(1, m_colors + 1):
        if is_valid_coloring(node, graph, colors, color):
            colors[node] = color
            print_console_graph(graph, colors)

            if solve_graph_coloring_console(graph, m_colors, colors, node + 1):
                return True
            colors[node] = 0
            print_console_graph(graph, colors)

    return False

def solve_graph_coloring_pygame(graph, m_colors, colors, node, pos=None, first_draw=True):
    if node == len(graph):
        return True

    for color in range(1, m_colors + 1):
        if is_valid_coloring(node, graph, colors, color):
            colors[node] = color

            if first_draw:
                pos = visualize_graph(graph, colors, f"Vertex {node} = Color {color}", None, True)
            else:
                visualize_graph(graph, colors, f"Vertex {node} = Color {color}", pos)

            if solve_graph_coloring_pygame(graph, m_colors, colors, node + 1, pos, False):
                return True

            colors[node] = 0
            visualize_graph(graph, colors, f"Backtrack from vertex {node}", pos)

    return False


def run_console_version():
    colors = [0] * len(graph)
    print("Solving Graph Coloring Problem...")

    if solve_graph_coloring_console(graph, m_colors, colors, 0):
        print("\nFinal Coloring:")
        print_console_graph(graph, colors)
    else:
        print("No valid coloring exists with the given number of colors.")

def run_pygame_version():
    colors = [0] * len(graph)
    print("Solving Graph Coloring Problem (Visual)...")

    if solve_graph_coloring_pygame(graph, m_colors, colors, 0):
        print("\nFinal Coloring:")
        print_console_graph(graph, colors)
    else:
        print("No valid coloring exists with the given number of colors.")

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Graph Coloring Solver')
    parser.add_argument('mode', choices=['console', 'visual'], help='Display mode')
    args = parser.parse_args()

    if args.mode == 'console':
        run_console_version()
    else:
        run_pygame_version()
