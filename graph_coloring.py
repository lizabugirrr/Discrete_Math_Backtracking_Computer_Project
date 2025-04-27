import matplotlib.pyplot as plt
import networkx as nx

def possible_coloring(node, graph, colors, color):
    for neighbor in range(len(graph)):
        if graph[node][neighbor] == 1 and colors[neighbor] == color:
            return False
    return True

def visualize_graph(graph, colors, title="Graph Coloring", pos=None, first_draw=False, success=True):
    if first_draw:
        plt.ion()
        plt.figure(figsize=(8, 6))

    plt.clf()

    G = nx.Graph()
    n = len(graph)

    for i in range(n):
        G.add_node(i)

    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                G.add_edge(i, j)

    color_map = []
    for color in colors:
        if color == 0:
            color_map.append('gray')
        else:
            color_list = ['teal', 'lightgreen', 'lightblue', 'pink', 'red', 'orange']
            color_map.append(color_list[(color - 1) % len(color_list)])

    if pos is None:
        pos = nx.spring_layout(G)

    nx.draw(G, pos, node_color=color_map, with_labels=True, node_size=700, font_size=12)
    plt.title(title)
    plt.pause(0.5)

    return pos

def solve_graph_coloring(graph, m_colors, colors, node, visualize=False, pos=None, first_draw=True):
    if node == len(graph):
        return True

    for color in range(1, m_colors + 1):
        if possible_coloring(node, graph, colors, color):
            colors[node] = color

            if visualize:
                if first_draw:
                    pos = visualize_graph(graph, colors, title=f"Вершина {node} = колір {color}", pos=None, first_draw=True, success=True)
                else:
                    visualize_graph(graph, colors, title=f"Вершина {node} = колір {color}", pos=pos, success=True)

            if solve_graph_coloring(graph, m_colors, colors, node + 1, visualize, pos, False):
                return True

            colors[node] = 0
            if visualize:
                visualize_graph(graph, colors, title=f"Откат з вершини {node}", pos=pos, success=False)

    return False

def graph_coloring(graph, m_colors, visualize=False):
    n = len(graph)
    colors = [0] * n

    if not solve_graph_coloring(graph, m_colors, colors, 0, visualize):
        print("Немає рішення")
        return None

    print("\nРозфарбування вершин:")
    for i in range(n):
        print(f"Вершина {i}: Колір {colors[i]}")
    return colors

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

result = graph_coloring(graph, m_colors, visualize=True)
