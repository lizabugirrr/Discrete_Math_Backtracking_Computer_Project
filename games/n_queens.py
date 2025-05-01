"""
A module for solving the N-Queens problem using backtracking algorithm with console
interface.
"""
import time
import argparse
import pygame

class NQueensSolver:
    """
    A class that solves the N-Queens problem using backtracking algorithm.
    Finds all possible solutions for placing N queens on an NxN chessboard
    where no two queens threaten each other.
    """
    def __init__(self):
        """
        Initializing variables.
        """
        self.solutions = []
        self.steps_count = 0
        self.backtracks_count = 0
        self.current_state = None

    def solve(self, n):
        """
        Solves the N-Queens problem for a board of size n x n.
        """
        self.solutions = []
        self.steps_count = 0
        self.backtracks_count = 0
        board = [-1] * n
        self.current_state = board[:]
        self._backtrack(board, 0, n)
        return self.solutions

    def _backtrack(self, board, row, n):
        """
        Recursive backtracking function to find solutions.
        """
        if row == n:
            self.solutions.append(board[:])
        for col in range(n):
            self.steps_count += 1
            if self._is_safe(board, row, col):
                board[row] = col
                self.current_state = board[:]
                self._backtrack(board, row + 1, n)
                board[row] = -1
                self.current_state = board[:]
                self.backtracks_count += 1

    def _is_safe(self, board, row, col):
        """
        Checks if a queen can be placed at position (row, col).
        """
        for i in range(row):
            if board[i] == col:
                return False
            if abs(board[i] - col) == abs(i - row):
                return False
        return True

    def get_statistics(self):
        """
        Returns statistics of the algorithm execution.
        """
        return {
            "steps": self.steps_count,
            "backtracks": self.backtracks_count,
            "solutions_count": len(self.solutions)
        }

    def print_solution(self, solution):
        """
        Prints a solution as a chessboard in the console.
        """
        n = len(solution)
        print("+" + "-" * (2 * n + 1) + "+")
        for row in range(n):
            line = "| "
            for col in range(n):
                if solution[row] == col:
                    line += "Q "
                else:
                    line += ". "
            line += "|"
            print(line)
        print("+" + "-" * (2 * n + 1) + "+")

class ConsoleNQueens:
    """
    Console interface for solving the N-Queens problem.
    """

    def __init__(self):
        """
        Initializing variables.
        """
        self.solver = NQueensSolver()

    def run(self):
        """
        Runs the console interface.
        """
        print("\n=== N-Queens Problem Solver ===\n")
        while True:
            try:
                n = int(input("Enter chessboard size (n) or 0 to exit: "))
                if n == 0:
                    print("Thank you for using the program!")
                    break
                elif n < 4:
                    print("Chessboard size must be at least 4.")
                    continue
                print(f"\nSolving for n = {n}...")
                start_time = time.time()
                solutions = self.solver.solve(n)
                end_time = time.time()
                stats = self.solver.get_statistics()
                print(f"\nFound {len(solutions)} solutions.")
                print(f"Execution time: {end_time - start_time:.4f} seconds")
                print(f"Number of steps: {stats['steps']}")
                print(f"Number of backtracks: {stats['backtracks']}")
                if solutions:
                    while True:
                        choice = input("\nShow solutions? (y/n): ").lower()
                        if choice == "y":
                            how_many = input("How many solutions to show? (all/number): ")
                            if how_many.lower() == "all":
                                limit = len(solutions)
                            else:
                                try:
                                    limit = min(int(how_many), len(solutions))
                                except ValueError:
                                    print("Invalid value. Showing the first solution.")
                                    limit = 1
                            for i in range(limit):
                                print(f"\nSolution #{i+1}:")
                                self.solver.print_solution(solutions[i])
                            break
                        elif choice == "n":
                            break
                        else:
                            print("Please enter 'y' or 'n'.")
                print("\n" + "-" * 50 + "\n")
            except ValueError:
                print("Please enter a valid integer.")
            except KeyboardInterrupt:
                print("\nProgram terminated by user.")
                break


def run_console_version():
    console_app = ConsoleNQueens()
    console_app.run()

def run_pygame_version():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='N-Queens Solver')
    parser.add_argument('mode', choices=['console', 'visual'], help='Display mode')
    args = parser.parse_args()

    if args.mode == 'console':
        run_console_version()
    else:
        run_pygame_version()
