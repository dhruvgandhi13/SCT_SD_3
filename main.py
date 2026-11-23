#!/usr/bin/env python3
"""Main Entrypoint for SCT_SD_3 Sudoku Solver.

Launches modern GUI by default, or CLI if --cli flag is passed.
"""
import sys

def main():
    if "--cli" in sys.argv or "-c" in sys.argv:
        from sudoku.cli import run_cli
        run_cli()
    else:
        from sudoku.gui import launch_gui
        launch_gui()

if __name__ == "__main__":
    main()
