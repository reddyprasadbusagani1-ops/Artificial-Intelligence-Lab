# Experiment 3: Depth First Search (DFS)

**Artificial Intelligence Lab | Subject Code 23A31301P | JNTUA R23 | B.Tech AI & DS**

## Aim

To write a Python program that traverses a graph using Depth First Search (recursive and stack-based) and displays the traversal order and a path to the goal.

## Theory

DFS is an **uninformed** search that goes as deep as possible along a branch before **backtracking**. It uses a **stack** (LIFO) - either an explicit stack or the recursion call stack.

* Memory use is small: proportional to the depth of the search.
* The path it finds is **not necessarily the shortest**.
* Time: O(V + E). A visited set is needed to avoid looping in graphs with cycles.

## Algorithm / Procedure

**Recursive version**
1. Mark the current node visited and add it to the order.
2. For each unvisited neighbour (in list order), call DFS on it.

**Stack version**
1. Push the start node on a stack.
2. Pop a node; if already visited, skip it; otherwise visit it.
3. Push its unvisited neighbours in **reverse** order (so the first neighbour is processed first).

**Path to goal:** run DFS and return the first path that reaches the goal; return "unreachable" if the search finishes without finding it.

## Source Code

The complete program is in [`main.py`](main.py) and is reproduced here.

```python
"""
Experiment 3: Depth First Search (DFS)
Subject: Artificial Intelligence Lab (23A31301P) - JNTUA R23

DFS goes as deep as possible along one branch before backtracking.
It uses a STACK (explicitly, or implicitly through recursion).
It finds A path, but not necessarily the shortest one.
"""

GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
    "G": ["H"],
    "H": ["G"],
}


def ask(prompt, default):
    try:
        text = input(prompt).strip()
    except EOFError:
        return default
    return text if text else default


def ask_node(prompt, default, graph):
    while True:
        node = ask(prompt, default).upper()
        if node in graph:
            return node
        print(f"  Invalid node '{node}'. Valid nodes: {', '.join(sorted(graph))}")


def dfs_recursive(graph, node, visited=None, order=None):
    """Recursive DFS: the Python call stack acts as the DFS stack."""
    if visited is None:
        visited, order = set(), []
    visited.add(node)
    order.append(node)
    for neighbour in graph[node]:
        if neighbour not in visited:
            dfs_recursive(graph, neighbour, visited, order)
    return order


def dfs_iterative(graph, start):
    """Iterative DFS with an explicit stack. Returns (order, parent map)."""
    stack = [start]
    visited = set()
    order = []
    parent = {start: None}
    while stack:
        node = stack.pop()                     # LAST pushed node is expanded first
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        # push neighbours in reverse so that the first neighbour is popped first
        for neighbour in reversed(graph[node]):
            if neighbour not in visited:
                if neighbour not in parent:
                    parent[neighbour] = node
                stack.append(neighbour)
    return order, parent


def dfs_path(graph, start, goal):
    """Find one path from start to goal using DFS (None if unreachable)."""
    def visit(node, visited):
        visited.add(node)
        if node == goal:
            return [node]
        for neighbour in graph[node]:
            if neighbour not in visited:
                rest = visit(neighbour, visited)
                if rest is not None:
                    return [node] + rest
        return None
    return visit(start, set())


def main():
    print("=" * 60)
    print("EXPERIMENT 3: DEPTH FIRST SEARCH (DFS)")
    print("=" * 60)
    print("Graph (adjacency list):")
    for node, neighbours in GRAPH.items():
        print(f"  {node} -> {neighbours}")

    start = ask_node("\nEnter start node [A]: ", "A", GRAPH)
    goal = ask_node("Enter goal node  [F]: ", "F", GRAPH)

    recursive_order = dfs_recursive(GRAPH, start)
    iterative_order, _ = dfs_iterative(GRAPH, start)

    print(f"\nDFS traversal (recursive): {' -> '.join(recursive_order)}")
    print(f"DFS traversal (stack)    : {' -> '.join(iterative_order)}")
    print("Both versions give the same order:", recursive_order == iterative_order)

    path = dfs_path(GRAPH, start, goal)
    if path is None:
        print(f"\nGoal {goal} is NOT reachable from {start}.")
    else:
        valid = all(b in GRAPH[a] for a, b in zip(path, path[1:]))
        print(f"\nA path found by DFS from {start} to {goal}: {' -> '.join(path)}")
        print("Path check (every step is a real edge):", valid)
        print("(DFS returns the first path it finds, which may be longer than the shortest.)")


if __name__ == "__main__":
    main()
```

## Sample Input

Start node `A`, goal node `F` (defaults). Try start `A`, goal `H` for the unreachable case.

## Expected Output

The outputs below were produced by actually running `main.py` (Python 3.12) with the inputs shown; text after each prompt is the input that was typed.

**Default input (Enter, Enter)**

```text
============================================================
EXPERIMENT 3: DEPTH FIRST SEARCH (DFS)
============================================================
Graph (adjacency list):
  A -> ['B', 'C']
  B -> ['A', 'D', 'E']
  C -> ['A', 'F']
  D -> ['B']
  E -> ['B', 'F']
  F -> ['C', 'E']
  G -> ['H']
  H -> ['G']

Enter start node [A]: 
Enter goal node  [F]: 

DFS traversal (recursive): A -> B -> D -> E -> F -> C
DFS traversal (stack)    : A -> B -> D -> E -> F -> C
Both versions give the same order: True

A path found by DFS from A to F: A -> B -> E -> F
Path check (every step is a real edge): True
(DFS returns the first path it finds, which may be longer than the shortest.)
```

**Unreachable goal (A to H)**

```text
============================================================
EXPERIMENT 3: DEPTH FIRST SEARCH (DFS)
============================================================
Graph (adjacency list):
  A -> ['B', 'C']
  B -> ['A', 'D', 'E']
  C -> ['A', 'F']
  D -> ['B']
  E -> ['B', 'F']
  F -> ['C', 'E']
  G -> ['H']
  H -> ['G']

Enter start node [A]: A
Enter goal node  [F]: H

DFS traversal (recursive): A -> B -> D -> E -> F -> C
DFS traversal (stack)    : A -> B -> D -> E -> F -> C
Both versions give the same order: True

Goal H is NOT reachable from A.
```

## Result

DFS visits A -> B -> D -> E -> F -> C. The recursive and stack versions give identical orders, and the path found to F is a valid sequence of edges (it is longer than the BFS path, showing DFS does not guarantee the shortest path).

## How to Run

```bat
cd Experiment_03_DFS
python main.py
```

From the project root you can also run `run_experiment.bat 3`.
