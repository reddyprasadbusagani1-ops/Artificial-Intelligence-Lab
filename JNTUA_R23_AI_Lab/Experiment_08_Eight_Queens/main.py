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
