import random
import time
import pygame
from colorama import init, Fore, Back, Style

init(autoreset = True)

# Sudoku Tools
def is_valid(board, row, col, num):
    for i in range(9):
        if num in (board[row][i], board[i][col]):
            return False

    row_block_start, col_block_start = 3* (row // 3), 3* (col // 3)
    row_block_end, col_block_end  = row_block_start + 3, col_block_start + 3

    for i in range(row_block_start, row_block_end):
        for j in range(col_block_start, col_block_end):
            if board[i][j] == num:
                return False
    return True

def find_empty_cell(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0 :
                return row,col
    return None

def generate_sudoku(clues=25):
    board = [[0] * 9 for _ in range(9)]
    solve_backtracking(board)
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    for i in range(81 - clues):
        r, c = cells[i]
        board[r][c] = 0
    return board

def solve_backtracking(board):
    empty = find_empty_cell(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_backtracking(board):
                return True
            board[row][col] = 0
    return False

#Console Display

def print_board(board, highlight=None):
    for i in range(9):
        row_str = ""
        for j in range(9):
            val = board[i][j]
            display = "." if val == 0 else str(val)
            if highlight == (i, j):
                row_str += Back.GREEN + Fore.BLACK + display + Style.RESET_ALL + " "
            else:
                row_str += display + " "
            if (j + 1) % 3 == 0 and j < 8:
                row_str += "| "
        print(row_str)
        if (i + 1) % 3 == 0 and i < 8:
            print("-" * 21)
    print("\n")

def visual_solve_console(board, delay=0.05):
    empty = find_empty_cell(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            print_board(board, highlight=(row, col))
            time.sleep(delay)
            if visual_solve_console(board, delay):
                return True
            board[row][col] = 0
            print_board(board, highlight=(row, col))
            time.sleep(delay / 2)
    return False

def run_console_version():
    board = generate_sudoku(clues=30)
    print("Initial Board:\n")
    print_board(board)
    input("Press Enter to start solving...\n")
    if visual_solve_console(board):
        print("Solved Board:\n")
        print_board(board)
    else:
        print("No solution found.")

# Pygame Display

WIDTH, HEIGHT = 540, 540
CELL = WIDTH // 9

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver Visualizer")
font = pygame.font.SysFont("arial", 35)

def draw_board(board, highlight=None):
    win.fill((255, 255, 255))
    for i in range(10):
        line_width = 4 if i % 3 == 0 else 1
        pygame.draw.line(win, (0, 0, 0), (0, i * CELL), (WIDTH, i * CELL), line_width)
        pygame.draw.line(win, (0, 0, 0), (i * CELL, 0), (i * CELL, HEIGHT), line_width)

    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num != 0:
                color = (50, 50, 50)
                if highlight == (i, j):
                    color = (50, 150, 50)
                text = font.render(str(num), True, color)
                win.blit(text, (j * CELL + 20, i * CELL + 10))

    pygame.display.update()

def visual_solve_pygame(board):
    empty = find_empty_cell(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            draw_board(board, highlight=(row, col))
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if visual_solve_pygame(board):
                return True
            board[row][col] = 0
            draw_board(board, highlight=(row, col))
            pygame.time.delay(50)
    return False

def run_pygame_version():
    board = generate_sudoku(clues=30)
    running = True
    solving = False
    while running:
        draw_board(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    solving = True
        if solving:
            visual_solve_pygame(board)
            solving = False
    pygame.quit()


if __name__ == "__main__":
    mode = input("Choose mode: (c)onsole or (v)isual: ").strip().lower()
    if mode == 'c':
        run_console_version()
    else:
        run_pygame_version()
