# import pygame
# import time
# import argparse

# # visualisation settings
# CELL_SIZE = 40
# FPS = 60
# FORWARD_DELAY = 0.05
# BACKTRACK_DELAY = 0.08

# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)
# BLUE = (30, 144, 255)
# GRAY = (200, 200, 200)

# def draw_cell(screen, r, c, symbol):
#     color = WHITE
#     if symbol == '#':
#         color = BLACK
#     elif symbol == 'A':
#         color = GREEN
#     elif symbol == 'B':
#         color = RED
#     elif symbol == '*':
#         color = BLUE
#     elif symbol == '.':
#         color = GRAY  # returning back
#     pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#     pygame.draw.rect(screen, BLACK, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# best_path_length = float('inf')

# def solve_maze(screen, maze, r, c, end_r, end_c, clock, path_length=0):
#     """ solution """
#     global best_path_length # global variable to keep track of the shortest path length found so far

#     if path_length >= best_path_length:
#         return False

#     if (r, c) == (end_r, end_c):
#         best_path_length = path_length
#         return True

#     rows, cols = len(maze), len(maze[0])
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

#     directions.sort(key=lambda d: abs((r + d[0]) - end_r) + abs((c + d[1]) - end_c))#euristic: sort directions based on distance to the end point

#     for dr, dc in directions:
#         nr, nc = r + dr, c + dc
#         if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] in ('-', 'B'):
#             original = maze[nr][nc]
#             if original != 'B':
#                 maze[nr][nc] = '*'  # mark as visited
#             draw_cell(screen, nr, nc, maze[nr][nc])
#             pygame.display.update()
#             clock.tick(FPS)
#             time.sleep(FORWARD_DELAY)

#             if solve_maze(screen, maze, nr, nc, end_r, end_c, clock, path_length + 1):
#                 return True

#             # Backtrack if not found
#             if original != 'B':
#                 maze[nr][nc] = '.'  # mark as unvisited
#             draw_cell(screen, nr, nc, maze[nr][nc])
#             pygame.display.update()
#             clock.tick(FPS)
#             time.sleep(BACKTRACK_DELAY)

#     return False
# if __name__ == "__main__":
#     pygame.init()
#     maze = [
#     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
#     ['#', 'A', '-', '#', '-', '-', '-', '#', '-', '-', '-', 'B', '#'],
#     ['#', '-', '-', '#', '-', '#', '-', '#', '-', '#', '-', '#', '#'],
#     ['#', '-', '#', '#', '-', '#', '-', '-', '-', '#', '-', '-', '#'],
#     ['#', '-', '-', '-', '-', '#', '#', '#', '-', '#', '#', '-', '#'],
#     ['#', '#', '#', '-', '#', '-', '-', '#', '-', '-', '#', '-', '#'],
#     ['#', '-', '-', '-', '#', '-', '#', '#', '#', '-', '#', '-', '#'],
#     ['#', '-', '#', '-', '-', '-', '-', '-', '#', '-', '-', '-', '#'],
#     ['#', '-', '#', '#', '#', '#', '#', '-', '#', '#', '#', '-', '#'],
#     ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
#     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
# ]
#     #maze = [
#     #     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
#     #     ['#', 'A', '-', '-', '#', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '-', '#', '#'],
#     #     ['#', '#', '#', '-', '#', '-', '#', '#', '#', '-', '#', '-', '#', '#', '#', '-', '#', '-', '#', '#', '#', '#', '-', '#', '#'],
#     #     ['#', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
#     #     ['#', '-', '#', '#', '#', '#', '-', '#', '#', '#', '#', '#', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '#', '#'],
#     #     ['#', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '#'],
#     #     ['#', '#', '#', '-', '#', '#', '#', '#', '-', '#', '-', '#', '#', '#', '#', '-', '#', '#', '#', '-', '#', '#', '#', '-', '#'],
#     #     ['#', '-', '-', '-', '-', '-', '-', '#', '-', '#', '-', '-', '-', '-', '#', '-', '-', '-', '#', '-', '-', '-', '-', '-', '#'],
#     #     ['#', '-', '#', '#', '#', '#', '-', '#', '#', '#', '#', '#', '#', '-', '#', '#', '#', '-', '#', '#', '#', '#', '#', '-', '#'],
#     #     ['#', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '#', '-', '-', '-', '-', '-', '#', '-', '#'],
#     #     ['#', '#', '#', '#', '-', '#', '#', '#', '#', '#', '#', '-', '#', '#', '#', '-', '#', '#', '#', '#', '#', '-', '#', '#', '#'],
#     #     ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
#     #     ['#', '-', '#', '#', '#', '#', '#', '#', '#', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '#'],
#     #     ['#', '-', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
#     #     ['#', '#', '#', '#', '#', '#', '#', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '#'],
#     #     ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#', '-', '#'],
#     #     ['#', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '#', '-', '#'],
#     #     ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'B', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '#'],
#     #     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
#     # ]

# #     maze = [
# #     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
# #     ['#', 'A', '-', '-', '#', '-', '-', '-', '-', '-', '#', 'B', '#'],
# #     ['#', '#', '#', '-', '#', '-', '#', '#', '#', '-', '#', '#', '#'],
# #     ['#', '-', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '#'],
# #     ['#', '-', '#', '#', '#', '#', '-', '#', '#', '#', '-', '#', '#'],
# #     ['#', '-', '-', '-', '-', '#', '-', '-', '-', '#', '-', '-', '#'],
# #     ['#', '#', '#', '-', '#', '#', '#', '#', '-', '#', '#', '-', '#'],
# #     ['#', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '#'],
# #     ['#', '-', '#', '#', '#', '#', '-', '#', '#', '#', '#', '-', '#'],
# #     ['#', '-', '-', '-', '-', '#', '-', '-', '-', '-', '#', '-', '#'],
# #     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
# # ]

#     rows, cols = len(maze), len(maze[0])
#     screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE))
#     pygame.display.set_caption("Maze Solver (Backtracking Visualization)")
#     start = None
#     end = None
#     for r in range(rows):
#         for c in range(cols):
#             if maze[r][c] == 'A':
#                 start = (r, c)
#             elif maze[r][c] == 'B':
#                 end = (r, c)
#     if not start or not end:
#         print("Maze must have start (A) and end (B) points.")
#     clock = pygame.time.Clock()
#     #draw a maze from the beginning
#     for r in range(rows):
#         for c in range(cols):
#             draw_cell(screen, r, c, maze[r][c])
#     pygame.display.flip()

#     # start solving
#     found_path = solve_maze(screen, maze, start[0], start[1], end[0], end[1], clock)

#     if not found_path:
#         print("Шлях знайти не вдалося!")

#     running = True
#     while running:
#         clock.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#     pygame.quit()



import pygame
import time
import argparse

# Constants
CELL_SIZE = 40
FPS = 60
FORWARD_DELAY = 0.05
BACKTRACK_DELAY = 0.08

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (30, 144, 255)
GRAY = (200, 200, 200)

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

def draw_cell(screen, r, c, symbol):
    color = WHITE
    if symbol == '#':
        color = BLACK
    elif symbol == 'A':
        color = GREEN
    elif symbol == 'B':
        color = RED
    elif symbol == '*':
        color = BLUE
    elif symbol == '.':
        color = GRAY
    pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, BLACK, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

best_path_length = float('inf')

def solve_maze(screen, maze, r, c, end_r, end_c, clock, path_length=0):
    global best_path_length

    if path_length >= best_path_length:
        return False

    if (r, c) == (end_r, end_c):
        best_path_length = path_length
        return True

    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    directions.sort(key=lambda d: abs((r + d[0]) - end_r) + abs((c + d[1]) - end_c))

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] in ('-', 'B'):
            original = maze[nr][nc]

            if original != 'B':
                maze[nr][nc] = '*'
            draw_cell(screen, nr, nc, maze[nr][nc])
            pygame.display.update()
            pygame.event.pump()
            time.sleep(FORWARD_DELAY)

            if solve_maze(screen, maze, nr, nc, end_r, end_c, clock, path_length + 1):
                return True

            if original != 'B':
                maze[nr][nc] = '.'
                draw_cell(screen, nr, nc, maze[nr][nc])
                pygame.display.update()
                pygame.event.pump()
                time.sleep(BACKTRACK_DELAY)

    return False


def run_console_version():
    pass

def run_pygame_version():
    pygame.init()
    rows, cols = len(maze), len(maze[0])
    screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE))
    pygame.display.set_caption("Maze Solver")

    start = None
    end = None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'A':
                start = (r, c)
            elif maze[r][c] == 'B':
                end = (r, c)

    if not start or not end:
        print("Maze must have start (A) and end (B) points.")
        return

    clock = pygame.time.Clock()

    for r in range(rows):
        for c in range(cols):
            draw_cell(screen, r, c, maze[r][c])
    pygame.display.flip()

    found_path = solve_maze(screen, maze, start[0], start[1], end[0], end[1], clock)

    if not found_path:
        print("No path found!")

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Maze Solver')
    parser.add_argument('mode', choices=['console', 'visual'], help='Display mode')
    args = parser.parse_args()

    if args.mode == 'console':
        run_console_version()
    else:
        run_pygame_version()
