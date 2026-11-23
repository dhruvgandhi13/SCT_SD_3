"""Modern Graphical User Interface for Automated Sudoku Solver."""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
import time
from .solver import (
    solve_grid,
    validate_entire_grid,
    is_valid_entry,
    solve_step_generator,
    PRESETS,
    copy_grid,
    Grid
)

class SudokuGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SudokuMatrix - Automated Sudoku Solver")
        self.root.geometry("860x780")
        self.root.minsize(800, 720)
        self.root.configure(bg="#0F172A")

        self.cells: list[list[tk.Entry]] = []
        self.cell_vars: list[list[tk.StringVar]] = []
        self.original_puzzle: Grid = [[0]*9 for _ in range(9)]
        self.is_animating = False
        self.anim_generator = None

        self.status_var = tk.StringVar(value="Status: Ready | Enter numbers or load a preset")
        self.metric_var = tk.StringVar(value="Time: 0.000s | Backtrack Steps: 0")
        self.preset_var = tk.StringVar(value="Medium")
        self.speed_var = tk.IntVar(value=20) # ms delay per step

        self._build_ui()
        self.load_preset("Medium")

    def _build_ui(self):
        # Header banner
        header = tk.Frame(self.root, bg="#1E293B", padx=24, pady=14)
        header.pack(fill="x")

        title_row = tk.Frame(header, bg="#1E293B")
        title_row.pack(fill="x")

        tk.Label(
            title_row,
            text="🧩 SudokuMatrix Solver",
            font=("Segoe UI", 18, "bold"),
            fg="#38BDF8",
            bg="#1E293B"
        ).pack(side="left")

        tk.Label(
            title_row,
            text="MRV Backtracking Engine",
            font=("Segoe UI", 9, "bold"),
            fg="#94A3B8",
            bg="#334155",
            padx=10,
            pady=3
        ).pack(side="right")

        tk.Label(
            header,
            text="Automatic 9x9 Sudoku Solver with instant solving and step-by-step visual animation",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#1E293B"
        ).pack(anchor="w", pady=(2, 0))

        # Main Body Frame
        container = tk.Frame(self.root, bg="#0F172A", padx=20, pady=12)
        container.pack(fill="both", expand=True)

        # Controls & Presets Bar
        toolbar = tk.Frame(container, bg="#1E293B", padx=16, pady=10)
        toolbar.pack(fill="x", pady=(0, 12))

        # Preset selector
        tk.Label(toolbar, text="Preset:", font=("Segoe UI", 9, "bold"), fg="#94A3B8", bg="#1E293B").pack(side="left", padx=(0, 6))
        preset_menu = ttk.Combobox(
            toolbar,
            textvariable=self.preset_var,
            values=list(PRESETS.keys()),
            state="readonly",
            width=18,
            font=("Segoe UI", 9)
        )
        preset_menu.pack(side="left", padx=(0, 10))
        preset_menu.bind("<<ComboboxSelected>>", lambda e: self.load_preset(self.preset_var.get()))

        load_btn = tk.Button(
            toolbar, text="Load Preset", font=("Segoe UI", 9), bg="#334155", fg="#F8FAFC",
            activebackground="#475569", relief="flat", cursor="hand2", padx=8, pady=2,
            command=lambda: self.load_preset(self.preset_var.get())
        )
        load_btn.pack(side="left", padx=(0, 12))

        clear_btn = tk.Button(
            toolbar, text="🧹 Clear", font=("Segoe UI", 9), bg="#334155", fg="#F8FAFC",
            activebackground="#475569", relief="flat", cursor="hand2", padx=8, pady=2,
            command=self.clear_grid
        )
        clear_btn.pack(side="left", padx=(0, 8))

        reset_btn = tk.Button(
            toolbar, text="🔄 Reset", font=("Segoe UI", 9), bg="#334155", fg="#F8FAFC",
            activebackground="#475569", relief="flat", cursor="hand2", padx=8, pady=2,
            command=self.reset_to_original
        )
        reset_btn.pack(side="left", padx=(0, 12))

        validate_btn = tk.Button(
            toolbar, text="✅ Validate", font=("Segoe UI", 9), bg="#0284C7", fg="#FFFFFF",
            activebackground="#0369A1", relief="flat", cursor="hand2", padx=8, pady=2,
            command=self.validate_board
        )
        validate_btn.pack(side="left", padx=(0, 8))

        # Solve Action Buttons
        self.instant_btn = tk.Button(
            toolbar, text="⚡ Solve Instantly", font=("Segoe UI", 9, "bold"), bg="#10B981", fg="#FFFFFF",
            activebackground="#059669", relief="flat", cursor="hand2", padx=12, pady=2,
            command=self.solve_instant
        )
        self.instant_btn.pack(side="right", padx=(8, 0))

        self.anim_btn = tk.Button(
            toolbar, text="▶️ Animate Solve", font=("Segoe UI", 9, "bold"), bg="#6366F1", fg="#FFFFFF",
            activebackground="#4F46E5", relief="flat", cursor="hand2", padx=10, pady=2,
            command=self.toggle_animation
        )
        self.anim_btn.pack(side="right", padx=(8, 0))

        # Center Board Frame
        board_outer = tk.Frame(container, bg="#334155", padx=3, pady=3)
        board_outer.pack(pady=4)

        for r in range(9):
            row_cells = []
            row_vars = []
            for c in range(9):
                # 3x3 block grouping styling
                bg_color = "#1E293B" if ((r // 3) + (c // 3)) % 2 == 0 else "#0F172A"
                
                # Outer borders for 3x3 subgrids
                ptop = 3 if r % 3 == 0 else 1
                pbot = 3 if r == 8 else 1
                pleft = 3 if c % 3 == 0 else 1
                pright = 3 if c == 8 else 1

                cell_frame = tk.Frame(
                    board_outer,
                    bg="#475569",
                    padx=0,
                    pady=0
                )
                cell_frame.grid(
                    row=r,
                    column=c,
                    padx=(pleft, pright),
                    pady=(ptop, pbot)
                )

                var = tk.StringVar()
                entry = tk.Entry(
                    cell_frame,
                    textvariable=var,
                    font=("Segoe UI", 16, "bold"),
                    justify="center",
                    width=2,
                    bg=bg_color,
                    fg="#F8FAFC",
                    relief="flat",
                    insertbackground="#38BDF8"
                )
                entry.pack(ipadx=6, ipady=5)

                # Navigation and validation bindings
                entry.bind("<KeyRelease>", lambda e, r=r, c=c: self._handle_cell_input(r, c, e))
                entry.bind("<Up>", lambda e, r=r, c=c: self._move_focus(r - 1, c))
                entry.bind("<Down>", lambda e, r=r, c=c: self._move_focus(r + 1, c))
                entry.bind("<Left>", lambda e, r=r, c=c: self._move_focus(r, c - 1))
                entry.bind("<Right>", lambda e, r=r, c=c: self._move_focus(r, c + 1))

                row_cells.append(entry)
                row_vars.append(var)

            self.cells.append(row_cells)
            self.cell_vars.append(row_vars)

        # Bottom Analytics & Animation Speed Bar
        bottom_bar = tk.Frame(container, bg="#1E293B", padx=16, pady=10)
        bottom_bar.pack(fill="x", pady=(12, 0))

        # Status row
        tk.Label(
            bottom_bar,
            textvariable=self.status_var,
            font=("Segoe UI", 10, "bold"),
            fg="#38BDF8",
            bg="#1E293B"
        ).pack(anchor="w")

        metrics_row = tk.Frame(bottom_bar, bg="#1E293B")
        metrics_row.pack(fill="x", pady=(4, 0))

        tk.Label(
            metrics_row,
            textvariable=self.metric_var,
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#1E293B"
        ).pack(side="left")

        # Speed slider for animation
        speed_frame = tk.Frame(metrics_row, bg="#1E293B")
        speed_frame.pack(side="right")
        tk.Label(speed_frame, text="Speed (ms):", font=("Segoe UI", 8), fg="#94A3B8", bg="#1E293B").pack(side="left", padx=4)
        speed_scale = tk.Scale(
            speed_frame,
            from_=1,
            to=100,
            orient="horizontal",
            variable=self.speed_var,
            bg="#1E293B",
            fg="#94A3B8",
            highlightthickness=0,
            length=100
        )
        speed_scale.pack(side="left")

    def _handle_cell_input(self, r: int, c: int, event):
        val = self.cell_vars[r][c].get()
        if len(val) > 1:
            val = val[-1]
            self.cell_vars[r][c].set(val)

        if val and val in "123456789":
            self.cells[r][c].config(fg="#38BDF8")
            # Move to next cell automatically
            if c < 8:
                self._move_focus(r, c + 1)
            elif r < 8:
                self._move_focus(r + 1, 0)
        elif val == "" or val == "0":
            self.cell_vars[r][c].set("")
        else:
            self.cell_vars[r][c].set("")

    def _move_focus(self, r: int, c: int):
        if 0 <= r < 9 and 0 <= c < 9:
            self.cells[r][c].focus_set()

    def get_current_grid(self) -> Grid:
        grid: Grid = []
        for r in range(9):
            row: list[int] = []
            for c in range(9):
                val = self.cell_vars[r][c].get().strip()
                row.append(int(val) if val.isdigit() and 1 <= int(val) <= 9 else 0)
            grid.append(row)
        return grid

    def load_preset(self, name: str):
        if name not in PRESETS:
            return
        grid = PRESETS[name]
        self.original_puzzle = copy_grid(grid)
        self.populate_board(grid, is_original=True)
        self.status_var.set(f"Loaded '{name}' preset. Ready to solve!")
        self.metric_var.set("Time: 0.000s | Backtrack Steps: 0")

    def populate_board(self, grid: Grid, is_original: bool = False):
        for r in range(9):
            for c in range(9):
                val = grid[r][c]
                bg_color = "#1E293B" if ((r // 3) + (c // 3)) % 2 == 0 else "#0F172A"
                if val != 0:
                    self.cell_vars[r][c].set(str(val))
                    if is_original:
                        self.cells[r][c].config(fg="#F8FAFC", bg=bg_color) # Preset: bold white
                    else:
                        self.cells[r][c].config(fg="#34D399", bg=bg_color) # Solved: emerald green
                else:
                    self.cell_vars[r][c].set("")
                    self.cells[r][c].config(fg="#F8FAFC", bg=bg_color)

    def clear_grid(self):
        self.is_animating = False
        self.original_puzzle = [[0]*9 for _ in range(9)]
        for r in range(9):
            for c in range(9):
                self.cell_vars[r][c].set("")
                bg_color = "#1E293B" if ((r // 3) + (c // 3)) % 2 == 0 else "#0F172A"
                self.cells[r][c].config(fg="#F8FAFC", bg=bg_color)
        self.status_var.set("Board cleared. Ready for manual entry.")
        self.metric_var.set("Time: 0.000s | Backtrack Steps: 0")

    def reset_to_original(self):
        self.is_animating = False
        self.populate_board(self.original_puzzle, is_original=True)
        self.status_var.set("Board reset to original puzzle state.")

    def validate_board(self):
        grid = self.get_current_grid()
        valid, msg = validate_entire_grid(grid)
        if valid:
            filled = sum(1 for r in range(9) for c in range(9) if grid[r][c] != 0)
            messagebox.showinfo("Validation Passed", f"The board is completely valid! ({filled}/81 cells placed)")
            self.status_var.set("Board status: Completely valid with no rule conflicts.")
        else:
            messagebox.showerror("Conflict Detected", msg)
            self.status_var.set(f"Conflict: {msg}")

    def solve_instant(self):
        self.is_animating = False
        grid = self.get_current_grid()
        valid, msg = validate_entire_grid(grid)
        if not valid:
            messagebox.showerror("Invalid Input Grid", msg)
            return

        solved_grid = copy_grid(grid)
        success, steps, elapsed = solve_grid(solved_grid)

        if success:
            for r in range(9):
                for c in range(9):
                    bg_color = "#1E293B" if ((r // 3) + (c // 3)) % 2 == 0 else "#0F172A"
                    if grid[r][c] == 0:
                        self.cell_vars[r][c].set(str(solved_grid[r][c]))
                        self.cells[r][c].config(fg="#34D399", bg=bg_color)
            self.status_var.set("🎉 Puzzle successfully solved!")
            self.metric_var.set(f"Time: {elapsed*1000:.2f} ms | Backtrack Recursive Calls: {steps}")
        else:
            messagebox.showwarning("Unsolvable", "No valid solution exists for this Sudoku configuration.")
            self.status_var.set("Failure: Unsolvable configuration.")

    def toggle_animation(self):
        if self.is_animating:
            self.is_animating = False
            self.anim_btn.config(text="▶️ Animate Solve", bg="#6366F1")
            self.status_var.set("Animation paused.")
            return

        grid = self.get_current_grid()
        valid, msg = validate_entire_grid(grid)
        if not valid:
            messagebox.showerror("Invalid Input Grid", msg)
            return

        self.is_animating = True
        self.anim_btn.config(text="⏹️ Stop", bg="#EF4444")
        self.status_var.set("Running animated backtracking search...")

        anim_board = copy_grid(grid)
        self.anim_generator = solve_step_generator(anim_board)
        self._step_animation(grid)

    def _step_animation(self, original: Grid):
        if not self.is_animating or not self.anim_generator:
            return

        try:
            r, c, val, action = next(self.anim_generator)
            bg_color = "#1E293B" if ((r // 3) + (c // 3)) % 2 == 0 else "#0F172A"

            if action == "SET":
                self.cell_vars[r][c].set(str(val))
                self.cells[r][c].config(fg="#FBBF24", bg="#3B2606") # Testing: Amber
            elif action == "CLEAR":
                self.cell_vars[r][c].set("")
                self.cells[r][c].config(fg="#F8FAFC", bg=bg_color)

            delay = max(1, self.speed_var.get())
            self.root.after(delay, lambda: self._step_animation(original))
        except StopIteration as e:
            self.is_animating = False
            self.anim_btn.config(text="▶️ Animate Solve", bg="#6366F1")
            # Mark all solved cells emerald
            current = self.get_current_grid()
            for row in range(9):
                for col in range(9):
                    bg_color = "#1E293B" if ((row // 3) + (col // 3)) % 2 == 0 else "#0F172A"
                    if original[row][col] == 0 and current[row][col] != 0:
                        self.cells[row][col].config(fg="#34D399", bg=bg_color)
            self.status_var.set("🎉 Visual solve completed!")

def launch_gui():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
