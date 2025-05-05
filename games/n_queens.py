"""
A module for solving the N-Queens problem using backtracking algorithm with console
interface.
"""
import time
import argparse
import threading
import tkinter as tk
from tkinter import ttk, messagebox
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
        self.visualization_callback = None
        self.delay = 0.1  # Delay for visualization (seconds)

    def solve(self, n, visualization_callback=None, delay=0.1):
        """
        Solves the N-Queens problem for a board of size n x n.
        """
        self.solutions = []
        self.steps_count = 0
        self.backtracks_count = 0
        self.visualization_callback = visualization_callback
        self.delay = delay
        board = [-1] * n
        self.current_state = board[:]
        if self.visualization_callback:
            self.visualization_callback(self.current_state)
            time.sleep(self.delay)
        self._backtrack(board, 0, n)
        return self.solutions

    def _backtrack(self, board, row, n):
        """
        Recursive backtracking function to find solutions.
        """
        if row == n:
            self.solutions.append(board[:])
            return
        for col in range(n):
            self.steps_count += 1
            if self._is_safe(board, row, col):
                board[row] = col
                self.current_state = board[:]
                if self.visualization_callback:
                    self.visualization_callback(self.current_state)
                    time.sleep(self.delay)
                self._backtrack(board, row + 1, n)
                board[row] = -1
                self.current_state = board[:]
                self.backtracks_count += 1
                if self.visualization_callback:
                    self.visualization_callback(self.current_state)
                    time.sleep(self.delay)

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


class VisualNQueens:
    """
    Graphical interface for solving the N-Queens problem.
    """
    def __init__(self, root):
        """
        Initializing variables.
        """
        self.root = root
        self.root.title("N-Queens Solver")
        self.root.geometry("800x600")
        self.solver = NQueensSolver()
        self.solutions = []
        self.current_solution_index = 0
        self.board_size = 8
        self.animation_speed = 100
        self.is_solving = False
        self._create_widgets()

    def _create_widgets(self):
        """
        Creates widgets for the graphical interface.
        """
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill='x')
        board_frame = ttk.Frame(self.root, padding="10")
        board_frame.pack(fill='both', expand=True)
        ttk.Label(control_frame, text="Board Size:").grid(row=0, column=0, padx=5, pady=5)
        self.size_var = tk.StringVar(value=str(self.board_size))
        size_combo = ttk.Combobox(control_frame, textvariable=self.size_var, width=5,
values=[str(i) for i in range(4, 21)])
        size_combo.grid(row=0, column=1, padx=5, pady=5)
        size_combo.bind("<<ComboboxSelected>>", self._on_size_change)
        ttk.Label(control_frame, text="Animation Speed:").grid(row=0, column=2, padx=5, pady=5)
        self.speed_var = tk.StringVar(value="Medium")
        speed_combo = ttk.Combobox(control_frame, textvariable=self.speed_var, width=10,
values=["Slow", "Medium", "Fast", "Very Fast"])
        speed_combo.grid(row=0, column=3, padx=5, pady=5)
        speed_combo.bind("<<ComboboxSelected>>", self._on_speed_change)
        self.solve_button = ttk.Button(control_frame, text="Solve", command=self._solve)
        self.solve_button.grid(row=0, column=4, padx=5, pady=5)
        self.stop_button = ttk.Button(control_frame, text="Stop", command=self._stop,
state=tk.DISABLED)
        self.stop_button.grid(row=0, column=5, padx=5, pady=5)
        self.nav_frame = ttk.Frame(control_frame)
        self.nav_frame.grid(row=1, column=0, columnspan=6, padx=5, pady=5)
        self.prev_button = ttk.Button(self.nav_frame, text="< Previous",
command=self._prev_solution, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.solution_label = ttk.Label(self.nav_frame, text="Solution: 0/0")
        self.solution_label.pack(side=tk.LEFT, padx=20)
        self.next_button = ttk.Button(self.nav_frame, text="Next >", command=self._next_solution,
state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.root, textvariable=self.status_var,
relief="sunken", anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        self.stats_frame = ttk.LabelFrame(control_frame, text="Statistics", padding="5")
        self.stats_frame.grid(row=2, column=0, columnspan=6, padx=5, pady=5, sticky="ew")
        self.steps_var = tk.StringVar(value="Steps: 0")
        ttk.Label(self.stats_frame, textvariable=self.steps_var).pack(side=tk.LEFT, padx=10)
        self.backtracks_var = tk.StringVar(value="Backtracks: 0")
        ttk.Label(self.stats_frame, textvariable=self.backtracks_var).pack(side=tk.LEFT, padx=10)
        self.time_var = tk.StringVar(value="Time: 0.0000 sec")
        ttk.Label(self.stats_frame, textvariable=self.time_var).pack(side=tk.LEFT, padx=10)
        self.canvas = tk.Canvas(board_frame, background="white")
        self.canvas.pack(fill='both', expand=True)
        self._draw_empty_board()

    def _on_size_change(self, event=None):
        """
        Handles changes to the chessboard size.
        """
        try:
            self.board_size = int(self.size_var.get())
            self._draw_empty_board()
            self._reset_solution_navigation()
        except ValueError:
            messagebox.showerror("Error", "Invalid board size")

    def _on_speed_change(self, event=None):
        """
        Handles changes to the animation speed.
        """
        speed = self.speed_var.get()
        if speed == "Slow":
            self.animation_speed = 500
        elif speed == "Medium":
            self.animation_speed = 100
        elif speed == "Fast":
            self.animation_speed = 20
        else:  # Very Fast
            self.animation_speed = 1

    def _reset_solution_navigation(self):
        """
        Resets solution navigation.
        """
        self.solutions = []
        self.current_solution_index = 0
        self.solution_label.config(text="Solution: 0/0")
        self.prev_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)

    def _draw_empty_board(self):
        """
        Draws an empty chessboard.
        """
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        cell_size = min(width, height) // self.board_size
        offset_x = (width - cell_size * self.board_size) // 2
        offset_y = (height - cell_size * self.board_size) // 2
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = offset_x + col * cell_size
                y1 = offset_y + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def _draw_board(self, board):
        """
        Draws a chessboard with queens.
        """
        self._draw_empty_board()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        cell_size = min(width, height) // self.board_size
        offset_x = (width - cell_size * self.board_size) // 2
        offset_y = (height - cell_size * self.board_size) // 2
        for row in range(len(board)):
            col = board[row]
            if col != -1:
                x = offset_x + col * cell_size + cell_size / 2
                y = offset_y + row * cell_size + cell_size / 2
                queen_size = cell_size * 0.8
                self.canvas.create_oval(
                    x - queen_size/2, y - queen_size/2,
                    x + queen_size/2, y + queen_size/2,
                    fill="#e63946", outline="black", width=2)
                self.canvas.create_text(
                    x, y, text="♛", fill="white", font=("Arial", int(queen_size * 0.6)))

    def _solve(self):
        """
        Starts solving the problem.
        """
        if self.is_solving:
            return
        self.is_solving = True
        self.solve_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self._reset_solution_navigation()
        self.solve_thread = threading.Thread(target=self._solve_thread)
        self.solve_thread.daemon = True
        self.solve_thread.start()

    def _solve_thread(self):
        """
        Function to execute in a separate thread.
        """
        try:
            self.status_var.set("Solving the problem...")
            delay = self.animation_speed / 1000
            start_time = time.time()
            self.solutions = self.solver.solve(self.board_size, self._update_board, delay)
            end_time = time.time()
            if not self.is_solving:
                return
            stats = self.solver.get_statistics()
            self.steps_var.set(f"Steps: {stats['steps']}")
            self.backtracks_var.set(f"Backtracks: {stats['backtracks']}")
            self.time_var.set(f"Time: {end_time - start_time:.4f} sec")
            self.status_var.set(f"Found {len(self.solutions)} solutions")
            if self.solutions:
                self.current_solution_index = 0
                self.solution_label.config(text=f"Solution: 1/{len(self.solutions)}")
                self._draw_board(self.solutions[0])
                if len(self.solutions) > 1:
                    self.next_button.config(state=tk.NORMAL)
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
        finally:
            self.is_solving = False
            self.root.after(0, lambda: self.solve_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))

    def _update_board(self, board):
        """
        Updates the chessboard display during animation.
        """
        if not self.is_solving:
            return
        self.root.after(0, lambda b=board[:]: self._draw_board(b))

    def _stop(self):
        """
        Stops solving.
        """
        self.is_solving = False
        self.status_var.set("Stopped by user")

    def _prev_solution(self):
        """
        Shows the previous solution.
        """
        if self.solutions and self.current_solution_index > 0:
            self.current_solution_index -= 1
            self._draw_board(self.solutions[self.current_solution_index])
            self.solution_label.config(text=
f"Solution: {self.current_solution_index+1}/{len(self.solutions)}")
            self.next_button.config(state=tk.NORMAL)
            if self.current_solution_index == 0:
                self.prev_button.config(state=tk.DISABLED)

    def _next_solution(self):
        """
        Shows the next solution.
        """
        if self.solutions and self.current_solution_index < len(self.solutions) - 1:
            self.current_solution_index += 1
            self._draw_board(self.solutions[self.current_solution_index])
            self.solution_label.config(text=
f"Solution: {self.current_solution_index+1}/{len(self.solutions)}")
            self.prev_button.config(state=tk.NORMAL)
            if self.current_solution_index == len(self.solutions) - 1:
                self.next_button.config(state=tk.DISABLED)

def run_console_version():
    """
    Runs the console version of the application.
    """
    console_app = ConsoleNQueens()
    console_app.run()

def run_visual_version():
    """
    Runs the visual version of the application.
    """
    root = tk.Tk()
    app = VisualNQueens(root)
    def on_closing():
        app.is_solving = False
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    def on_resize(event):
        if event.widget == root:
            app._draw_board([-1] * app.board_size)
    root.bind("<Configure>", on_resize)
    root.mainloop()

def run_pygame_version():
    """
    Runs the Pygame version of the application.
    """
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='N-Queens Solver')
    parser.add_argument('mode', choices=['console', 'visual'], help='Display mode')
    args = parser.parse_args()

    if args.mode == 'console':
        run_console_version()
    elif args.mode == 'visual':
        run_visual_version()
    else:
        run_pygame_version()
