import pygame
import random
import time

# Константи для візуалізації
CELL_SIZE = 40
FPS = 2
FORWARD_DELAY = 0.5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (30, 144, 255)
GRAY = (200, 200, 200)

class CrosswordSolverBase:
    def __init__(self, grid, words, screen):
        self.grid = [row[:] for row in grid] #deep copy
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.words = words
        self.screen = screen
        self.font = pygame.font.Font(None, 30)

    def draw_cell(self, row, col, value):
        # draw a cell
        color = WHITE if value == '-' else GRAY
        pygame.draw.rect(self.screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        if value != '-':
            text = self.font.render(value, True, BLACK)
            self.screen.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 5))

    def print_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.draw_cell(r, c, self.grid[r][c])
        pygame.display.update()

    def is_valid_placement(self, word, row, col, direction):
        if direction == 'H':
            if col + len(word) > self.cols:
                return False
            for i in range(len(word)):
                if self.grid[row][col + i] not in ('-', word[i]):
                    return False
        elif direction == 'V':
            if row + len(word) > self.rows:
                return False
            for i in range(len(word)):
                if self.grid[row + i][col] not in ('-', word[i]):
                    return False
        return True

    def place_word(self, word, row, col, direction):
        previous_state = []
        if direction == 'H':
            for i in range(len(word)):
                previous_state.append(self.grid[row][col + i])
                self.grid[row][col + i] = word[i]
        elif direction == 'V':
            for i in range(len(word)):
                previous_state.append(self.grid[row + i][col])
                self.grid[row + i][col] = word[i]
        return previous_state

    def remove_word(self, word, row, col, direction, previous_state):
        if direction == 'H':
            for i in range(len(word)):
                self.grid[row][col + i] = previous_state[i]
        elif direction == 'V':
            for i in range(len(word)):
                self.grid[row + i][col] = previous_state[i]

class BacktrackingSolver(CrosswordSolverBase):
    def solve(self, index=0):
        if index == len(self.words):
            return True
        word = self.words[index]
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_valid_placement(word, row, col, 'H'):
                    previous_state = self.place_word(word, row, col, 'H')
                    self.print_board()
                    pygame.display.update()
                    time.sleep(FORWARD_DELAY)

                    if self.solve(index + 1):
                        return True
                    self.remove_word(word, row, col, 'H', previous_state)

                if self.is_valid_placement(word, row, col, 'V'):
                    previous_state = self.place_word(word, row, col, 'V')
                    self.print_board()
                    pygame.display.update()
                    time.sleep(FORWARD_DELAY)

                    if self.solve(index + 1):
                        return True
                    self.remove_word(word, row, col, 'V', previous_state)

        return False

def benchmark_solver(solver_class, grid, words, name):
    pygame.init()
    screen = pygame.display.set_mode((len(grid[0]) * CELL_SIZE, len(grid) * CELL_SIZE))
    pygame.display.set_caption(f"{name} Solver")

    solver = solver_class(grid, words, screen)
    solver.print_board()

    start_time = time.perf_counter()
    success = solver.solve()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    if success:
        print(f"{name} Solver: Solution Found:")
        solver.print_board()
    else:
        print(f"{name} Solver: No solution exists.")
    print(f"Execution Time: {elapsed_time:.6f} seconds\n")
    pygame.quit()

# grid = [
#     ['-', '-', '#', '-', '-', '#', '-', '#', '-', '#', '#', '#', '-', '#', '#'],
#     ['-', '#', '#', '-', '#', '#', '-', '-', '#', '#', '#', '-', '#', '#', '-'],
#     ['-', '#', '#', '#', '-', '#', '#', '-', '-', '#', '#', '#', '-', '#', '-'],
#     ['#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '-', '#', '-', '-'],
#     ['-', '-', '-', '#', '#', '-', '#', '#', '-', '#', '-', '-', '-', '#', '#'],
#     ['-', '-', '#', '#', '#', '-', '-', '#', '#', '-', '#', '#', '#', '#', '-'],
#     ['#', '-', '-', '-', '#', '#', '-', '-', '#', '#', '-', '-', '-', '#', '-'],
#     ['-', '-', '-', '#', '#', '#', '-', '-', '-', '-', '-', '#', '-', '-', '#'],
#     ['#', '#', '#', '#', '-', '-', '#', '#', '#', '-', '#', '-', '-', '#', '#'],
#     ['-', '#', '#', '#', '-', '#', '-', '#', '-', '#', '#', '#', '#', '-', '#']
# ]
grid = [
    ['-', '#', '#', '#'],
    ['-', '#', '#', '#'],
    ['-', '-', '-', '-'],
    ['#', '#', '#', '-'],
    ['#', '#', '#', '-'],
    ['#', '#', '#', '-'],
    ['#', '#', '#', '-']
]

if __name__ == "__main__":
    with open("words_2.txt", "r", encoding='utf-8') as f:
        all_words = [line.strip().upper() for line in f if line.strip()]

    N = int(input('введіть кількість слів: '))
    selected_words = random.sample([word for word in all_words if 3 <= len(word) <= 8], k=N)

    benchmark_solver(BacktrackingSolver, grid, selected_words, "Backtracking")
