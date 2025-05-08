"""
Module for comparing different N-Queens solving algorithms.
"""
import time
import random
from collections import defaultdict
from queue import Queue
import matplotlib.pyplot as plt

class NQueensComparison:
    """
    A class for comparing different N-Queens solving algorithms:
    - Backtracking (the original algorithm)
    - BFS (Breadth-First Search)
    - Greedy approach
    """
    def __init__(self):
        """
        Initialize statistics for the comparison.
        """
        self.stats = {
            'backtracking': defaultdict(dict),
            'bfs': defaultdict(dict),
            'greedy': defaultdict(dict)
        }
        for alg in self.stats:
            for metric in ['time', 'steps', 'solutions']:
                self.stats[alg][metric] = []

    def is_safe(self, board, row, col):
        """
        Checks if a queen can be placed at position (row, col).
        """
        n = len(board)
        for i in range(col):
            if board[row][i] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, n), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        return True

    def backtracking_solver(self, n, visualization_callback=None, delay=0):
        """
        Solve N-Queens using backtracking (the original algorithm).
        Returns all solutions.
        """
        solutions = []
        steps = 0
        backtracks = 0
        board = [[-1] * n for _ in range(n)]

        def backtrack(col):
            nonlocal steps, backtracks
            if col == n:
                solution = []
                for i in range(n):
                    for j in range(n):
                        if board[i][j] == 1:
                            solution.append(j)
                            break
                solutions.append(solution)
                return
            for row in range(n):
                steps += 1
                if all(board[row][c] == 0 for c in range(col)) and self.is_safe(board, row, col):
                    board[row][col] = 1
                    if visualization_callback:
                        current_state = [-1] * n
                        for r in range(n):
                            for c in range(n):
                                if board[r][c] == 1:
                                    current_state[r] = c
                        visualization_callback(current_state)
                        if delay > 0:
                            time.sleep(delay)
                    backtrack(col + 1)
                    board[row][col] = 0
                    backtracks += 1
                    if visualization_callback:
                        current_state = [-1] * n
                        for r in range(n):
                            for c in range(n):
                                if board[r][c] == 1:
                                    current_state[r] = c
                        visualization_callback(current_state)
                        if delay > 0:
                            time.sleep(delay)
        for i in range(n):
            for j in range(n):
                board[i][j] = 0
        backtrack(0)
        stats = {
            "steps": steps,
            "backtracks": backtracks,
            "solutions_count": len(solutions)
        }
        return solutions, stats

    def bfs_solver(self, n, visualization_callback=None, delay=0):
        """
        Solve N-Queens using Breadth-First Search.
        Returns all solutions found.
        """
        solutions = []
        steps = 0
        backtracks = 0
        queue = Queue()
        queue.put(([], 0))
        while not queue.empty():
            placement, row = queue.get()
            steps += 1
            if row == n:
                solutions.append(placement)
                continue
            for col in range(n):
                valid = True
                for r, c in enumerate(placement):
                    if c == col or r + c == row + col or r - c == row - col:
                        valid = False
                        backtracks += 1
                        break
                if valid:
                    new_placement = placement + [col]
                    if visualization_callback:
                        current_state = [-1] * n
                        for r, c in enumerate(new_placement):
                            current_state[r] = c
                        visualization_callback(current_state)
                        if delay > 0:
                            time.sleep(delay)
                    queue.put((new_placement, row + 1))
        stats = {
            "steps": steps,
            "backtracks": backtracks,
            "solutions_count": len(solutions)
        }
        return solutions, stats

    def greedy_solver(self, n, attempts=1000, visualization_callback=None, delay=0):
        """
        Solve N-Queens using a greedy approach.
        Tries a number of random configurations and improves them.
        Returns the best solution found or an empty list if none is found.
        """
        steps = 0
        backtracks = 0
        solutions = []
        for _ in range(attempts):
            placement = []
            failed = False
            for row in range(n):
                steps += 1
                valid_cols = []
                for col in range(n):
                    valid = True
                    for r, c in enumerate(placement):
                        if c == col or r + c == row + col or r - c == row - col:
                            valid = False
                            break
                    if valid:
                        valid_cols.append(col)
                if not valid_cols:
                    backtracks += 1
                    failed = True
                    break
                chosen_col = random.choice(valid_cols)
                placement.append(chosen_col)
                if visualization_callback:
                    current_state = [-1] * n
                    for r, c in enumerate(placement):
                        current_state[r] = c
                    visualization_callback(current_state)
                    if delay > 0:
                        time.sleep(delay)
            if not failed:
                solutions.append(placement)
                break
        stats = {
            "steps": steps,
            "backtracks": backtracks,
            "solutions_count": len(solutions)
        }
        return solutions, stats

    def benchmark_solvers(self, sizes, trials=5):
        """
        Benchmark the three algorithms across different board sizes.
        """
        results = {
            'backtracking': defaultdict(lambda: defaultdict(list)),
            'bfs': defaultdict(lambda: defaultdict(list)),
            'greedy': defaultdict(lambda: defaultdict(list))
        }
        for size in sizes:
            print(f"\nBenchmarking board size {size}x{size}...")
            for trial in range(1, trials + 1):
                print(f"  Trial {trial}/{trials}:")
                start = time.time()
                try:
                    solutions, stats = self.backtracking_solver(size)
                    solutions_count = stats["solutions_count"]
                    steps_count = stats["steps"]
                    backtracks_count = stats["backtracks"]
                except Exception as e:
                    print(f"    Backtracking failed: {e}")
                    solutions_count = 0
                    steps_count = 0
                    backtracks_count = 0
                bt_time = time.time() - start
                results['backtracking'][size]['time'].append(bt_time)
                results['backtracking'][size]['solutions'].append(solutions_count)
                results['backtracking'][size]['steps'].append(steps_count)
                results['backtracking'][size]['backtracks'].append(backtracks_count)
                print(f"    Backtracking time: {bt_time:.4f} seconds, solutions: {solutions_count}")
                if size <= 10:
                    start = time.time()
                    try:
                        solutions, stats = self.bfs_solver(size)
                        solutions_count = stats["solutions_count"]
                        steps_count = stats["steps"]
                        backtracks_count = stats["backtracks"]
                    except Exception as e:
                        print(f"    BFS failed: {e}")
                        solutions_count = 0
                        steps_count = 0
                        backtracks_count = 0
                    bfs_time = time.time() - start
                    results['bfs'][size]['time'].append(bfs_time)
                    results['bfs'][size]['solutions'].append(solutions_count)
                    results['bfs'][size]['steps'].append(steps_count)
                    results['bfs'][size]['backtracks'].append(backtracks_count)
                    print(f"    BFS time: {bfs_time:.4f} seconds, solutions: {solutions_count}")
                else:
                    print("    BFS skipped for large board size")
                    results['bfs'][size]['time'].append(None)
                    results['bfs'][size]['solutions'].append(None)
                    results['bfs'][size]['steps'].append(None)
                    results['bfs'][size]['backtracks'].append(None)
                start = time.time()
                try:
                    solutions, stats = self.greedy_solver(size)
                    solutions_count = stats["solutions_count"]
                    steps_count = stats["steps"]
                    backtracks_count = stats["backtracks"]
                except Exception as e:
                    print(f"    Greedy failed: {e}")
                    solutions_count = 0
                    steps_count = 0
                    backtracks_count = 0
                greedy_time = time.time() - start
                results['greedy'][size]['time'].append(greedy_time)
                results['greedy'][size]['solutions'].append(solutions_count)
                results['greedy'][size]['steps'].append(steps_count)
                results['greedy'][size]['backtracks'].append(backtracks_count)
                print(f"    Greedy time: {greedy_time:.4f} seconds, solutions: {solutions_count}")
        return results

    def show_all_plots(self, results):
        """
        Display plots comparing the different algorithms.
        """
        sizes = sorted([size for size in results['backtracking'].keys()])
        plt.figure(figsize=(15, 12))
        plt.subplot(2, 2, 1)
        for method in ['backtracking', 'bfs', 'greedy']:
            times = []
            valid_sizes = []
            for size in sizes:
                method_times = results[method][size]['time']
                valid_times = [t for t in method_times if t is not None]
                if valid_times:
                    times.append(sum(valid_times) / len(valid_times))
                    valid_sizes.append(size)
            if valid_sizes:
                plt.plot(valid_sizes, times, 'o-', label=method)
        plt.title('Performance by Board Size')
        plt.xlabel('Board Size (N)')
        plt.ylabel('Time (seconds)')
        plt.grid(True)
        plt.legend()
        plt.yscale('log')
        plt.subplot(2, 2, 2)
        for method in ['backtracking', 'bfs', 'greedy']:
            steps = []
            valid_sizes = []
            for size in sizes:
                method_steps = results[method][size]['steps']
                valid_steps = [s for s in method_steps if s is not None]
                if valid_steps:
                    steps.append(sum(valid_steps) / len(valid_steps))
                    valid_sizes.append(size)
            if valid_sizes:
                plt.plot(valid_sizes, steps, 'o-', label=method)
        plt.title('Steps by Board Size')
        plt.xlabel('Board Size (N)')
        plt.ylabel('Number of Steps')
        plt.grid(True)
        plt.legend()
        plt.yscale('log')
        plt.tight_layout()
        plt.savefig('nqueens_benchmark.png', dpi=300, bbox_inches='tight')
        plt.show()

def run_benchmark():
    """
    Run the benchmark and display results.
    """
    print("Starting N-Queens algorithm comparison...")
    comparison = NQueensComparison()
    sizes_to_test = [4, 5, 6, 7, 8, 9, 10]
    trials = 3
    results = comparison.benchmark_solvers(
        sizes=sizes_to_test,
        trials=trials
    )
    comparison.show_all_plots(results)

if __name__ == "__main__":
    run_benchmark()
