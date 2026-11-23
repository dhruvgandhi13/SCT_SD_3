"""Command-line interface for the Sudoku Solver."""
import sys
from .solver import solve_grid, PRESETS, copy_grid, validate_entire_grid

def print_grid(grid):
    print("+-------+-------+-------+")
    for r in range(9):
        row_str = "| "
        for c in range(9):
            val = str(grid[r][c]) if grid[r][c] != 0 else "."
            row_str += val + " "
            if (c + 1) % 3 == 0:
                row_str += "| "
        print(row_str)
        if (r + 1) % 3 == 0:
            print("+-------+-------+-------+")

def run_cli():
    print("\n" + "=" * 45)
    print("      🧩 SUDOKU SOLVER ENGINE (CLI)")
    print("=" * 45)
    print("Available Presets: " + ", ".join(PRESETS.keys()))

    preset_name = "Hard"
    if len(sys.argv) > 2 and sys.argv[2] in PRESETS:
        preset_name = sys.argv[2]

    print(f"\n[+] Selected Preset: {preset_name}")
    board = copy_grid(PRESETS[preset_name])

    print("\n[Input Unsolved Puzzle]")
    print_grid(board)

    valid, msg = validate_entire_grid(board)
    if not valid:
        print(f"\n[!] Board Validation Failed: {msg}")
        return

    print("\nSolving using MRV Backtracking algorithm...")
    success, steps, elapsed = solve_grid(board)

    if success:
        print("\n[Solved Puzzle]")
        print_grid(board)
        print(f"\nExecution Time: {elapsed*1000:.3f} ms")
        print(f"Recursive Backtrack Steps: {steps}")
    else:
        print("\n[!] No valid solution could be found.")

if __name__ == "__main__":
    run_cli()
