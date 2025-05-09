import time

class CrosswordSolverBase:
    """Base class for common crossword methods shared by all solvers."""

    def __init__(self, grid, words):
        self.grid = [row[:] for row in grid]  # Deep copy of the grid
        self.words = words
        self.rows = len(grid)
        self.cols = len(grid[0])

    def print_board(self):
        """Prints the current crossword grid."""
        for row in self.grid:
            print(''.join(row))
        print()

    def is_valid_placement(self, word, row, col, direction):
        """
        Checks if a word can be placed at the specified row, col in the given direction.
        - Direction 'H' is horizontal, 'V' is vertical.
        """
        if direction == 'H':  # Horizontal placement
            if col + len(word) > self.cols:  # Word goes out of bounds
                return False
            for i in range(len(word)):
                if self.grid[row][col + i] not in ('-', word[i]):  # Conflict in placement
                    return False

        elif direction == 'V':  # Vertical placement
            if row + len(word) > self.rows:  # Word goes out of bounds
                return False
            for i in range(len(word)):
                if self.grid[row + i][col] not in ('-', word[i]):  # Conflict in placement
                    return False

        return True

    def place_word(self, word, row, col, direction):
        """
        Places a word on the grid in the specified direction and returns the previous state for backtracking.
        """
        previous_state = []
        if direction == 'H':  # Horizontal placement
            for i in range(len(word)):
                previous_state.append(self.grid[row][col + i])
                self.grid[row][col + i] = word[i]

        elif direction == 'V':  # Vertical placement
            for i in range(len(word)):
                previous_state.append(self.grid[row + i][col])
                self.grid[row + i][col] = word[i]

        return previous_state

    def remove_word(self, word, row, col, direction, previous_state):
        """
        Removes a word from the grid by restoring it to its previous state.
        """
        if direction == 'H':  # Horizontal placement
            for i in range(len(word)):
                self.grid[row][col + i] = previous_state[i]

        elif direction == 'V':  # Vertical placement
            for i in range(len(word)):
                self.grid[row + i][col] = previous_state[i]


class BacktrackingSolver(CrosswordSolverBase):
    """Solver using the backtracking algorithm."""

    def solve(self, index=0):
        if index == len(self.words):  # All words have been placed
            return True

        word = self.words[index]
        for row in range(self.rows):
            for col in range(self.cols):
                # Try placing horizontally
                if self.is_valid_placement(word, row, col, 'H'):
                    previous_state = self.place_word(word, row, col, 'H')
                    if self.solve(index + 1):  # Recursively place the next word
                        return True
                    self.remove_word(word, row, col, 'H', previous_state)  # Backtrack

                # Try placing vertically
                if self.is_valid_placement(word, row, col, 'V'):
                    previous_state = self.place_word(word, row, col, 'V')
                    if self.solve(index + 1):  # Recursively place the next word
                        return True
                    self.remove_word(word, row, col, 'V', previous_state)  # Backtrack

        return False


class BruteForceSolver(CrosswordSolverBase):
    """Solver using the brute force algorithm."""

    def solve(self, index=0):
        if index == len(self.words):  # All words have been placed
            return True

        word = self.words[index]
        for row in range(self.rows):
            for col in range(self.cols):
                # Try placing horizontally
                if self.is_valid_placement(word, row, col, 'H'):
                    previous_state = self.place_word(word, row, col, 'H')
                    if self.solve(index + 1):  # Recursively place the next word
                        return True
                    self.remove_word(word, row, col, 'H', previous_state)  # Backtrack

                # Try placing vertically
                if self.is_valid_placement(word, row, col, 'V'):
                    previous_state = self.place_word(word, row, col, 'V')
                    if self.solve(index + 1):  # Recursively place the next word
                        return True
                    self.remove_word(word, row, col, 'V', previous_state)  # Backtrack

        return False


class GreedySolver(CrosswordSolverBase):
    """Solver using the greedy algorithm."""

    def score_placement(self, word, row, col, direction):
        """
        Scores a potential word placement based on the number of matching letters
        or overlaps with existing grid content.
        """
        score = 0
        if direction == 'H':  # Horizontal placement
            for i in range(len(word)):
                if self.grid[row][col + i] == word[i]:  # Overlap with existing letter
                    score += 1

        elif direction == 'V':  # Vertical placement
            for i in range(len(word)):
                if self.grid[row + i][col] == word[i]:  # Overlap with existing letter
                    score += 1

        return score

    def find_best_placement(self, word):
        """
        Finds the best placement for a word based on the greedy scoring function.
        Returns the row, col, direction, and score.
        """
        best_score = -1
        best_row, best_col, best_direction = None, None, None

        for row in range(self.rows):
            for col in range(self.cols):
                # Check horizontal placement
                if self.is_valid_placement(word, row, col, 'H'):
                    score = self.score_placement(word, row, col, 'H')
                    if score > best_score:
                        best_score = score
                        best_row, best_col, best_direction = row, col, 'H'

                # Check vertical placement
                if self.is_valid_placement(word, row, col, 'V'):
                    score = self.score_placement(word, row, col, 'V')
                    if score > best_score:
                        best_score = score
                        best_row, best_col, best_direction = row, col, 'V'

        return best_row, best_col, best_direction, best_score

    def solve(self):
        """
        Solves the crossword puzzle using a greedy algorithm.
        - Iteratively places words based on the "best" placement at each step.
        """
        for word in self.words:
            best_row, best_col, best_direction, best_score = self.find_best_placement(word)
            if best_score == -1:  # No valid placement exists for this word
                return False
            self.place_word(word, best_row, best_col, best_direction)

        return True


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
    # Define the grid and word list
    # grid = [
    #     ['-', '#', '-', '#', '-', '#', '-'],
    #     ['-', '#', '-', '#', '-', '#', '-'],
    #     ['-', '#', '-', '#', '-', '#', '-'],
    #     ['#', '#', '-', '#', '#', '#', '#'],
    #     ['#', '#', '-', '#', '#', '#', '#'],
    #     ['#', '#', '#', '#', '#', '#', '#'],
    #     ['-', '-', '-', '-', '-', '-', '-'],
    #     ['#', '#', '#', '#', '#', '#', '#'],
    #     ['#', '#', '#', '#', '#', '#', '#'],
    #     ['-', '-', '-', '-', '-', '-', '-'],
    #     ['#', '#', '#', '#', '#', '#', '#'],
    #     ['#', '#', '#', '#', '#', '#', '#'],
    #     ['#', '#', '-', '-', '-', '-', '#']
    # ]
    # words = ["PIP", "TRY", "UCU", "LEARN", "MORNING", "UKRAINE", "BEST"]
    # grid = [
    #     ['-', '#', '-', '#', '-', '#', '-'],
    #     ['-', '#', '-', '#', '-', '#', '-'],
    #     ['-', '#', '-', '#', '-', '#', '-'],
    #     ['#', '#', '-', '#', '#', '#', '#']
    # ]

    # words = ["PIP", "FOOD", "UCU", "FLY"]
    grid = [
        ['-', '#', '-', '#', '-', '#', '-'],
        ['-', '#', '-', '#', '-', '#', '-'],
        ['-', '#', '-', '#', '-', '#', '-'],
        ['#', '#', '-', '#', '#', '#', '#'],
        ['#', '#', '-', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['-', '-', '-', '-', '-', '-', '-'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['-', '-', '-', '-', '-', '-', '-'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '-', '-', '-', '-', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#']
    ]
    words = ["BEST", "PIP", "TRY", "UCU", "LEARN", "MORNING", "UKRAINE"]
    # Benchmark all solvers
    backtracking_time = benchmark_solver(BacktrackingSolver, grid, words, "Backtracking")
    brute_force_time = benchmark_solver(BruteForceSolver, grid, words, "Brute Force")
    greedy_time = benchmark_solver(GreedySolver, grid, words, "Greedy")

    # Compare results
    print("Execution Time Comparison:")
    print(f"Backtracking: {backtracking_time:.6f} seconds")
    print(f"Brute Force: {brute_force_time:.6f} seconds")
    print(f"Greedy: {greedy_time:.6f} seconds")
    print(f"-------------------------------------------------")
    print(f"Brute Force / Backtracking: {brute_force_time / backtracking_time *100:.2f} %")
    print(f"Greedy / Backtracking: {greedy_time / backtracking_time *100:.2f} %")
    print(f"-------------------------------------------------")
