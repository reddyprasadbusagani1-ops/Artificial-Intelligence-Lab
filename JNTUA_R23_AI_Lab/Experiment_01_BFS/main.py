"""
Experiment 1: Breadth First Search (BFS)
Subject: Artificial Intelligence Lab (23A31301P) - JNTUA R23

BFS visits nodes level by level using a FIFO queue.
Because it explores all nodes at distance k before distance k+1,
it also finds the path with the FEWEST EDGES in an unweighted graph.
"""

from collections import deque

# Undirected sample graph (adjacency list). G-H is a separate component,
# used to show what happens when a node cannot be reached.
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
    """Read a line of input; return default if the user presses Enter or input ends."""
    try:
        text = input(prompt).strip()
    except EOFError:
        return default
    return text if text else default


def ask_node(prompt, default, graph):
    """Keep asking until the user types a node that exists in the graph."""
    while True:
        node = ask(prompt, default).upper()
        if node in graph:
            return node
        print(f"  Invalid node '{node}'. Valid nodes: {', '.join(sorted(graph))}")


def bfs(graph, start):
    """Return (visit order, parent map, level map) for BFS from start."""
    visited = {start}              # nodes already put in the queue
    queue = deque([start])         # FIFO queue of nodes waiting to be expanded
    order = []                     # order in which nodes are visited
    parent = {start: None}         # remembers how we reached each node
    level = {start: 0}             # number of edges from the start node

    while queue:
        node = queue.popleft()     # take the OLDEST node (front of queue)
        order.append(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                parent[neighbour] = node
                level[neighbour] = level[node] + 1
                queue.append(neighbour)   # add to the BACK of the queue
    return order, parent, level


def build_path(parent, goal):
    """Follow parent links backwards from goal to start. None if goal unreachable."""
    if goal not in parent:
        return None
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


def path_is_valid(graph, path):
    """Check that every consecutive pair in the path is really an edge."""
    return all(b in graph[a] for a, b in zip(path, path[1:]))


def main():
    print("=" * 60)
    print("EXPERIMENT 1: BREADTH FIRST SEARCH (BFS)")
    print("=" * 60)
    print("Graph (adjacency list):")
    for node, neighbours in GRAPH.items():
        print(f"  {node} -> {neighbours}")

    start = ask_node("\nEnter start node [A]: ", "A", GRAPH)
    goal = ask_node("Enter goal node  [F]: ", "F", GRAPH)

    order, parent, level = bfs(GRAPH, start)

    print(f"\nBFS traversal order from {start}: {' -> '.join(order)}")
    print("Level of each visited node:",
          ", ".join(f"{n}={level[n]}" for n in order))

    unreached = [n for n in GRAPH if n not in order]
    if unreached:
        print("Nodes not reachable from the start:", ", ".join(unreached))

    path = build_path(parent, goal)
    if path is None:
        print(f"\nGoal {goal} is NOT reachable from {start}.")
    else:
        print(f"\nShortest path (fewest edges) {start} to {goal}: {' -> '.join(path)}")
        print(f"Number of edges: {len(path) - 1}")
        print("Path check (every step is a real edge):", path_is_valid(GRAPH, path))


if __name__ == "__main__":
    main()
