import time
import random
import copy
from collections import defaultdict
import matplotlib.pyplot as plt
from sudoku import is_valid



# Sudoku Generator
def generate_sudoku(N, clues):
    """
    Generate a Sudoku board of size NxN with a given number of clues.
    Returns:
        list: A 2D list representing the generated Sudoku board.
    """
    base = int(N**0.5)
    def pattern(r, c):
        """
        Determine the value at position (r, c) based on the Sudoku pattern.
        """
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
    """
    Solve the Sudoku puzzle using Depth First Search (DFS) algorithm.
    Args:
        board (list): The Sudoku puzzle to be solved.
    Returns:
        list: A solved Sudoku board, or None if no solution exists.
    """
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
    """
    Solve the Sudoku puzzle using the Backtracking algorithm.
    Args:
        board (list): The Sudoku puzzle to be solved.
    Returns:
        list: A solved Sudoku board, or None if no solution exists.
    """
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
    """
    Solve the Sudoku puzzle using the Greedy algorithm.
    
    Args:
        board (list): The Sudoku puzzle to be solved.
    
    Returns:
        list: A solved Sudoku board, or None if no solution exists.
    """
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
    """
    Benchmark the three Sudoku solving algorithms (DFS, Backtracking, Greedy) 
    on different board sizes and clue counts.
    Args:
        sizes (list): A list of grid sizes
        trials (int): The number of trials to run for each size and clue count.
    Returns:
        dict: A dictionary containing the results of the benchmark for each algorithm.
    """
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
    """
    Generate and display plots based on benchmarking results.
    """
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
