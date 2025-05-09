import time

import heapq



DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]



def print_path(grid, path):

    result = [row[:] for row in grid]

    for r, c in path:

        if result[r][c] == '-':

            result[r][c] = '*'

    for row in result:

        print(' '.join(row))

    print()



def is_valid(grid, row, col, visited):

    return (0 <= row < len(grid) and 0 <= col < len(grid[0]) and

            grid[row][col] in ('-', 'B') and (row, col) not in visited)



def heuristic(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])



def find_point(grid, symbol):

    for r in range(len(grid)):

        for c in range(len(grid[0])):

            if grid[r][c] == symbol:

                return (r, c)

    return None



# 1. Backtracking

def backtracking(grid, start, end):

    path = []

    visited = set()



    def dfs(r, c):

        if (r, c) == end:

            path.append((r, c))

            return True

        if not ((r, c) == start or is_valid(grid, r, c, visited)):

            return False

        visited.add((r, c))

        path.append((r, c))

        for dr, dc in DIRECTIONS:

            if dfs(r + dr, c + dc):

                return True

        path.pop()

        return False



    dfs(*start)

    return path

# 3. DFS Stack

def dfs_stack(grid, start, end):

    stack = [(start, [start])]

    visited = set()



    while stack:

        (r, c), path = stack.pop()

        if (r, c) == end:

            return path

        if (r, c) in visited:

            continue

        visited.add((r, c))

        for dr, dc in DIRECTIONS:

            nr, nc = r + dr, c + dc

            if is_valid(grid, nr, nc, visited):

                stack.append(((nr, nc), path + [(nr, nc)]))

    return []



# 4. Greedy

def greedy(grid, start, end):

    heap = []

    heapq.heappush(heap, (heuristic(start, end), start, [start]))

    visited = set()



    while heap:

        _, (r, c), path = heapq.heappop(heap)

        if (r, c) == end:

            return path

        if (r, c) in visited:

            continue

        visited.add((r, c))

        for dr, dc in DIRECTIONS:

            nr, nc = r + dr, c + dc

            if is_valid(grid, nr, nc, visited):

                new_path = path + [(nr, nc)]

                heapq.heappush(heap, (heuristic((nr, nc), end), (nr, nc), new_path))

    return []



# Maze input

maze = [

    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],

    ['#', 'A', '-', '#', '-', '-', '-', '#', '-', '-', '-', 'B', '#'],

    ['#', '-', '-', '#', '-', '#', '-', '#', '-', '#', '-', '#', '#'],

    ['#', '-', '#', '#', '-', '#', '-', '-', '-', '#', '-', '-', '#'],

    ['#', '-', '-', '-', '-', '#', '#', '#', '-', '#', '#', '-', '#'],

    ['#', '#', '#', '-', '#', '-', '-', '#', '-', '-', '#', '-', '#'],

    ['#', '-', '-', '-', '#', '-', '#', '#', '#', '-', '#', '-', '#'],

    ['#', '-', '#', '-', '-', '-', '-', '-', '#', '-', '-', '-', '#'],

    ['#', '-', '#', '#', '#', '#', '#', '-', '#', '#', '#', '-', '#'],

    ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],

    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']

]



# Знаходимо старт і фініш

start = find_point(maze, 'A')

end = find_point(maze, 'B')



# Запускаємо всі алгоритми

algorithms = {

    "Backtracking": backtracking,

    # "Backtracking + Heuristic": backtracking_heuristic,

    "DFS": dfs_stack,

    "Greedy": greedy

}



for name, func in algorithms.items():

    print(f"--- {name} ---")

    t0 = time.perf_counter()

    path = func(maze, start, end)

    t1 = time.perf_counter()

    if path:

        print(f"Path found (length {len(path)}):")

        print_path(maze, path)

    else:

        print("No path found.")

    print(f"Time: {t1 - t0:.6f} sec\n")


