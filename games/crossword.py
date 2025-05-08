import random
import time
import argparse
import os
import sys

# constants
CELL_SIZE = 40
FPS = 2
FORWARD_DELAY = 0.5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (30, 144, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

class CrosswordSolverBase:
    def __init__(self, grid, words, screen, valid_words, use_console_visualization=False):
        self.grid = [row[:] for row in grid] #deep copy
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.words = words
        self.screen = screen
        self.valid_words = valid_words  # dict for valid words
        self.word_positions = []  # list to store placed words to check intersections
        self.use_console_visualization = use_console_visualization

        if screen is not None:
            import pygame
            self.font = pygame.font.Font(None, 30)
    # function for visualisation
    def draw_cell(self, row, col, value, highlight=False):
        if self.screen is None:
            return

        # draw a cell
        import pygame
        color = YELLOW if highlight else (WHITE if value == '-' else GRAY)
        pygame.draw.rect(self.screen, color, (col * CELL_SIZE, row * CELL_SIZE,\
         CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE,\
         CELL_SIZE, CELL_SIZE), 1)

        if value != '-':
            text = self.font.render(value, True, BLACK)
            self.screen.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 5))
    # function for visualisation
    def clear_console(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    # function for visualisation
    def print_board(self, highlight_positions=None):
        if self.use_console_visualization:
            self.clear_console()
            print("\nПоточний стан кросворду:")
            for r in range(self.rows):
                row_str = ""
                for c in range(self.cols):
                    cell_value = self.grid[r][c]
                    if highlight_positions and (r, c) in highlight_positions:
                        if cell_value == '-':
                            row_str += '[ ]'
                        else:
                            row_str += f'[{cell_value}]'
                    else:
                        if cell_value == '-':
                            row_str += ' . '
                        elif cell_value == '#':
                            row_str += ' # '
                        else:
                            row_str += f' {cell_value} '
                print(row_str)

            if self.word_positions:
                print("\nРозміщені слова:")
            print("=" * 40)
            time.sleep(FORWARD_DELAY)
            return

        if self.screen is None:
            for row in self.grid:
                print(' '.join(row))
            print()
            return

        import pygame
        for r in range(self.rows):
            for c in range(self.cols):
                highlight = False
                if highlight_positions:
                    if (r, c) in highlight_positions:
                        highlight = True
                self.draw_cell(r, c, self.grid[r][c], highlight)
        pygame.display.update()

    def is_valid_placement(self, word, row, col, direction):
        if direction == 'H':
            if col + len(word) > self.cols:
                return False
            for i, char in enumerate(word):
                if self.grid[row][col + i] not in ('-', char):
                    return False
        elif direction == 'V':
            if row + len(word) > self.rows:
                return False
            for i, char in enumerate(word):
                if self.grid[row + i][col] not in ('-', char):
                    return False
        if not self.check_intersections(word, row, col, direction):
            return False

        return True

    def check_intersections(self, new_word, row, col, direction):
        #create a temporary grid to check intersections
        temp_grid = [row[:] for row in self.grid]
        if direction == 'H':
            for i, char in enumerate(new_word):
                temp_grid[row][col + i] = char
        else:  # 'V'
            for i, char in enumerate(new_word):
                temp_grid[row + i][col] = char
        for r in range(self.rows):
            current_word = ""
            start_col = 0
            for c in range(self.cols + 1):
                if c < self.cols and temp_grid[r][c] != '#' and temp_grid[r][c] != '-':
                    if current_word == "":
                        start_col = c
                    current_word += temp_grid[r][c]
                else:
                    if len(current_word) > 1:
                        # is_part_of_new_word = (direction == 'H' and r == row and 
                        #                       start_col <= col + len(new_word) - 1 and 
                        #                       col <= start_col + len(current_word) - 1)
                        is_part_of_new_word = (direction == 'H' and r == row and 
                                              start_col <= col + len(new_word) - 1 and 
                                              col <= start_col + len(current_word) - 1)
                        if not is_part_of_new_word or (direction == 'H' and r == row):
                            if current_word.lower() not in self.valid_words:
                                return False
                    current_word = ""
        for c in range(self.cols):
            current_word = ""
            start_row = 0
            for r in range(self.rows + 1):
                if r < self.rows and temp_grid[r][c] != '#' and temp_grid[r][c] != '-':
                    if current_word == "":
                        start_row = r
                    current_word += temp_grid[r][c]
                else:
                    if len(current_word) > 1:
                        # is_part_of_new_word = (direction == 'V' and c == col and 
                        #                       start_row <= row + len(new_word) - 1 and 
                        #                       row <= start_row + len(current_word) - 1)
                        is_part_of_new_word = (direction == 'V' and c == col and 
                                              start_row <= row + len(new_word) - 1 and 
                                              row <= start_row + len(current_word) - 1)
                        if not is_part_of_new_word or (direction == 'V' and c == col):
                            if current_word.lower() not in self.valid_words:
                                return False
                    current_word = ""

        return True

    def place_word(self, word, row, col, direction):
        previous_state = []
        positions = []

        if direction == 'H':
            for i, char in enumerate(word):
                previous_state.append(self.grid[row][col + i])
                self.grid[row][col + i] = char
                positions.append((row, col + i))
        elif direction == 'V':
            for i, char in enumerate(word):
                previous_state.append(self.grid[row + i][col])
                self.grid[row + i][col] = char
                positions.append((row + i, col))

        self.word_positions.append({
            'word': word,
            'row': row,
            'col': col,
            'direction': direction,
            'positions': positions
        })

        return previous_state

    def remove_word(self, word, row, col, direction, previous_state):
        if direction == 'H':
            for i in range(len(word)):
                self.grid[row][col + i] = previous_state[i]
        elif direction == 'V':
            for i in range(len(word)):
                self.grid[row + i][col] = previous_state[i]

        for i, word_info in enumerate(self.word_positions):
            if (word_info['word'] == word and 
                word_info['row'] == row and 
                word_info['col'] == col and 
                word_info['direction'] == direction):
                self.word_positions.pop(i)
                break
    # function for visualisation
    def highlight_intersections(self):
        intersections = []
        for i, word1 in enumerate(self.word_positions):
            for j, word2 in enumerate(self.word_positions):
                if i >= j:
                    continue
                for pos1 in word1['positions']:
                    for pos2 in word2['positions']:
                        if pos1 == pos2:
                            intersections.append(pos1)

        return intersections

class BacktrackingSolver(CrosswordSolverBase):
    def solve(self, index=0):
        if index == len(self.words):
        #     if any('-' in sublist for sublist in self.grid):
        #         return False
        #     else:
            return True
        # if any('-' in sublist for sublist in self.grid):
        #     print (self.grid)
        word = self.words[index]

        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_valid_placement(word, row, col, 'H'):
                    previous_state = self.place_word(word, row, col, 'H')
                    intersections = self.highlight_intersections()
                    self.print_board(intersections)     
                    if self.screen is not None and not self.use_console_visualization:
                        import pygame
                        # pygame.display.update()
                        # time.sleep(FORWARD_DELAY)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        pygame.display.update()
                        time.sleep(FORWARD_DELAY)

                    if self.solve(index + 1):
                        return True
                    self.remove_word(word, row, col, 'H', previous_state)
                    # Show backtracking in console visualization
                    if self.use_console_visualization:
                        self.print_board(self.highlight_intersections())

                if self.is_valid_placement(word, row, col, 'V'):
                    previous_state = self.place_word(word, row, col, 'V')
                    intersections = self.highlight_intersections()
                    self.print_board(intersections)

                    if self.screen is not None and not self.use_console_visualization:
                        import pygame
                        # pygame.display.update()
                        # time.sleep(FORWARD_DELAY)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        pygame.display.update()
                        time.sleep(FORWARD_DELAY)

                    if self.solve(index + 1):
                        return True
                    self.remove_word(word, row, col, 'V', previous_state)
                    # Show backtracking in console visualization
                    if self.use_console_visualization:
                        self.print_board(self.highlight_intersections())

        return False
# function for visualisation
def benchmark_solver(solver_class, grid, words, name, valid_words, use_console=False):
    screen = None
    if not use_console:
        try:
            import pygame
            pygame.init()
            screen = pygame.display.set_mode((len(grid[0]) * CELL_SIZE, len(grid) * CELL_SIZE))
            pygame.display.set_caption(f"{name} Solver")
        except Exception:
            print("Pygame не може бути ініціалізовано. Використовуємо консольний режим.")
            use_console = True

    solver = solver_class(grid, words, screen, valid_words, use_console_visualization=use_console)

    if use_console:
        print("\nПочатковий стан кросворду:")

    solver.print_board()

    start_time = time.perf_counter()
    success = solver.solve()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    if success and not any('-' in sublist for sublist in solver.grid):
        print(f"\n{name} Solver: Рішення знайдено:")
        solver.print_board(solver.highlight_intersections())
    else:
        print(f"\n{name} Solver: Рішення не існує.")
        print (words)
    print(f"Час виконання: {elapsed_time:.6f} секунд\n")

    if screen is not None:
        import pygame
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

# grid = [
#     ['-', '#', '#', '#'],
#     ['-', '#', '#', '#'],
#     ['-', '-', '-', '-'],
#     ['#', '#', '#', '-'],
#     ['#', '#', '#', '-'],
#     ['#', '#', '#', '-'],
#     ['#', '#', '#', '-']
# ]
grid = [
    ['-','-','-', '#', '-', '-', '-'],
    ['#', '#', '#', '#', '#','#', '#'],
    ['#','#', '-', '-', '-', '#', '#'],
    ['#', '#', '#', '#','#', '#', '#'],
    ['-','-','-','-','-','-','-'],
    ['#', '#', '#', '-','#', '#', '#'],
    ['#', '#', '#', '-', '#', '#', '#'],
    ['#', '#', '#', '-', '#', '#', '#']
]
# grid = [
#     ['-','-','-', '#', '-', '-', '-'],
#     ['#', '#', '#', '#', '#','#', '#'],
#     ['#','#', '-', '-', '-', '#', '#'],
#     ['#', '#', '#', '#','#', '#', '#'],
#     ['-','-','-','-','-','-','-']
# ]
def load_words_from_file(filename):
    if not os.path.exists(filename):
        print(f"Файл {filename} не знайдено.")
        return []

    with open(filename, "r", encoding='utf-8') as f:
        words = [line.strip().lower() for line in f if line.strip()]
    return words

def run_console_version():
    words_file = 'words_2.txt'
    all_words = load_words_from_file(words_file)

    if not all_words:
        print("Не вдалося завантажити слова. Використовуємо тестовий набір.")
        all_words = ["cat", "dog", "rat", "bat", "hat", "morning", "teacher", "picture", "lamp", "mat"]

    valid_words_set = set(all_words)
    N = 5
    # try:
    #     N = int(input('Введіть кількість слів для кросворду: '))
    selected_words = random.sample([word for word in all_words if 3 <= len(word) <= 8], k=min(N, len(all_words)))
    
    # except:
    #     print("Помилка при виборі слів. Використовуємо 5 слів.")
    #     selected_words = random.sample([word for word in all_words if 3 <= len(word) <= 8], k=min(5, len(all_words)))

    selected_words = [word.upper() for word in selected_words]
    print(f"Вибрані слова: {selected_words}")
    benchmark_solver(BacktrackingSolver, grid, selected_words, "Backtracking", valid_words_set, use_console=True)

def run_pygame_version():
    try:
        # words_file = 'words_2.txt'
        words_file = os.path.join(os.path.dirname(__file__), 'words_2.txt')
        all_words = load_words_from_file(words_file)

        valid_words_set = set(all_words)
        N = 5
        # N = int(input('Введіть кількість слів для кросворду: '))
        selected_words = random.sample([word for word in all_words if 3 <= len(word) <= 8], k=min(N, len(all_words)))
        selected_words = [word.upper() for word in selected_words]
        benchmark_solver(BacktrackingSolver, grid, selected_words, "Backtracking", valid_words_set, use_console=False)
    except Exception as e:
        print(f"Помилка: {e}")
        print("Використовуємо консольний режим.")
        run_console_version()

#run_console_version()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crossword Solver')
    parser.add_argument('mode', choices=['console', 'visual'], help='Display mode')
    args = parser.parse_args()
    if args.mode == 'console':
        run_console_version()
    else:
        run_pygame_version()
