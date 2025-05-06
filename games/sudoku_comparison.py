# import time
# import random
# import matplotlib.pyplot as plt
# from sudoku import is_valid, find_empty_cell
# import timeit
# import math
# from copy import deepcopy

# def raw_backtracking(board):
#     empty = find_empty_cell(board)
#     if not empty:
#         return True
#     row, col = empty
#     for num in range(1, len(board) + 1):
#         if is_valid(board, row, col, num):
#             board[row][col] = num
#             if raw_backtracking(board):
#                 return True
#             board[row][col] = 0
#     return False

# def benchmark(func):
#     def wrapper(*args, **kwargs):
#         for _ in range(2):
#             func(*args, **kwargs)
#         start_time = timeit.default_timer()
#         result = func(*args, **kwargs)
#         end_time = timeit.default_timer()
#         return result, end_time - start_time
#     return wrapper

# @benchmark
# def solve_backtracking(board):
#     board_copy = [row[:] for row in board]
#     success = raw_backtracking(board_copy)
#     return board_copy if success else None

# @benchmark
# def solve_dfs(board):
#     board_copy = [row[:] for row in board]
#     def dfs_helper(board):
#         empty = find_empty_cell(board)
#         if not empty:
#             return True
#         row, col = empty
#         for num in range(1, len(board)+1):
#             if is_valid(board, row, col, num):
#                 board[row][col] = num
#                 if dfs_helper(board):
#                     return True
#                 board[row][col] = 0
#         return False
#     success = dfs_helper(board_copy)
#     return board_copy if success else None

# @benchmark
# def solve_mrv(board):
#     board_copy = [row[:] for row in board]
#     size = len(board)
#     subgrid_size = int(size ** 0.5)

#     all_peers = {}
#     for r in range(size):
#         for c in range(size):
#             peers = set()
#             for i in range(size):
#                 if i != c: 
#                     peers.add((r, i))
#                 if i != r: 
#                     peers.add((i, c))
#             br, bc = r // subgrid_size, c // subgrid_size
#             for i in range(br * subgrid_size, (br + 1) * subgrid_size):
#                 for j in range(bc * subgrid_size, (bc + 1) * subgrid_size):
#                     if i != r or j != c:
#                         peers.add((i, j))
#             all_peers[(r, c)] = peers

#     domains = {}
#     for r in range(size):
#         for c in range(size):
#             if board_copy[r][c] == 0:
#                 domains[(r, c)] = set(range(1, size + 1))

#     for r in range(size):
#         for c in range(size):
#             val = board_copy[r][c]
#             if val != 0:
#                 for peer in all_peers[(r, c)]:
#                     if peer in domains and val in domains[peer]:
#                         domains[peer].remove(val)

#     def mrv_helper(domains):
#         if not domains:
#             return True

#         cell = min(domains.items(), key=lambda x: len(x[1]))[0]
#         r, c = cell
#         values = list(domains[cell])

#         for val in values:
#             board_copy[r][c] = val
#             new_domains = {}
#             conflict = False

#             for peer in all_peers[(r, c)]:
#                 if peer in domains and val in domains[peer]:
#                     if peer not in new_domains:
#                         new_domains[peer] = domains[peer].copy()
#                     new_domains[peer].remove(val)
#                     if not new_domains[peer]:
#                         conflict = True
#                         break

#             if not conflict:
#                 for other_cell in domains:
#                     if other_cell not in new_domains and other_cell != cell:
#                         new_domains[other_cell] = domains[other_cell]

#                 if mrv_helper(new_domains):
#                     return True

#             board_copy[r][c] = 0

#         return False

#     success = mrv_helper(domains)
#     return board_copy if success else None

# def generate_sudoku(size=9, clues=30):
#     board = [[0]*size for _ in range(size)]
#     raw_backtracking([row[:] for row in board])

#     cells = [(i,j) for i in range(size) for j in range(size)]
#     random.shuffle(cells)
#     for i in range(size*size - clues):
#         r,c = cells[i]
#         board[r][c] = 0
#     return board




# def verify_solution(board):
#     if board is None:
#         return False

#     size = len(board)
#     for r in range(size):
#         row_nums = set()
#         col_nums = set()
#         for c in range(size):
#             if board[r][c] == 0 or board[r][c] > size:
#                 return False
#             row_nums.add(board[r][c])
#             col_nums.add(board[c][r])
#         if len(row_nums) != size or len(col_nums) != size:
#             return False

#     subgrid_size = int(size ** 0.5)
#     for br in range(subgrid_size):
#         for bc in range(subgrid_size):
#             nums = set()
#             for r in range(br*subgrid_size, (br+1)*subgrid_size):
#                 for c in range(bc*subgrid_size, (bc+1)*subgrid_size):
#                     nums.add(board[r][c])
#             if len(nums) != size:
#                 return False
#     return True

# def benchmark_solvers(sizes=[9, 16], trials=10):
#     results = {
#         'backtracking': {},
#         'dfs': {},
#         'mrv': {}
#     }

    # for size in sizes:
    #     if size == 9:
    #         clue_counts = [20, 30, 40]
    #     elif size == 16:
    #         clue_counts = [100, 110, 120, 130]
    #     else:
    #         print(f"Skipping unsupported size: {size}")
    #         continue

#         results['backtracking'][size] = {clues: [] for clues in clue_counts}
#         results['dfs'][size] = {clues: [] for clues in clue_counts}
#         results['mrv'][size] = {clues: [] for clues in clue_counts}

#         print(f"\nBenchmarking {size}x{size}...")
#         for clues in clue_counts:
#             print(f"  Testing with {clues} clues...")
#             for t in range(trials):
#                 puzzle = generate_sudoku(size=size, clues=clues)

#                 solution_bt, time_bt = solve_backtracking(deepcopy(puzzle))
#                 solution_dfs, time_dfs = solve_dfs(deepcopy(puzzle))
#                 solution_mrv, time_mrv = solve_mrv(deepcopy(puzzle))

#                 valid = all([
#                     verify_solution(solution_bt),
#                     verify_solution(solution_dfs),
#                     verify_solution(solution_mrv)
#                 ])

#                 if valid:
#                     results['backtracking'][size][clues].append(time_bt)
#                     results['dfs'][size][clues].append(time_dfs)
#                     results['mrv'][size][clues].append(time_mrv)
#                     print(f"    Trial {t+1}/{trials}: BT={time_bt:.6f}s, DFS={time_dfs:.6f}s, MRV={time_mrv:.6f}s")
#                 else:
#                     print(f"    Trial {t+1}/{trials}: Skipped due to solver failure")

#     return results


# # def show_all_plots(results):
# #     clue_counts = sorted(next(iter(results['backtracking'].values())).keys())
# #     sizes = sorted(results['backtracking'].keys())

# #     plt.figure(figsize=(15, 12))
    
# #     # Plot 1: Performance by Grid Size (30 clues)
# #     plt.subplot(2, 2, 1)
# #     for method in results.keys():
# #         avg_times = [sum(results[method][size][40])/len(results[method][size][40]) for size in sizes]
# #         plt.plot(sizes, avg_times, 'o-', label=method)
# #     plt.title('Performance by Grid Size (30 Clues)')
# #     plt.xlabel('Grid Size')
# #     plt.ylabel('Time (seconds)')
# #     plt.grid(True)
# #     plt.legend()
# #     plt.yscale('log')

# #     # Plot 2: Performance by Grid Size (20 clues)
# #     plt.subplot(2, 2, 2)
# #     for method in results.keys():
# #         avg_times = [sum(results[method][size][20])/len(results[method][size][20]) for size in sizes]
# #         plt.plot(sizes, avg_times, 'o-', label=method)
# #     plt.title('Performance by Grid Size (20 Clues)')
# #     plt.xlabel('Grid Size')
# #     plt.ylabel('Time (seconds)')
# #     plt.grid(True)
# #     plt.legend()
# #     plt.yscale('log')

# #     # Plot 3: Performance by Clue Count (16x16)
# #     plt.subplot(2, 2, 3)
# #     for method in results.keys():
# #         avg_times = [sum(results[method][9][clues])/len(results[method][9][clues]) for clues in clue_counts]
# #         plt.plot(clue_counts, avg_times, 'o-', label=method)
# #     plt.title('Performance by Clue Count (9x9 Grid)')
# #     plt.xlabel('Number of Clues')
# #     plt.ylabel('Time (seconds)')
# #     plt.grid(True)
# #     plt.legend()
# #     plt.yscale('log')

# #     # Plot 4: Performance by Clue Count (25x25)
# #     plt.subplot(2, 2, 4)
# #     for method in results.keys():
# #         avg_times = [sum(results[method][16][clues])/len(results[method][16][clues]) for clues in clue_counts]
# #         plt.plot(clue_counts, avg_times, 'o-', label=method)
# #     plt.title('Performance by Clue Count (16x16 Grid)')
# #     plt.xlabel('Number of Clues')
# #     plt.ylabel('Time (seconds)')
# #     plt.grid(True)
# #     plt.legend()
# #     plt.yscale('log')

# #     plt.tight_layout()
# #     plt.savefig('sudoku_benchmark.png', dpi=300, bbox_inches='tight')
# #     plt.show()

# # if __name__ == "__main__":
# #     print("Starting benchmark tests...")

# #     sizes_to_test = [9, 16]
# #     trials = 10

# #     results = benchmark_solvers(
# #         sizes=sizes_to_test,
# #         trials=trials
# #     )

# #     show_all_plots(results)

# def show_all_plots(results):
#     sizes = sorted(results['backtracking'].keys())
    
#     plt.figure(figsize=(15, 12))
    
#     # Plot 1: Performance by Grid Size (for each method's most common clue count)
#     plt.subplot(2, 2, 1)
#     for method in results.keys():
#         avg_times = []
#         for size in sizes:
#             # Get the middle clue count for this size
#             clues = sorted(results[method][size].keys())[len(results[method][size])//2]
#             times = results[method][size][clues]
#             avg_times.append(sum(times)/len(times))
#         plt.plot(sizes, avg_times, 'o-', label=method)
#     plt.title('Performance by Grid Size (Middle Clue Count)')
#     plt.xlabel('Grid Size')
#     plt.ylabel('Time (seconds)')
#     plt.grid(True)
#     plt.legend()
#     plt.yscale('log')

#     # Plot 2: Performance by Clue Count (9x9)
#     plt.subplot(2, 2, 2)
#     if 9 in sizes:
#         clue_counts = sorted(results['backtracking'][9].keys())
#         for method in results.keys():
#             avg_times = [sum(results[method][9][clues])/len(results[method][9][clues]) for clues in clue_counts]
#             plt.plot(clue_counts, avg_times, 'o-', label=method)
#         plt.title('Performance by Clue Count (9x9 Grid)')
#         plt.xlabel('Number of Clues')
#         plt.ylabel('Time (seconds)')
#         plt.grid(True)
#         plt.legend()
#         plt.yscale('log')

#     # Plot 3: Performance by Clue Count (16x16)
#     plt.subplot(2, 2, 3)
#     if 16 in sizes:
#         clue_counts = sorted(results['backtracking'][16].keys())
#         for method in results.keys():
#             avg_times = [sum(results[method][16][clues])/len(results[method][16][clues]) for clues in clue_counts]
#             plt.plot(clue_counts, avg_times, 'o-', label=method)
#         plt.title('Performance by Clue Count (16x16 Grid)')
#         plt.xlabel('Number of Clues')
#         plt.ylabel('Time (seconds)')
#         plt.grid(True)
#         plt.legend()
#         plt.yscale('log')

#     plt.tight_layout()
#     plt.savefig('sudoku_benchmark.png', dpi=300, bbox_inches='tight')
#     plt.show()
# if __name__ == "__main__":
#     print("Starting benchmark tests...")

#     sizes_to_test = [9, 16]
#     trials = 10

#     results = benchmark_solvers(
#         sizes=sizes_to_test,
#         trials=trials
#     )
#     show_all_plots(results)







# import time
# import math
# import random
# import matplotlib.pyplot as plt
# import copy

# def is_valid(board, row, col, num):
#     size = len(board)
#     subgrid_size = int(math.sqrt(size))

#     for i in range(size):
#         if num in (board[row][i], board[i][col]):
#             return False

#     row_start = (row // subgrid_size) * subgrid_size
#     col_start = (col // subgrid_size) * subgrid_size

#     for i in range(row_start, row_start + subgrid_size):
#         for j in range(col_start, col_start + subgrid_size):
#             if board[i][j] == num:
#                 return False
#     return True

# def find_empty_cell(board):
#     size = len(board)
#     for row in range(size):
#         for col in range(size):
#             if board[row][col] == 0:
#                 return row, col
#     return None

# # Backtracking implementation
# def backtracking_solver(board):
#     empty = find_empty_cell(board)
#     if not empty:
#         return True
#     row, col = empty
    
#     size = len(board)
#     for num in range(1, size + 1):
#         if is_valid(board, row, col, num):
#             board[row][col] = num
#             if backtracking_solver(board):
#                 return True
#             board[row][col] = 0
#     return False

# # DFS implementation (very similar to backtracking in this context)
# def dfs_solver(board):
#     empty = find_empty_cell(board)
#     if not empty:
#         return True
#     row, col = empty
    
#     size = len(board)
#     for num in range(1, size + 1):
#         if is_valid(board, row, col, num):
#             board[row][col] = num
#             if dfs_solver(board):
#                 return True
#             board[row][col] = 0
#     return False

# # Greedy MRV (Minimum Remaining Values) implementation
# def greedy_mrv_solver(board):
#     def get_mrv_cell(board):
#         size = len(board)
#         min_options = size + 1
#         mrv_cell = None
#         options_for_cell = {}
        
#         for row in range(size):
#             for col in range(size):
#                 if board[row][col] == 0:
#                     options = []
#                     for num in range(1, size + 1):
#                         if is_valid(board, row, col, num):
#                             options.append(num)
#                     if len(options) < min_options:
#                         min_options = len(options)
#                         mrv_cell = (row, col)
#                         options_for_cell[(row, col)] = options
#                         if min_options == 1:  # Can't get better than this
#                             return mrv_cell, options_for_cell[mrv_cell]
#         return mrv_cell, options_for_cell.get(mrv_cell, [])
    
#     mrv_cell, options = get_mrv_cell(board)
#     if not mrv_cell:
#         return True
#     row, col = mrv_cell
    
#     for num in options:
#         board[row][col] = num
#         if greedy_mrv_solver(board):
#             return True
#         board[row][col] = 0
#     return False

# # Helper functions for testing
# def generate_sudoku(size, clues):
#     board = [[0 for _ in range(size)] for _ in range(size)]
#     subgrid_size = int(math.sqrt(size))
    
#     # Fill diagonal subgrids
#     for box in range(0, size, subgrid_size):
#         nums = list(range(1, size + 1))
#         random.shuffle(nums)
#         for i in range(subgrid_size):
#             for j in range(subgrid_size):
#                 board[box + i][box + j] = nums.pop()
    
#     # Solve the complete board
#     solver = greedy_mrv_solver if size > 9 else backtracking_solver
#     solver(copy.deepcopy(board))
    
#     # Remove numbers to leave only 'clues' number of cells filled
#     empty_cells = size * size - clues
#     indices = [(i, j) for i in range(size) for j in range(size)]
#     random.shuffle(indices)
    
#     for i, j in indices[:empty_cells]:
#         board[i][j] = 0
    
#     return board

# def time_solver(solver, board):
#     board_copy = copy.deepcopy(board)
#     start = time.time()
#     result = solver(board_copy)
#     end = time.time()
#     return end - start if result else float('inf')

# def plot_and_save_results(results, test_configs, solvers):
#     # Create a figure with subplots
#     fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16))
#     fig.suptitle('Sudoku Solver Performance Comparison', fontsize=16)
    
#     # First subplot - combined results
#     x_labels = [config["label"] for config in test_configs]
#     x = range(len(x_labels))
#     width = 0.25
    
#     for i, solver in enumerate(solvers):
#         ax1.bar([p + width * i for p in x], results[solver["name"]], width, label=solver["name"])
    
#     ax1.set_ylabel('Time (seconds)')
#     ax1.set_title('All Configurations')
#     ax1.set_xticks([p + width for p in x])
#     ax1.set_xticklabels(x_labels)
#     ax1.legend()
    
#     # Second subplot - individual configurations
#     colors = ['blue', 'orange', 'green']
#     for i, config in enumerate(test_configs):
#         solver_names = [solver["name"] for solver in solvers]
#         times = [results[solver["name"]][i] for solver in solvers]
#         ax2.bar([f"{solver}\n{config['label']}" for solver in solver_names], 
#                 times, color=colors, alpha=0.6)
    
#     ax2.set_ylabel('Time (seconds)')
#     ax2.set_title('Individual Configurations')
#     ax2.tick_params(axis='x', rotation=45)
    
#     plt.tight_layout()
#     plt.savefig('sudoku_benchmark.png', dpi=300, bbox_inches='tight')
#     plt.close()
#     print("Results saved to 'sudoku_benchmark.png'")

# # Test configurations
# test_configs = [
#     {"size": 9, "clues": 30, "label": "9x9 (30 clues)"},
#     {"size": 9, "clues": 25, "label": "9x9 (25 clues)"},
#     {"size": 16, "clues": 200, "label": "16x16 (100 clues)"},
#     {"size": 16, "clues": 150, "label": "16x16 (120 clues)"}
# ]

# # Solvers to test
# solvers = [
#     {"name": "Backtracking", "func": backtracking_solver},
#     {"name": "DFS", "func": dfs_solver},
#     {"name": "Greedy MRV", "func": greedy_mrv_solver}
# ]

# # Run tests
# results = {solver["name"]: [] for solver in solvers}
# num_tests = 5  # Number of tests per configuration

# for config in test_configs:
#     print(f"\nTesting {config['label']}...")
#     for solver in solvers:
#         total_time = 0
#         for _ in range(num_tests):
#             board = generate_sudoku(config["size"], config["clues"])
#             solve_time = time_solver(solver["func"], board)
#             if solve_time == float('inf'):
#                 print(f"{solver['name']} failed to solve a puzzle")
#                 solve_time = 0  # Skip failed attempts for averaging
#             else:
#                 total_time += solve_time
#         avg_time = total_time / num_tests
#         results[solver["name"]].append(avg_time)
#         print(f"{solver['name']}: {avg_time:.4f} seconds average")

# # Plot and save results
# plot_and_save_results(results, test_configs, solvers)













import time
import random
import copy
import matplotlib.pyplot as plt
from sudoku import is_valid
from collections import defaultdict


# Sudoku Generator
def generate_sudoku(N, clues):
    base = int(N**0.5)
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % N

    def shuffle(s):
        return random.sample(s, len(s))

    rows = [g * base + r for g in shuffle(range(base)) for r in shuffle(range(base))]
    cols = [g * base + c for g in shuffle(range(base)) for c in shuffle(range(base))]
    nums = shuffle(range(1, N + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    squares = N * N
    empties = squares - clues
    for _ in range(empties):
        r, c = divmod(random.randrange(squares), N)
        board[r][c] = 0

    return board


# DFS Solver
def dfs_solver(board):
    size = len(board)
    stack = [(0, 0, copy.deepcopy(board))]
    while stack:
        row, col, b = stack.pop()
        if row == size:
            return b
        if b[row][col] != 0:
            next_col = (col + 1) % size
            next_row = row + (col + 1) // size
            stack.append((next_row, next_col, b))
            continue
        for num in range(1, size+1):
            if is_valid(b, row, col, num):
                new_board = copy.deepcopy(b)
                new_board[row][col] = num
                next_col = (col + 1) % size
                next_row = row + (col + 1) // size
                stack.append((next_row, next_col, new_board))
    return None

# Backtracking Solver
def backtracking_solver(board):
    size = len(board)
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                for num in range(1, size+1):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if backtracking_solver(board):
                            return board
                        board[row][col] = 0
                return None
    return board


# Greedy Solver
def greedy_solver(board):
    size = len(board)
    empty = [(r, c) for r in range(size) for c in range(size) if board[r][c] == 0]
    random.shuffle(empty)
    for row, col in empty:
        for num in range(1, size+1):
            if is_valid(board, row, col, num):
                board[row][col] = num
                break
        if board[row][col] == 0:
            return None
    return board if all(all(cell != 0 for cell in row) for row in board) else None


# Benchmarking Function
def benchmark_solvers(sizes, trials):
    results = {
        'dfs': defaultdict(lambda: defaultdict(list)),
        'backtracking': defaultdict(lambda: defaultdict(list)),
        'greedy': defaultdict(lambda: defaultdict(list))
    }

    for size in sizes:
        if size == 9:
            clue_counts = [20, 30, 40]
        elif size == 16:
            clue_counts = [110, 120, 130]
        else:
            print(f"Skipping unsupported size: {size}")
            continue

        for clues in clue_counts:
            print(f"\nBenchmarking size {size}x{size} with {clues} clues...")
            for trial in range(1, trials + 1):
                board = generate_sudoku(size, clues)
                print(f"  Trial {trial}/{trials}:")

                # DFS
                start = time.time()
                try:
                    dfs_solver(copy.deepcopy(board))
                except Exception as e:
                    print(f"    DFS failed: {e}")
                dfs_time = time.time() - start
                results['dfs'][size][clues].append(dfs_time)
                print(f"    DFS time:         {dfs_time:.4f} seconds")

                # Backtracking
                start = time.time()
                try:
                    backtracking_solver(copy.deepcopy(board))
                except Exception as e:
                    print(f"    Backtracking failed: {e}")
                bt_time = time.time() - start
                results['backtracking'][size][clues].append(bt_time)
                print(f"    Backtracking time: {bt_time:.4f} seconds")

                # Greedy
                start = time.time()
                try:
                    greedy_solver(copy.deepcopy(board))
                except Exception as e:
                    print(f"    Greedy failed: {e}")
                greedy_time = time.time() - start
                results['greedy'][size][clues].append(greedy_time)
                print(f"    Greedy time:       {greedy_time:.4f} seconds")

    return results


def show_all_plots(results):
    sizes = sorted(results['backtracking'].keys())
    plt.figure(figsize=(15, 12))
    
    # Plot 1: Performance by Grid Size (middle clue count)
    plt.subplot(2, 2, 1)
    for method in results.keys():
        avg_times = []
        for size in sizes:
            clues = sorted(results[method][size].keys())[len(results[method][size])//2]
            times = results[method][size][clues]
            avg_times.append(sum(times)/len(times))
        plt.plot(sizes, avg_times, 'o-', label=method)
    plt.title('Performance by Grid Size (Middle Clue Count)')
    plt.xlabel('Grid Size')
    plt.ylabel('Time (seconds)')
    plt.grid(True)
    plt.legend()
    plt.yscale('log')

    # Plot 2: Performance by Clue Count (9x9)
    plt.subplot(2, 2, 2)
    if 9 in sizes:
        clue_counts = sorted(results['backtracking'][9].keys())
        for method in results.keys():
            avg_times = [sum(results[method][9][clues])/len(results[method][9][clues]) for clues in clue_counts]
            plt.plot(clue_counts, avg_times, 'o-', label=method)
        plt.title('Performance by Clue Count (9x9 Grid)')
        plt.xlabel('Number of Clues')
        plt.ylabel('Time (seconds)')
        plt.grid(True)
        plt.legend()
        plt.yscale('log')

    # Plot 3: Performance by Clue Count (16x16)
    plt.subplot(2, 2, 3)
    if 16 in sizes:
        clue_counts = sorted(results['backtracking'][16].keys())
        for method in results.keys():
            avg_times = [sum(results[method][16][clues])/len(results[method][16][clues]) for clues in clue_counts]
            plt.plot(clue_counts, avg_times, 'o-', label=method)
        plt.title('Performance by Clue Count (16x16 Grid)')
        plt.xlabel('Number of Clues')
        plt.ylabel('Time (seconds)')
        plt.grid(True)
        plt.legend()
        plt.yscale('log')

    plt.tight_layout()
    plt.savefig('sudoku_benchmark.png', dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    print("Starting benchmark tests...")
    sizes_to_test = [9, 16]
    trials = 6

    results = benchmark_solvers(
        sizes=sizes_to_test,
        trials=trials
    )
    show_all_plots(results)
