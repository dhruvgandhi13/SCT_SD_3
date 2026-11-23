"""Sudoku Solver Engine using Backtracking and MRV Heuristic."""
from __future__ import annotations
import time
from typing import List, Optional, Tuple, Iterator, Generator

Grid = List[List[int]]

PRESETS = {
    "Easy": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    "Medium": [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ],
    "Hard": [
        [0, 0, 0, 6, 0, 0, 4, 0, 0],
        [7, 0, 0, 0, 0, 3, 6, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 1, 8, 0, 0, 0, 3],
        [0, 0, 0, 3, 0, 6, 0, 4, 5],
        [0, 4, 0, 2, 0, 0, 0, 6, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 1, 0, 0]
    ],
    "Expert (AI Escargot)": [
        [1, 0, 0, 0, 0, 7, 0, 9, 0],
        [0, 3, 0, 0, 2, 0, 0, 0, 8],
        [0, 0, 9, 6, 0, 0, 5, 0, 0],
        [0, 0, 5, 3, 0, 0, 9, 0, 0],
        [0, 1, 0, 0, 8, 0, 0, 0, 2],
        [6, 0, 0, 0, 0, 4, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 7, 0, 0, 0, 3, 0, 0]
    ]
}

def is_valid_entry(grid: Grid, row: int, col: int, num: int) -> bool:
    """Check if placing num at grid[row][col] is legally valid."""
    # Check row
    for c in range(9):
        if c != col and grid[row][c] == num:
            return False

    # Check column
    for r in range(9):
        if r != row and grid[r][col] == num:
            return False

    # Check 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r != row or c != col) and grid[r][c] == num:
                return False

    return True

def validate_entire_grid(grid: Grid) -> Tuple[bool, str]:
    """Validate all filled numbers on board for conflicts."""
    for r in range(9):
        for c in range(9):
            val = grid[r][c]
            if val != 0:
                if not (1 <= val <= 9):
                    return False, f"Invalid value {val} at Row {r+1}, Col {c+1}. Must be 1-9."
                if not is_valid_entry(grid, r, c, val):
                    return False, f"Conflict detected for digit {val} at Row {r+1}, Col {c+1}."
    return True, "Board is valid!"

def find_mrv_empty(grid: Grid) -> Optional[Tuple[int, int, List[int]]]:
    """Find empty cell with Minimum Remaining Values (MRV heuristic)."""
    min_candidates = 10
    best_cell = None

    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                candidates = [num for num in range(1, 10) if is_valid_entry(grid, r, c, num)]
                if len(candidates) < min_candidates:
                    min_candidates = len(candidates)
                    best_cell = (r, c, candidates)
                    if min_candidates == 0:
                        # Dead end detected early
                        return best_cell

    return best_cell

def solve_grid(grid: Grid) -> Tuple[bool, int, float]:
    """Solve puzzle in-place using MRV Backtracking. Returns (solved, steps, elapsed_time)."""
    start_time = time.perf_counter()
    steps = 0

    def backtrack() -> bool:
        nonlocal steps
        steps += 1
        mrv = find_mrv_empty(grid)
        if mrv is None:
            return True # No empty cells left: solved!

        row, col, candidates = mrv
        if not candidates:
            return False # Dead end

        for num in candidates:
            grid[row][col] = num
            if backtrack():
                return True
            grid[row][col] = 0

        return False

    solved = backtrack()
    elapsed = time.perf_counter() - start_time
    return solved, steps, elapsed

def solve_step_generator(grid: Grid) -> Generator[Tuple[int, int, int, str], None, bool]:
    """Yields steps for visual animation: (row, col, value, action)."""
    def backtrack() -> Generator[Tuple[int, int, int, str], None, bool]:
        mrv = find_mrv_empty(grid)
        if mrv is None:
            return True

        row, col, candidates = mrv
        if not candidates:
            return False

        for num in candidates:
            grid[row][col] = num
            yield (row, col, num, "SET")
            if (yield from backtrack()):
                return True
            grid[row][col] = 0
            yield (row, col, 0, "CLEAR")

        return False

    return (yield from backtrack())

def copy_grid(grid: Grid) -> Grid:
    return [row[:] for row in grid]
