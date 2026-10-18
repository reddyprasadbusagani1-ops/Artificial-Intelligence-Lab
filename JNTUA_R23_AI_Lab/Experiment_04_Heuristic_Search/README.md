# Experiment 4: Heuristic Search (Manhattan distance on a grid)

**Artificial Intelligence Lab | Subject Code 23A31301P | JNTUA R23 | B.Tech AI & DS**

## Aim

To demonstrate heuristic search with a clear example, explain the heuristic used, and compare uninformed BFS, hill climbing and greedy best-first search.

## Theory

A **heuristic** h(n) is a rule-of-thumb estimate of the remaining cost from state n to the goal. Good heuristics let a search focus on promising states instead of exploring everything.

**Heuristic used - Manhattan distance:** on a grid where moves are up/down/left/right, h(cell) = |row - goal_row| + |column - goal_column|. It is the number of moves needed if there were no walls, so it never over-estimates (it is *admissible*).

Three methods are compared on a maze with a wall between the start and the goal:
* **BFS** - no heuristic; always finds a shortest path but expands many cells.
* **Hill climbing** - moves to the best neighbour and never goes back. It is cheap but can get stuck in a **local minimum** (a cell where every neighbour looks worse).
* **Greedy best-first** - also uses h, but keeps a frontier so it can **backtrack** out of dead ends.

## Algorithm / Procedure

1. Read the grid and locate S and G.
2. **BFS:** expand cells in FIFO order until G is reached.
3. **Hill climbing:** from the current cell, look at all walkable neighbours; move to the one with the smallest h only if it is smaller than the current h; otherwise stop (stuck).
4. **Greedy best-first:** keep a priority queue ordered by h; expand the smallest-h cell; add undiscovered neighbours; stop at G.
5. Draw each path with `*`, verify it is legal (adjacent steps, no walls, correct ends) and print statistics.

## Source Code

The complete program is in [`main.py`](main.py) and is reproduced here.

```python
"""
Experiment 4: Heuristic Search (Hill Climbing vs Greedy Best-First vs BFS)
Subject: Artificial Intelligence Lab (23A31301P) - JNTUA R23

Problem : find a path on a grid from S to G while avoiding walls (#).
Heuristic: Manhattan distance  h(cell) = |row - goal_row| + |col - goal_col|
           It estimates how many moves remain if there were no walls.

Three searches are compared:
  1. BFS (uninformed, no heuristic)            - always finds a shortest path
  2. Hill climbing (heuristic, no memory)      - can get STUCK in a local minimum
  3. Greedy best-first (heuristic + frontier)  - escapes dead ends by backtracking
"""

import heapq
import itertools
from collections import deque

GRID = [
    "...........",
    "......#....",
    "......#....",
    ".S....#.G..",
    "......#....",
    "......#....",
    "...........",   # the only gap in the wall is on the bottom row
]
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # up, down, left, right


def find_cell(grid, symbol):
    for r, row in enumerate(grid):
        if symbol in row:
            return (r, row.index(symbol))
    raise ValueError(f"Symbol {symbol} not found in grid")


def manhattan(cell, goal):
    """The heuristic: Manhattan distance between a cell and the goal."""
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def neighbours(grid, cell):
    """All walkable neighbouring cells (inside the grid and not a wall)."""
    r, c = cell
    for dr, dc in MOVES:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
            yield (nr, nc)


def build_path(parent, goal):
    path, cell = [], goal
    while cell is not None:
        path.append(cell)
        cell = parent[cell]
    return path[::-1]


def bfs(grid, start, goal):
    """Uninformed search. Returns (path, number of cells expanded)."""
    queue = deque([start])
    parent = {start: None}
    expanded = 0
    while queue:
        cell = queue.popleft()
        expanded += 1
        if cell == goal:
            return build_path(parent, goal), expanded
        for nxt in neighbours(grid, cell):
            if nxt not in parent:
                parent[nxt] = cell
                queue.append(nxt)
    return None, expanded


def hill_climbing(grid, start, goal):
    """
    Steepest-ascent hill climbing: always move to the neighbour with the lowest h,
    but only if it is strictly better than the current cell. No backtracking.
    Returns (path, stuck_flag).
    """
    current = start
    path = [current]
    while current != goal:
        best = min(neighbours(grid, current), key=lambda n: manhattan(n, goal),
                   default=None)
        if best is None or manhattan(best, goal) >= manhattan(current, goal):
            return path, True      # no neighbour is better: local minimum
        current = best
        path.append(current)
    return path, False


def greedy_best_first(grid, start, goal):
    """Greedy best-first: expand the frontier cell with the smallest h."""
    counter = itertools.count()
    frontier = [(manhattan(start, goal), next(counter), start)]
    parent = {start: None}
    expanded = 0
    while frontier:
        _, _, cell = heapq.heappop(frontier)
        expanded += 1
        if cell == goal:
            return build_path(parent, goal), expanded
        for nxt in neighbours(grid, cell):
            if nxt not in parent:
                parent[nxt] = cell
                heapq.heappush(frontier, (manhattan(nxt, goal), next(counter), nxt))
    return None, expanded


def draw(grid, path):
    """Print the grid with the path marked by '*'."""
    cells = set(path or [])
    for r, row in enumerate(grid):
        line = ""
        for c, ch in enumerate(row):
            line += "*" if (r, c) in cells and ch == "." else ch
        print("   " + line)


def path_is_valid(grid, path, start, goal):
    """Check start/goal, adjacency and that no wall is crossed."""
    if path[0] != start or path[-1] != goal:
        return False
    for a, b in zip(path, path[1:]):
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1 or grid[b[0]][b[1]] == "#":
            return False
    return True


def main():
    print("=" * 60)
    print("EXPERIMENT 4: HEURISTIC SEARCH")
    print("=" * 60)
    start, goal = find_cell(GRID, "S"), find_cell(GRID, "G")
    print("Grid (S = start, G = goal, # = wall):")
    draw(GRID, [])
    print(f"Start = {start}, Goal = {goal}")
    print(f"Heuristic: Manhattan distance. h(start) = {manhattan(start, goal)}")

    print("\n--- 1. Breadth First Search (no heuristic) ---")
    path, expanded = bfs(GRID, start, goal)
    draw(GRID, path)
    print(f"   Path length = {len(path) - 1} moves, cells expanded = {expanded}, "
          f"valid = {path_is_valid(GRID, path, start, goal)}")

    print("\n--- 2. Hill climbing (heuristic, no backtracking) ---")
    path, stuck = hill_climbing(GRID, start, goal)
    draw(GRID, path)
    if stuck:
        print(f"   STUCK at {path[-1]} with h = {manhattan(path[-1], goal)}: every "
              "neighbour is worse (local minimum).")
        print("   Hill climbing failed because it never goes 'uphill' to get around the wall.")
    else:
        print(f"   Reached the goal in {len(path) - 1} moves.")

    print("\n--- 3. Greedy best-first search (heuristic + frontier) ---")
    path, expanded = greedy_best_first(GRID, start, goal)
    draw(GRID, path)
    print(f"   Path length = {len(path) - 1} moves, cells expanded = {expanded}, "
          f"valid = {path_is_valid(GRID, path, start, goal)}")
    print("   It keeps a frontier, so it backtracks out of the dead end and uses the gap.")


if __name__ == "__main__":
    main()
```

## Sample Input

No input needed - the maze is built into the program (7 rows x 11 columns, wall in column 6 with a gap in the bottom row).

## Expected Output

The outputs below were produced by actually running `main.py` (Python 3.12) with the inputs shown; text after each prompt is the input that was typed.

**Run (no input)**

```text
============================================================
EXPERIMENT 4: HEURISTIC SEARCH
============================================================
Grid (S = start, G = goal, # = wall):
   ...........
   ......#....
   ......#....
   .S....#.G..
   ......#....
   ......#....
   ...........
Start = (3, 1), Goal = (3, 8)
Heuristic: Manhattan distance. h(start) = 7

--- 1. Breadth First Search (no heuristic) ---
   .*******...
   .*....#*...
   .*....#*...
   .S....#*G..
   ......#....
   ......#....
   ...........
   Path length = 13 moves, cells expanded = 64, valid = True

--- 2. Hill climbing (heuristic, no backtracking) ---
   ...........
   ......#....
   ......#....
   .S****#.G..
   ......#....
   ......#....
   ...........
   STUCK at (3, 5) with h = 3: every neighbour is worse (local minimum).
   Hill climbing failed because it never goes 'uphill' to get around the wall.

--- 3. Greedy best-first search (heuristic + frontier) ---
   .....***...
   .....*#*...
   .....*#*...
   .S****#*G..
   ......#....
   ......#....
   ...........
   Path length = 13 moves, cells expanded = 22, valid = True
   It keeps a frontier, so it backtracks out of the dead end and uses the gap.
```

## Result

BFS finds a 13-move path after expanding 64 cells. Hill climbing gets **stuck** at the wall (local minimum). Greedy best-first search escapes through the gap, finds a 13-move path and expands only 22 cells, showing the benefit of the Manhattan-distance heuristic.

## How to Run

```bat
cd Experiment_04_Heuristic_Search
python main.py
```

From the project root you can also run `run_experiment.bat 4`.
