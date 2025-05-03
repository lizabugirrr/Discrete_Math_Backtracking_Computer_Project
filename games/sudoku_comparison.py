# import time
# import matplotlib.pyplot as plt
# from sudoku import is_valid, find_empty_cell, solve_backtracking as raw_backtracking

# @benchmark
# def solve_backtracking(board):
#     raw_backtracking(board)
#     return True


# def generate_sudoku(clues=25):
#     board = [[0] * 9 for _ in range(9)]
#     solve_backtracking(board)
#     cells = [(i, j) for i in range(9) for j in range(9)]
#     random.shuffle(cells)
#     for i in range(81 - clues):
#         r, c = cells[i]
#         board[r][c] = 0
#     return board

# def benchmark(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         return result, end_time - start_time
#     return wrapper

# # DFS Solver
# @benchmark
# def solve_dfs(board):
#     empty = find_empty_cell(board)
#     if not empty:
#         return True
#     row, col = empty
#     size = len(board)
#     for num in range(1, size + 1):
#         if is_valid(board, row, col, num):
#             board[row][col] = num
#             if solve_dfs(board)[0]:
#                 return True, 0
#             board[row][col] = 0
#     return False, 0

# # MRV
# def count_valid_options(board, row, col):
#     size = len(board)
#     return sum(1 for num in range(1, size + 1) if is_valid(board, row, col, num))

# def find_empty_cell_mrv(board):
#     size = len(board)
#     min_options = size + 1
#     best_cell = None
#     for row in range(size):
#         for col in range(size):
#             if board[row][col] == 0:
#                 options = count_valid_options(board, row, col)
#                 if options < min_options:
#                     min_options = options
#                     best_cell = (row, col)
#                     if min_options == 1:
#                         return best_cell
#     return best_cell

# @benchmark
# def solve_mrv(board):
#     empty = find_empty_cell_mrv(board)
#     if not empty:
#         return True
#     row, col = empty
#     size = len(board)
#     for num in range(1, size + 1):
#         if is_valid(board, row, col, num):
#             board[row][col] = num
#             if solve_mrv(board)[0]:
#                 return True, 0
#             board[row][col] = 0
#     return False, 0


# def benchmark_solvers(sizes=[4, 9, 16], difficulties=[0.3], trials=3):
#     results = {
#         'backtracking': {size: {diff: [] for diff in difficulties} for size in sizes},
#         'dfs': {size: {diff: [] for diff in difficulties} for size in sizes},
#         'mrv': {size: {diff: [] for diff in difficulties} for size in sizes}
#     }

#     for size in sizes:
#         print(f"\nBenchmarking {size}x{size}...")
#         for diff in difficulties:
#             for _ in range(trials):
#                 puzzle = generate_sudoku(size, diff)

#                 board_bt = [row[:] for row in puzzle]
#                 board_dfs = [row[:] for row in puzzle]
#                 board_mrv = [row[:] for row in puzzle]

#                 _, time_bt = solve_backtracking(board_bt)
#                 _, time_dfs = solve_dfs(board_dfs)
#                 _, time_mrv = solve_mrv(board_mrv)

#                 results['backtracking'][size][diff].append(time_bt)
#                 results['dfs'][size][diff].append(time_dfs)
#                 results['mrv'][size][diff].append(time_mrv)
#     return results

# # Visualization functions
# def plot_size_comparison(results, difficulty=0.3):
#     plt.figure(figsize=(12, 6))

#     sizes = sorted(results['backtracking'].keys())
#     for method in results.keys():
#         avg_times = []
#         for size in sizes:
#             times = results[method][size][difficulty]
#             avg_times.append(sum(times)/len(times))

#         plt.plot(sizes, avg_times, 'o-', label=method)

#     plt.title(f'Solver Performance Comparison (Difficulty: {int(difficulty*100)}% clues)')
#     plt.xlabel('Grid Size (NxN)')
#     plt.ylabel('Average Solving Time (seconds)')
#     plt.xticks(sizes)
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# def plot_difficulty_comparison(results, size=9):
#     plt.figure(figsize=(12, 6))

#     difficulties = sorted(results['backtracking'][size].keys())
#     for method in results.keys():
#         avg_times = []
#         for diff in difficulties:
#             times = results[method][size][diff]
#             avg_times.append(sum(times)/len(times))

#         plt.plot([int(d*100) for d in difficulties], avg_times, 'o-', label=method)

#     plt.title(f'Solver Performance Comparison (Size: {size}x{size})')
#     plt.xlabel('Percentage of Clues (%)')
#     plt.ylabel('Average Solving Time (seconds)')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# if __name__ == "__main__":
#     print("Starting benchmark tests...")

#     sizes_to_test = [4, 9, 16]  # 4x4, 9x9, and 16x16 grids
#     difficulty_ratios = [0.2, 0.3, 0.4]  # 20%, 30%, 40% clues
#     trials = 3

#     results = benchmark_solvers(sizes=sizes_to_test, 
#                               difficulties=difficulty_ratios, 
#                               trials=trials)

#     # Visualize results
#     plot_size_comparison(results, difficulty=0.3)
#     plot_difficulty_comparison(results, size=9)
#     plot_difficulty_comparison(results, size=16)


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

# -------------------------
# Visualization Functions
# -------------------------
# def plot_size_comparison(results, difficulty=0.3):
#     plt.figure(figsize=(12, 6))
#     sizes = sorted(results['backtracking'].keys())
#     for method in results.keys():
#         avg_times = [sum(results[method][size][difficulty]) / len(results[method][size][difficulty]) for size in sizes]
#         plt.plot(sizes, avg_times, 'o-', label=method)

#     plt.title(f'Solver Performance by Size (Difficulty: {int(difficulty * 100)}% clues)')
#     plt.xlabel('Grid Size (NxN)')
#     plt.ylabel('Average Solving Time (seconds)')
#     plt.xticks(sizes)
#     plt.legend()
#     plt.grid(True)
#     plt.show(block=False)
#     plt.pause(1)

# def plot_difficulty_comparison(results, size=9):
#     plt.figure(figsize=(12, 6))
#     difficulties = sorted(results['backtracking'][size].keys())
#     for method in results.keys():
#         avg_times = [sum(results[method][size][diff]) / len(results[method][size][diff]) for diff in difficulties]
#         plt.plot([int(d * 100) for d in difficulties], avg_times, 'o-', label=method)

#     plt.title(f'Solver Performance by Difficulty (Size: {size}x{size})')
#     plt.xlabel('Percentage of Clues (%)')
#     plt.ylabel('Average Solving Time (seconds)')
#     plt.legend()
#     plt.grid(True)
#     plt.show(block=False)
#     plt.pause(1)

# def show_all_plots(results):
#     plot_size_comparison(results, difficulty=0.3)
#     plot_difficulty_comparison(results, size=9)
#     plot_difficulty_comparison(results, size=16)
#     input("Press Enter to close all plots...")
#     plt.close('all')

# # -------------------------
# # Entry Point
# # -------------------------
# if __name__ == "__main__":
#     print("Starting benchmark tests...")

#     sizes_to_test = [4, 9, 16]
#     difficulty_ratios = [0.2, 0.3, 0.4]
#     trials = 3

#     results = benchmark_solvers(
#         sizes=sizes_to_test,
#         difficulties=difficulty_ratios,
#         trials=trials
#     )

#     show_all_plots(results)
def show_all_plots(results):
    difficulties = sorted(next(iter(results['backtracking'].values())).keys())
    sizes = sorted(results['backtracking'].keys())

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # --- Plot 1: Size Comparison ---
    for method in results.keys():
        avg_times = [sum(results[method][size][0.3]) / len(results[method][size][0.3]) for size in sizes]
        axs[0].plot(sizes, avg_times, 'o-', label=method)
    axs[0].set_title('Performance by Grid Size\n(Difficulty = 30% clues)')
    axs[0].set_xlabel('Grid Size (NxN)')
    axs[0].set_ylabel('Time (seconds)')
    axs[0].grid(True)
    axs[0].legend()

    # --- Plot 2: Difficulty Comparison (9x9) ---
    for method in results.keys():
        avg_times = [sum(results[method][9][diff]) / len(results[method][9][diff]) for diff in difficulties]
        axs[1].plot([int(d * 100) for d in difficulties], avg_times, 'o-', label=method)
    axs[1].set_title('Performance by Difficulty\n(9x9 Grid)')
    axs[1].set_xlabel('Clues (%)')
    axs[1].set_ylabel('Time (seconds)')
    axs[1].grid(True)
    axs[1].legend()

    # --- Plot 3: Difficulty Comparison (16x16) ---
    for method in results.keys():
        avg_times = [sum(results[method][16][diff]) / len(results[method][16][diff]) for diff in difficulties]
        axs[2].plot([int(d * 100) for d in difficulties], avg_times, 'o-', label=method)
    axs[2].set_title('Performance by Difficulty\n(16x16 Grid)')
    axs[2].set_xlabel('Clues (%)')
    axs[2].set_ylabel('Time (seconds)')
    axs[2].grid(True)
    axs[2].legend()

    plt.tight_layout()
    plt.show()
    input("Press Enter to close...")

if __name__ == "__main__":
    print("Starting benchmark tests...")

    sizes_to_test = [4, 9, 16]
    difficulty_ratios = [0.2, 0.3, 0.4]
    trials = 3

    results = benchmark_solvers(sizes=sizes_to_test,
                                difficulties=difficulty_ratios,
                                trials=trials)

    show_all_plots(results)
    