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
