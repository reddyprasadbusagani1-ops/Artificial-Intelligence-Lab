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
