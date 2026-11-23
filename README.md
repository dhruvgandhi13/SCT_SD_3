# SudokuMatrix - Automated Sudoku Solver

An automated 9x9 Sudoku solver application featuring a modern desktop graphical user interface, visual backtracking animation, and high-performance Constraint Satisfaction heuristics (MRV - Minimum Remaining Values). Developed as part of the SkillCraft Technology Software Development Internship (Track Code: SD, Task 03).

## Features

- **High-Performance Solving Engine**: Solves standard and complex 9x9 puzzles in milliseconds using depth-first backtracking optimized with the Minimum Remaining Values (MRV) heuristic.
- **Visual Animated Solver**: Watch the algorithmic search in real-time with an interactive speed-adjustment slider.
- **Modern 9x9 Grid GUI**:
  - Clear visual demarcation of 3x3 subgrids.
  - Automatic cursor advancement and directional arrow key navigation.
  - Color-coded feedback (user inputs vs. solved digits vs. validation conflicts).
- **Rule Verification & Validation**: Instantly verifies complete row, column, and 3x3 block constraints to detect inconsistencies before solving.
- **Built-in Difficulty Presets**: Includes Easy, Medium, Hard, and the famous "AI Escargot" (expert benchmark puzzle).
- **Terminal CLI Solver**: Run and solve puzzles directly within the terminal with full ASCII board rendering and metrics.
- **Zero External Dependencies**: Implemented entirely using Python's standard library.

## Project Structure

```text
SCT_SD_3/
├── sudoku/
│   ├── __init__.py       # Package definition
│   ├── solver.py         # MRV backtracking algorithm, validator, and presets
│   ├── gui.py            # Tkinter visual grid and animated GUI
│   └── cli.py            # Terminal interface with ASCII board formatter
├── tests/
│   └── test_sudoku.py    # Unit tests for algorithm correctness and benchmarks
├── main.py               # Main application launcher
├── requirements.txt      # Dependency specification
└── README.md             # Project documentation
```

## Getting Started

### Prerequisites
- Python 3.8 or higher.

### Launching the Graphical User Interface (GUI)
Start the desktop application:
```bash
python main.py
```

### Launching the Command-Line Interface (CLI)
Solve presets directly from your terminal:
```bash
python main.py --cli Hard
```

### Running Automated Tests
Run unit tests across presets and boundary conditions:
```bash
python -m unittest discover tests
```
