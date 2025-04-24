import time
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
            if col + len(word) > self.cols:  # word goes out of bounds
                return False
            for i in range(len(word)):
                if self.grid[row][col + i] not in ('-', word[i]):  # wrong placement
                    return False
        elif direction == 'V':  # vertical
            if row + len(word) > self.rows:  # word goes out of bounds
                return False
            for i in range(len(word)):
                if self.grid[row + i][col] not in ('-', word[i]):  # wrong placement
                    return False
        return True
    def place_word(self, word, row, col, direction):
        """
        places a word on the grid in the specified direction and returns the previous state for backtracking.
        """
        previous_state = []
        if direction == 'H':  # horizontal
            for i in range(len(word)):
                previous_state.append(self.grid[row][col + i])
                self.grid[row][col + i] = word[i]
        elif direction == 'V':  # vertical
            for i in range(len(word)):
                previous_state.append(self.grid[row + i][col])
                self.grid[row + i][col] = word[i]
        return previous_state
    def remove_word(self, word, row, col, direction, previous_state):
        """
        removes a word from the grid by restoring it to its previous state.
        """
        if direction == 'H':  # horizontal
            for i in range(len(word)):
                self.grid[row][col + i] = previous_state[i]
        elif direction == 'V':  # vertical
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
        if index == len(self.words):  # All words have been placed
            return True
        word = self.words[index]
        for row in range(self.rows):
            for col in range(self.cols):
                # Try placing horizontally
                if self.is_valid_placement(word, row, col, 'H'):
                    previous_state = self.place_word(word, row, col, 'H')
                    if self.solve(index + 1):  # placing the next word, recursively
                        return True
                    self.remove_word(word, row, col, 'H', previous_state)  # backtrack
                # Try placing vertically
                if self.is_valid_placement(word, row, col, 'V'):
                    previous_state = self.place_word(word, row, col, 'V')
                    if self.solve(index + 1):   # placing the next word, recursively
                        return True
                    self.remove_word(word, row, col, 'V', previous_state)  # backtrack
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
    grid = [
        ['-', '-', '#', '-', '-'],
        ['-', '-', '#', '-', '-'],
        ['#', '#', '#', '#', '-'],
        ['-', '-', '#', '-', '#'],
        ['-', '-', '-', '-', '-']
    ]
    words = ["HELLO", "SEE", "CS"]
    backtracking_time = benchmark_solver(BacktrackingSolver, grid, words, "Backtracking")
#питання: номери слів