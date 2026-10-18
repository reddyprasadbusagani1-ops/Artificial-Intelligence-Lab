# Experiment 8: Eight Queens Problem

**Artificial Intelligence Lab | Subject Code 23A31301P | JNTUA R23 | B.Tech AI & DS**

## Aim

To solve the eight-queens problem using backtracking, display valid boards and report the total number of solutions.

## Theory

Place 8 queens on an 8x8 chessboard so that **no two queens attack each other**: no two share a row, a column or a diagonal. **Backtracking** builds the solution one row at a time. For each row it tries each column; if the square is safe it places a queen and moves to the next row. If no column is safe, it **backtracks** (removes the previous queen) and tries the next column there.

Two queens (r1, c1) and (r2, c2) attack diagonally when |c1 - c2| = |r1 - r2|. The 8x8 board has **92** solutions (12 distinct up to rotation/reflection).

## Algorithm / Procedure

1. `place(row)`: if row == N, store a copy of the placement as a solution.
2. For each column 0..N-1: if `is_safe(row, column)` (no earlier queen in the same column or diagonal), put the queen there, call `place(row + 1)`, then remove the queen (backtrack).
3. Collect all solutions; print the count, the first solution as a board, and (for N = 8) a second one.
4. Verify every solution with an independent validity check.

## Source Code

The complete program is in [`main.py`](main.py) and is reproduced here.

```python
"""
Experiment 8: Eight Queens Problem (backtracking)
Subject: Artificial Intelligence Lab (23A31301P) - JNTUA R23

Place 8 queens on an 8x8 board so that no two attack each other
(no shared row, column or diagonal).
Backtracking places one queen per row, column by column; if a row has no safe
square, it goes back to the previous row and tries the next column.
The program also accepts other board sizes N (the 8x8 board has 92 solutions).
"""


def ask(prompt, default):
    try:
        text = input(prompt).strip()
    except EOFError:
        return default
    return text if text else default


def is_safe(columns, row, col):
    """columns[r] = column of the queen in row r (rows 0..row-1 are already placed)."""
    for placed_row in range(row):
        placed_col = columns[placed_row]
        same_column = placed_col == col
        same_diagonal = abs(placed_col - col) == abs(placed_row - row)
        if same_column or same_diagonal:
            return False
    return True


def solve_queens(n):
    """Return a list of all solutions; each solution is a list of columns per row."""
    solutions = []
    columns = []

    def place(row):
        if row == n:                       # all rows filled: a complete solution
            solutions.append(columns.copy())
            return
        for col in range(n):
            if is_safe(columns, row, col):
                columns.append(col)        # place a queen
                place(row + 1)
                columns.pop()              # BACKTRACK: remove the queen
    place(0)
    return solutions


def is_valid_solution(columns):
    """Independent check: n queens, one per column, no two on a common diagonal."""
    n = len(columns)
    if sorted(columns) != list(range(n)):
        return False
    return all(abs(columns[i] - columns[j]) != j - i
               for i in range(n) for j in range(i + 1, n))


def print_board(columns):
    for col in columns:
        print("   " + " ".join("Q" if c == col else "." for c in range(len(columns))))


def main():
    print("=" * 60)
    print("EXPERIMENT 8: EIGHT QUEENS PROBLEM")
    print("=" * 60)
    while True:
        text = ask("Board size N [8]: ", "8")
        if text.isdigit() and 1 <= int(text) <= 12:
            n = int(text)
            break
        print("  Please enter a whole number between 1 and 12.")

    solutions = solve_queens(n)
    print(f"\nNumber of solutions for {n} queens: {len(solutions)}")
    if not solutions:
        print("No arrangement exists for this board size.")
        return

    print("\nFirst solution (rows top to bottom, Q = queen):")
    print_board(solutions[0])
    print("Queen columns by row (1-based):", [c + 1 for c in solutions[0]])
    if n == 8:
        print("\nSecond solution:")
        print_board(solutions[1])
    print("\nCheck: all solutions valid and distinct =",
          all(is_valid_solution(s) for s in solutions)
          and len({tuple(s) for s in solutions}) == len(solutions))


if __name__ == "__main__":
    main()
```

## Sample Input

Board size N = 8 (press Enter). You may also enter 1-12; e.g. N = 6 has 4 solutions and N = 3 has none.

## Expected Output

The outputs below were produced by actually running `main.py` (Python 3.12) with the inputs shown; text after each prompt is the input that was typed.

**Default N = 8**

```text
============================================================
EXPERIMENT 8: EIGHT QUEENS PROBLEM
============================================================
Board size N [8]: 

Number of solutions for 8 queens: 92

First solution (rows top to bottom, Q = queen):
   Q . . . . . . .
   . . . . Q . . .
   . . . . . . . Q
   . . . . . Q . .
   . . Q . . . . .
   . . . . . . Q .
   . Q . . . . . .
   . . . Q . . . .
Queen columns by row (1-based): [1, 5, 8, 6, 3, 7, 2, 4]

Second solution:
   Q . . . . . . .
   . . . . . Q . .
   . . . . . . . Q
   . . Q . . . . .
   . . . . . . Q .
   . . . Q . . . .
   . Q . . . . . .
   . . . . Q . . .

Check: all solutions valid and distinct = True
```

**N = 3 (no solution)**

```text
============================================================
EXPERIMENT 8: EIGHT QUEENS PROBLEM
============================================================
Board size N [8]: 3

Number of solutions for 3 queens: 0
No arrangement exists for this board size.
```

**Invalid input then N = 6**

```text
============================================================
EXPERIMENT 8: EIGHT QUEENS PROBLEM
============================================================
Board size N [8]: abc
  Please enter a whole number between 1 and 12.
Board size N [8]: 6

Number of solutions for 6 queens: 4

First solution (rows top to bottom, Q = queen):
   . Q . . . .
   . . . Q . .
   . . . . . Q
   Q . . . . .
   . . Q . . .
   . . . . Q .
Queen columns by row (1-based): [2, 4, 6, 1, 3, 5]

Check: all solutions valid and distinct = True
```

## Result

The program finds all **92** solutions for N = 8 and prints the first valid board. All solutions are verified to be valid and distinct. Other sizes work too (N = 6 gives 4, N = 3 gives 0).

## How to Run

```bat
cd Experiment_08_Eight_Queens
python main.py
```

From the project root you can also run `run_experiment.bat 8`.
