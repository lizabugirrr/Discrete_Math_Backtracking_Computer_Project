import time
import random
import matplotlib.pyplot as plt
from sudoku import is_valid, find_empty_cell, solve_backtracking as raw_backtracking


def benchmark(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, end_time - start_time
    return wrapper


@benchmark
def solve_backtracking(board):
    raw_backtracking(board)
    return True


@benchmark
def solve_dfs(board):
    empty = find_empty_cell(board)
    if not empty:
        return True
    row, col = empty
    size = len(board)
    for num in range(1, size + 1):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_dfs(board)[0]:
                return True, 0
            board[row][col] = 0
    return False, 0


def count_valid_options(board, row, col):
    size = len(board)
    return sum(1 for num in range(1, size + 1) if is_valid(board, row, col, num))

def find_empty_cell_mrv(board):
    size = len(board)
    min_options = size + 1
    best_cell = None
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                options = count_valid_options(board, row, col)
                if options < min_options:
                    min_options = options
                    best_cell = (row, col)
                    if min_options == 1:
                        return best_cell
    return best_cell

@benchmark
def solve_mrv(board):
    empty = find_empty_cell_mrv(board)
    if not empty:
        return True
    row, col = empty
    size = len(board)
    for num in range(1, size + 1):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_mrv(board)[0]:
                return True, 0
            board[row][col] = 0
    return False, 0


def generate_sudoku(size=9, difficulty=0.3):
    board = [[0] * size for _ in range(size)]
    raw_backtracking(board)
    cells = [(i, j) for i in range(size) for j in range(size)]
    random.shuffle(cells)
    clues = int(size * size * difficulty)
    for i in range(size * size - clues):
        r, c = cells[i]
        board[r][c] = 0
    return board


def benchmark_solvers(sizes=[4, 9, 16], difficulties=[0.3], trials=3):
    results = {
        'backtracking': {size: {diff: [] for diff in difficulties} for size in sizes},
        'dfs': {size: {diff: [] for diff in difficulties} for size in sizes},
        'mrv': {size: {diff: [] for diff in difficulties} for size in sizes}
    }

    for size in sizes:
        print(f"\nBenchmarking {size}x{size}...")
        for diff in difficulties:
            for _ in range(trials):
                puzzle = generate_sudoku(size, diff)

                board_bt = [row[:] for row in puzzle]
                board_dfs = [row[:] for row in puzzle]
                board_mrv = [row[:] for row in puzzle]

                _, time_bt = solve_backtracking(board_bt)
                _, time_dfs = solve_dfs(board_dfs)
                _, time_mrv = solve_mrv(board_mrv)

                results['backtracking'][size][diff].append(time_bt)
                results['dfs'][size][diff].append(time_dfs)
                results['mrv'][size][diff].append(time_mrv)
    return results

# def show_all_plots(results):
#     difficulties = sorted(next(iter(results['backtracking'].values())).keys())
#     sizes = sorted(results['backtracking'].keys())

#     fig, axs = plt.subplots(1, 3, figsize=(18, 5))

#     # Size Comparison
#     for method in results.keys():
#         avg_times = [sum(results[method][size][0.3]) / len(results[method][size][0.3]) for size in sizes]
#         axs[0].plot(sizes, avg_times, 'o-', label=method)
#     axs[0].set_title('Performance by Grid Size\n(Difficulty = 30% clues)')
#     axs[0].set_xlabel('Grid Size (NxN)')
#     axs[0].set_ylabel('Time (seconds)')
#     axs[0].grid(True)
#     axs[0].legend()

#     # Difficulty Comparison (9x9)
#     for method in results.keys():
#         avg_times = [sum(results[method][9][diff]) / len(results[method][9][diff]) for diff in difficulties]
#         axs[1].plot([int(d * 100) for d in difficulties], avg_times, 'o-', label=method)
#     axs[1].set_title('Performance by Difficulty\n(9x9 Grid)')
#     axs[1].set_xlabel('Clues (%)')
#     axs[1].set_ylabel('Time (seconds)')
#     axs[1].grid(True)
#     axs[1].legend()

#     # Difficulty Comparison (16x16)
#     for method in results.keys():
#         avg_times = [sum(results[method][16][diff]) / len(results[method][16][diff]) for diff in difficulties]
#         axs[2].plot([int(d * 100) for d in difficulties], avg_times, 'o-', label=method)
#     axs[2].set_title('Performance by Difficulty\n(16x16 Grid)')
#     axs[2].set_xlabel('Clues (%)')
#     axs[2].set_ylabel('Time (seconds)')
#     axs[2].grid(True)
#     axs[2].legend()

#     plt.tight_layout()
#     plt.show()
#     input("Press Enter to close...")

# if __name__ == "__main__":
#     print("Starting benchmark tests...")

#     sizes_to_test = [4, 9, 16]
#     difficulty_ratios = [0.2, 0.3, 0.4]
#     trials = 3

#     results = benchmark_solvers(sizes=sizes_to_test,
#                                 difficulties=difficulty_ratios,
#                                 trials=trials)

#     show_all_plots(results)


sizes = [9, 36]  # 9x9 and 36x36 boards
difficulties = [0.3, 0.05]  # Easy (~30% clues), Hard (~5% clues)
trials = 3

# Averaging helper
def average(times):
    return sum(times) / len(times)

# Plot 1: Difficulty comparison (easiest vs hardest) on 9x9
def plot_difficulty_comparison(results):
    easy = difficulties[0]
    hard = difficulties[1]
    size = 9
    plt.figure(figsize=(8, 5))
    
    for method in results:
        times_easy = average(results[method][size][easy])
        times_hard = average(results[method][size][hard])
        plt.bar([f'{method} (easy)', f'{method} (hard)'], [times_easy, times_hard])

    plt.title("Solver Time vs Difficulty (9x9 Sudoku)")
    plt.ylabel("Time (seconds)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

# Plot 2: Size comparison (9x9 vs 36x36) at difficulty 0.3
def plot_size_comparison(results):
    diff = 0.3
    plt.figure(figsize=(8, 5))
    
    for method in results:
        t_9x9 = average(results[method][9][diff])
        t_36x36 = average(results[method][36][diff])
        plt.bar([f'{method} (9x9)', f'{method} (36x36)'], [t_9x9, t_36x36])

    plt.title("Solver Time vs Board Size (Difficulty 30%)")
    plt.ylabel("Time (seconds)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

# Plot 3: Comparison across solvers for hardest 9x9
def plot_solver_comparison_hard(results):
    diff = 0.05
    size = 9
    plt.figure(figsize=(8, 5))
    methods = list(results.keys())
    times = [average(results[method][size][diff]) for method in methods]
    
    plt.bar(methods, times, color=['blue', 'orange', 'green'])
    plt.title("Solver Performance on Hard 9x9 Sudoku (5% clues)")
    plt.ylabel("Time (seconds)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

# Plot 4: Comparison across solvers for large board (36x36)
def plot_solver_comparison_large(results):
    diff = 0.3
    size = 36
    plt.figure(figsize=(8, 5))
    methods = list(results.keys())
    times = [average(results[method][size][diff]) for method in methods]
    
    plt.bar(methods, times, color=['blue', 'orange', 'green'])
    plt.title("Solver Performance on Large 36x36 Sudoku")
    plt.ylabel("Time (seconds)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    results = benchmark_solvers(sizes=sizes, difficulties=difficulties, trials=trials)

    plot_difficulty_comparison(results)
    plot_size_comparison(results)
    plot_solver_comparison_hard(results)
    plot_solver_comparison_large(results)

