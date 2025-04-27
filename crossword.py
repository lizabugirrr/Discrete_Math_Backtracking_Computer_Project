import time
import random

class CrosswordSolverBase:
    """
    base class for common crossword methods shared by all solvers.
    """
    def __init__(self, grid, words):
        """
        initialization.
        """
        self.grid = [row[:] for row in grid]  # deep copy
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.words = words

    def print_board(self):
        """
        current crossword grid.
        """
        for row in self.grid:
            print(''.join(row))
        print()

    def is_valid_placement(self, word, row, col, direction):
        """
        checks if a word can be placed at the specified row, col in the given direction.
        """
        if direction == 'H':  # horizontal
            if col + len(word) > self.cols:
                return False
            for i in range(len(word)):
                if self.grid[row][col + i] not in ('-', word[i]):
                    return False
        elif direction == 'V':  # vertical
            if row + len(word) > self.rows:
                return False
            for i in range(len(word)):
                if self.grid[row + i][col] not in ('-', word[i]):
                    return False
        return True

    def place_word(self, word, row, col, direction):
        """
        places a word on the grid in the specified direction and returns the previous state for backtracking.
        """
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
        """
        removes a word from the grid by restoring it to its previous state.
        """
        if direction == 'H':
            for i in range(len(word)):
                self.grid[row][col + i] = previous_state[i]
        elif direction == 'V':
            for i in range(len(word)):
                self.grid[row + i][col] = previous_state[i]

class BacktrackingSolver(CrosswordSolverBase):
    """
    solver using the backtracking algorithm.
    """
    def solve(self, index=0):
        """
        solving using the backtracking algorithm.
        """
        if index == len(self.words):
            return True
        word = self.words[index]
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_valid_placement(word, row, col, 'H'):
                    previous_state = self.place_word(word, row, col, 'H')
                    if self.solve(index + 1):
                        return True
                    self.remove_word(word, row, col, 'H', previous_state)
                if self.is_valid_placement(word, row, col, 'V'):
                    previous_state = self.place_word(word, row, col, 'V')
                    if self.solve(index + 1):
                        return True
                    self.remove_word(word, row, col, 'V', previous_state)
        return False

def benchmark_solver(solver_class, grid, words, name):
    """Benchmarks a solver class by measuring execution time."""
    solver = solver_class(grid, words)
    start_time = time.perf_counter()
    success = solver.solve()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"{name} Solver:")
    if success:
        print("Solution Found:")
        solver.print_board()
    else:
        print("No solution exists.")
    print(f"Execution Time: {elapsed_time:.6f} seconds\n")
    return elapsed_time

if __name__ == "__main__":
    with open("words.txt", "r", encoding='utf-8') as f:
        all_words = [line.strip().upper() for line in f if line.strip()]

    #вибираємо N слів
    N = 10
    filtered_words = [word for word in all_words if len(word) <= 5]
    selected_words = random.sample(filtered_words, k=N)
    grid = [
        ['-', '-', '#', '-', '-', '-', '#', '-', '-', '-'],
        ['-', '-', '#', '-', '-', '-', '#', '-', '-', '-'],
        ['#', '#', '#', '-', '-', '-', '#', '#', '#', '-'],
        ['-', '-', '#', '-', '#', '-', '#', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '#', '-', '#', '-', '#', '-', '#', '-', '#'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '#', '-', '-', '-', '#', '-', '-', '-'],
        ['#', '-', '-', '-', '#', '-', '-', '-', '#', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
    ]

    backtracking_time = benchmark_solver(BacktrackingSolver, grid, selected_words, "Backtracking")
