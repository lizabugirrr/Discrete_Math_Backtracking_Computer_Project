import random
import time
import math
import pygame
from colorama import init, Fore, Back, Style

init(autoreset = True)

# Sudoku Tools
def is_valid(board, row, col, num):
    size = len(board)
    base = int(size**0.5)
    for i in range(size):
        if num in (board[row][i], board[i][col]):
            return False
    start_row = base * (row // base)
    start_col = base * (col // base)
    for i in range(start_row, start_row + base):
        for j in range(start_col, start_col + base):
            if board[i][j] == num:
                return False
    return True

def find_empty_cell(board):
    size = len(board)
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                return row, col
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
    size = len(board)
    for num in range(1, size + 1):
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
    size = len(board)
    for num in range(1, size + 1):
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

def run_console_version(clues):
    clues = choose_difficulty()
    board = generate_sudoku(clues=clues)
    print("\nInitial Board (Difficulty: {} clues):\n".format(clues))
    print_board(board)

    while True:
        proceed = input("Press Enter to solve or type 'q' to quit: ").strip().lower()
        if proceed == "":
            break
        elif proceed == "q":
            print("Exiting...")
            return

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
    size = len(board)
    for num in range(1, size + 1):
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

def run_pygame_version(clues):
    board = generate_sudoku(clues=clues)
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

def choose_difficulty():
    print("Select Difficulty:")
    print("1 - Easy")
    print("2 - Medium")
    print("3 - Hard")
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice == "1":
            return 40
        elif choice == "2":
            return 30
        elif choice == "3":
            return 20
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Sudoku Solver')
    parser.add_argument('mode', choices=['console', 'visual'], help='Display mode')
    parser.add_argument('difficulty', type=int, nargs='?', default=30, 
                       help='Number of clues (difficulty)')

    args = parser.parse_args()

    if args.mode == 'console':
        run_console_version(None)
    else:
        run_pygame_version(args.difficulty)
