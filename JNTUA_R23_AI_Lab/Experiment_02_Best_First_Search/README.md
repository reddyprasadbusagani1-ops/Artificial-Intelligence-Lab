# Experiment 2: Greedy Best First Search

**Artificial Intelligence Lab | Subject Code 23A31301P | JNTUA R23 | B.Tech AI & DS**

## Aim

To implement greedy best-first search using heuristic values, display the search steps and the path found, and compare its cost with the optimal cost.

## Theory

Best-first search is an **informed** search. Each node n has a heuristic value h(n) estimating how far it is from the goal. **Greedy** best-first search keeps a priority queue (the *frontier*) and always expands the node with the **smallest h(n)**.

* It is usually fast because it heads straight toward the goal.
* It **ignores the cost already paid**, so the path it finds is **not guaranteed to be optimal**.
* It is not guaranteed to be optimal, and in infinite spaces it may not be complete; with a visited set on a finite graph it always terminates.

The program prints the cost of the greedy path and compares it with the optimal cost found by Dijkstra's algorithm so the difference is visible.

## Algorithm / Procedure

1. Put the start node in a priority queue ordered by h(n).
2. Repeat while the queue is not empty:
   1. Remove the node with the **smallest h**; record it as expanded.
   2. If it is the goal, rebuild the path from parent links and stop.
   3. For each undiscovered neighbour: set its parent and insert it into the queue with its h value.
3. If the queue becomes empty, the goal is unreachable.
4. Compute the path cost and compare with Dijkstra's optimal cost.

## Source Code

The complete program is in [`main.py`](main.py) and is reproduced here.

```python
"""
Experiment 2: Greedy Best First Search
Subject: Artificial Intelligence Lab (23A31301P) - JNTUA R23

Greedy best-first search always expands the frontier node with the
SMALLEST heuristic value h(n) (estimated distance to the goal).
It ignores the cost already paid, so it is fast but NOT always optimal.
"""

import heapq
import itertools

GOAL = "G"

# Weighted undirected graph: node -> {neighbour: edge cost}
GRAPH = {
    "S": {"A": 2, "B": 5},
    "A": {"S": 2, "C": 3, "D": 3},
    "B": {"S": 5, "E": 4, "F": 6},
    "C": {"A": 3},
    "D": {"A": 3, "G": 4},
    "E": {"B": 4, "H": 3},
    "F": {"B": 6, "G": 7},
    "H": {"E": 3, "G": 5},
    "G": {"D": 4, "F": 7, "H": 5},
    "Z": {},                       # isolated node: goal is unreachable from here
}

# Heuristic: estimated remaining distance from each node to the goal G
HEURISTIC = {"S": 10, "A": 8, "B": 6, "C": 9, "D": 5,
             "E": 4, "F": 3, "H": 2, "G": 0, "Z": 7}


def ask(prompt, default):
    try:
        text = input(prompt).strip()
    except EOFError:
        return default
    return text if text else default


def greedy_best_first(graph, h, start, goal, show_steps=True):
    """Return (path, expanded nodes). path is None when the goal is unreachable."""
    counter = itertools.count()                     # tie-breaker for equal h values
    frontier = [(h[start], next(counter), start)]   # priority queue ordered by h
    discovered = {start}
    parent = {start: None}
    expanded = []

    while frontier:
        h_value, _, node = heapq.heappop(frontier)  # smallest h first
        expanded.append(node)
        if show_steps:
            waiting = sorted((h[n], n) for _, _, n in frontier)
            print(f"  Expand {node} (h={h_value}); frontier before expanding: "
                  f"{[(n, v) for v, n in sorted([(h_value, node)] + waiting)]}")
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], expanded
        for neighbour in graph[node]:
            if neighbour not in discovered:
                discovered.add(neighbour)
                parent[neighbour] = node
                heapq.heappush(frontier, (h[neighbour], next(counter), neighbour))
    return None, expanded


def dijkstra_cost(graph, start, goal):
    """Optimal cost (for comparison only, to show greedy is not always optimal)."""
    best = {start: 0}
    queue = [(0, start)]
    while queue:
        cost, node = heapq.heappop(queue)
        if node == goal:
            return cost
        if cost > best.get(node, float("inf")):
            continue
        for neighbour, edge in graph[node].items():
            new_cost = cost + edge
            if new_cost < best.get(neighbour, float("inf")):
                best[neighbour] = new_cost
                heapq.heappush(queue, (new_cost, neighbour))
    return None


def path_cost(graph, path):
    """Add up edge costs; raises KeyError if the path uses a non-existent edge."""
    return sum(graph[a][b] for a, b in zip(path, path[1:]))


def main():
    print("=" * 60)
    print("EXPERIMENT 2: GREEDY BEST FIRST SEARCH")
    print("=" * 60)
    print(f"Goal node: {GOAL}")
    print("Heuristic values h(n):", HEURISTIC)

    while True:
        start = ask("\nEnter start node [S] (Z shows an unreachable case): ", "S").upper()
        if start in GRAPH:
            break
        print(f"  Invalid node. Valid nodes: {', '.join(sorted(GRAPH))}")

    print(f"\nSearching from {start} to {GOAL}:")
    path, expanded = greedy_best_first(GRAPH, HEURISTIC, start, GOAL)

    print(f"\nNodes expanded in order: {' -> '.join(expanded)}")
    if path is None:
        print(f"Goal {GOAL} is NOT reachable from {start}.")
        return
    cost = path_cost(GRAPH, path)
    print(f"Path found by greedy search: {' -> '.join(path)}  (cost = {cost})")
    best = dijkstra_cost(GRAPH, start, GOAL)
    print(f"Optimal cost (Dijkstra, for comparison): {best}")
    if cost > best:
        print("Note: greedy search is fast but did NOT find the cheapest path.")
    else:
        print("Greedy search happened to find an optimal path here.")


if __name__ == "__main__":
    main()
```

## Sample Input

Start node `S` (default). Goal is fixed as `G` because the heuristic values were written for goal G. Enter `Z` as the start to see an unreachable case.

## Expected Output

The outputs below were produced by actually running `main.py` (Python 3.12) with the inputs shown; text after each prompt is the input that was typed.

**Default input (start S)**

```text
============================================================
EXPERIMENT 2: GREEDY BEST FIRST SEARCH
============================================================
Goal node: G
Heuristic values h(n): {'S': 10, 'A': 8, 'B': 6, 'C': 9, 'D': 5, 'E': 4, 'F': 3, 'H': 2, 'G': 0, 'Z': 7}

Enter start node [S] (Z shows an unreachable case): 

Searching from S to G:
  Expand S (h=10); frontier before expanding: [('S', 10)]
  Expand B (h=6); frontier before expanding: [('B', 6), ('A', 8)]
  Expand F (h=3); frontier before expanding: [('F', 3), ('E', 4), ('A', 8)]
  Expand G (h=0); frontier before expanding: [('G', 0), ('E', 4), ('A', 8)]

Nodes expanded in order: S -> B -> F -> G
Path found by greedy search: S -> B -> F -> G  (cost = 18)
Optimal cost (Dijkstra, for comparison): 9
Note: greedy search is fast but did NOT find the cheapest path.
```

**Unreachable case (start Z)**

```text
============================================================
EXPERIMENT 2: GREEDY BEST FIRST SEARCH
============================================================
Goal node: G
Heuristic values h(n): {'S': 10, 'A': 8, 'B': 6, 'C': 9, 'D': 5, 'E': 4, 'F': 3, 'H': 2, 'G': 0, 'Z': 7}

Enter start node [S] (Z shows an unreachable case): Z

Searching from Z to G:
  Expand Z (h=7); frontier before expanding: [('Z', 7)]

Nodes expanded in order: Z
Goal G is NOT reachable from Z.
```

## Result

Greedy best-first search finds S -> B -> F -> G with cost 18, whereas the optimal cost is 9. This shows the speed of heuristic search and its lack of optimality. An unreachable start (Z) is reported correctly.

## How to Run

```bat
cd Experiment_02_Best_First_Search
python main.py
```

From the project root you can also run `run_experiment.bat 2`.
