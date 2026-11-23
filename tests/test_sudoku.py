"""Unit tests for Sudoku Solver Engine."""
import unittest
from sudoku.solver import (
    solve_grid,
    validate_entire_grid,
    is_valid_entry,
    PRESETS,
    copy_grid
)

class TestSudokuSolver(unittest.TestCase):
    def test_solve_easy_preset(self):
        board = copy_grid(PRESETS["Easy"])
        solved, steps, elapsed = solve_grid(board)
        self.assertTrue(solved)
        # Verify completely filled
        for r in range(9):
            for c in range(9):
                self.assertIn(board[r][c], range(1, 10))
        # Verify valid solution
        valid, msg = validate_entire_grid(board)
        self.assertTrue(valid)

    def test_solve_hardest_preset(self):
        # Solves world famous AI Escargot
        board = copy_grid(PRESETS["Expert (AI Escargot)"])
        solved, steps, elapsed = solve_grid(board)
        self.assertTrue(solved)
        valid, _ = validate_entire_grid(board)
        self.assertTrue(valid)

    def test_detect_row_conflict(self):
        board = [[0]*9 for _ in range(9)]
        board[0][0] = 5
        board[0][8] = 5 # duplicate in row
        valid, msg = validate_entire_grid(board)
        self.assertFalse(valid)
        self.assertIn("Conflict", msg)

    def test_detect_box_conflict(self):
        board = [[0]*9 for _ in range(9)]
        board[0][0] = 4
        board[1][1] = 4 # duplicate in same 3x3 block
        valid, msg = validate_entire_grid(board)
        self.assertFalse(valid)

    def test_unsolvable_board(self):
        # 1 and 2 in same row where an empty cell cannot be filled
        board = [
            [5, 1, 6, 8, 4, 9, 7, 3, 2],
            [3, 0, 7, 6, 0, 5, 0, 0, 0],
            [8, 0, 9, 7, 0, 0, 0, 6, 5],
            [1, 3, 5, 0, 6, 0, 9, 0, 7],
            [4, 7, 2, 5, 9, 1, 0, 0, 6],
            [9, 6, 8, 3, 7, 0, 0, 5, 0],
            [2, 5, 3, 1, 8, 6, 0, 7, 4],
            [6, 8, 4, 2, 0, 7, 5, 0, 0],
            [7, 9, 1, 0, 5, 0, 6, 0, 8]
        ]
        # Force contradiction
        board[1][1] = 5 # Conflicts with row 0 col 0 indirectly or unsolvable
        board[1][4] = 5
        valid, _ = validate_entire_grid(board)
        self.assertFalse(valid)

if __name__ == "__main__":
    unittest.main()
