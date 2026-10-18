# Experiment 5: A* and AO* Algorithms

**Artificial Intelligence Lab | Subject Code 23A31301P | JNTUA R23 | B.Tech AI & DS**

## Aim

To implement the A* shortest-path algorithm for an ordinary graph and the AO* algorithm for an AND-OR graph, and to clearly distinguish between them.

## Theory

**A\* search** works on an ordinary (OR) graph. It expands the node with the smallest **f(n) = g(n) + h(n)**, where g(n) is the cost from the start and h(n) is the estimated cost to the goal. If h never over-estimates (is *admissible*), A* returns an **optimal path**.

**AO\* search** works on an **AND-OR graph**, used for problem decomposition. A node can be solved by choosing **one** of several arcs:
* an **OR arc** has one child - solve that child;
* an **AND arc** has several children - **all** of them must be solved (and their costs add up).
The answer is not a path but a **solution graph**. The cost of a node is  min over arcs of  sum( edge cost + child cost ).

| | A* | AO* |
|---|---|---|
| Graph type | ordinary (OR) graph | AND-OR graph |
| Result | a single path | a solution graph (a tree of choices) |
| Cost rule | g(n) + h(n) | min over arcs of sum(edge + child cost) |
| Needs | admissible h | admissible h, **acyclic** graph (as implemented here) |

## Algorithm / Procedure

**A\***
1. Put the start node in the open list with f = h(start).
2. Remove the node with the smallest f. If it is the goal, rebuild the path and stop.
3. For each neighbour compute new g = g(node) + edge cost; if it is better than any known g, store it and insert it with f = g + h.
4. If the open list becomes empty, the goal is unreachable.

**AO\***
1. Start with the estimates h(n) for every node.
2. Follow the currently best arcs from the start node and find a tip node that is not yet expanded and not solved.
3. **Expand** the tip: compute the cost of each of its arcs from the estimates of its children and mark the cheapest arc.
4. **Revise (back-propagate):** recompute cost, best arc and solved status of all expanded nodes until nothing changes. A node is *solved* when all children of its best arc are solved.
5. Repeat from step 2 until the start node is solved (or its cost becomes infinite = no solution).
6. Report the cost and the solution graph (chosen arc of each node in the solution).

## Source Code

The complete program is in [`main.py`](main.py) and is reproduced here.

```python
"""
Experiment 5: A* Algorithm and AO* Algorithm
Subject: Artificial Intelligence Lab (23A31301P) - JNTUA R23

A*  : searches an ORDINARY graph (OR graph). Result = a single PATH.
      f(n) = g(n) + h(n)   g = cost so far, h = estimated cost to goal.
AO* : searches an AND-OR graph. Result = a SOLUTION GRAPH (a tree of choices).
      An AND arc needs ALL of its child nodes solved; OR arcs need only ONE.
      Cost of a node = min over its arcs of  sum(edge cost + child cost).

Both need h to be OPTIMISTIC (never over-estimate) to guarantee optimal answers.
The AO* version here is for acyclic AND-OR graphs.
"""

import heapq
import itertools

INF = float("inf")


# ----------------------------------------------------------------------
#                              PART A : A*
# ----------------------------------------------------------------------
ASTAR_GRAPH = {
    "S": {"A": 1, "B": 4},
    "A": {"S": 1, "B": 2, "C": 5, "D": 12},
    "B": {"S": 4, "A": 2, "C": 2},
    "C": {"A": 5, "B": 2, "D": 3, "G": 7},
    "D": {"A": 12, "C": 3, "G": 3},
    "G": {"C": 7, "D": 3},
    "X": {},                           # isolated node used for the unreachable demo
}
# Admissible heuristic: never larger than the true remaining cost to G
ASTAR_H = {"S": 7, "A": 6, "B": 4, "C": 4, "D": 2, "G": 0, "X": 0}


def a_star(graph, h, start, goal):
    """Return (path, cost, expanded list) or (None, None, expanded) if unreachable."""
    counter = itertools.count()
    open_list = [(h[start], next(counter), 0, start)]   # entries: (f, tie, g, node)
    best_g = {start: 0}
    parent = {start: None}
    closed = set()
    expanded = []

    while open_list:
        f, _, g, node = heapq.heappop(open_list)        # smallest f = g + h
        if node in closed:
            continue
        closed.add(node)
        expanded.append((node, g, h[node], f))
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], g, expanded
        for neighbour, edge_cost in graph[node].items():
            new_g = g + edge_cost
            if new_g < best_g.get(neighbour, INF):      # found a cheaper way
                best_g[neighbour] = new_g
                parent[neighbour] = node
                heapq.heappush(open_list,
                               (new_g + h[neighbour], next(counter), new_g, neighbour))
    return None, None, expanded


def uniform_cost(graph, start, goal):
    """Plain Dijkstra, used only to double-check that A* is optimal."""
    best = {start: 0}
    queue = [(0, start)]
    while queue:
        cost, node = heapq.heappop(queue)
        if node == goal:
            return cost
        if cost > best.get(node, INF):
            continue
        for neighbour, edge in graph[node].items():
            if cost + edge < best.get(neighbour, INF):
                best[neighbour] = cost + edge
                heapq.heappush(queue, (cost + edge, neighbour))
    return None


# ----------------------------------------------------------------------
#                             PART B : AO*
# ----------------------------------------------------------------------
# AND-OR graph: node -> list of ARCS. Each arc is a list of (child, edge_cost).
#   An arc with ONE child is an OR choice.
#   An arc with SEVERAL children is an AND arc (all children must be solved).
# Nodes that do not appear as keys are terminal (leaf) nodes.
AO_GRAPH = {
    "A": [[("B", 1)], [("C", 1), ("D", 1)]],   # A via B   OR   A via (C AND D)
    "B": [[("E", 1)], [("F", 1)]],             # B via E   OR   B via F
    "C": [[("G", 1)], [("H", 1)]],             # C via G   OR   C via H
    "D": [[("H", 1), ("I", 1)]],               # D via (H AND I)
}
# Heuristic estimates. For leaves this is their true cost. For inner nodes it is an
# optimistic (never too high) estimate used until the node has been expanded.
AO_H = {"A": 5, "B": 4, "C": 2, "D": 3,
        "E": 10, "F": 9, "G": 5, "H": 2, "I": 1}

# A second graph in which the only leaf has infinite cost (unsolvable)
AO_GRAPH_UNSOLVABLE = {"P": [[("Q", 1)], [("R", 2), ("S", 1)]]}
AO_H_UNSOLVABLE = {"P": 1, "Q": INF, "R": 1, "S": INF}


def arc_cost(arc, estimate):
    """Cost of one arc = sum over children of (edge cost + current estimate of child)."""
    return sum(edge + estimate[child] for child, edge in arc)


def ao_star(graph, h, start, verbose=True):
    """
    AO* for an acyclic AND-OR graph.
    Returns (cost, best_arc dict, solved flag, expansion order).

    Steps repeated until the start node is SOLVED (or proven unsolvable):
      1. Follow the currently best arcs from the start to find a tip node that
         is not yet expanded and not solved.
      2. EXPAND it: compute its cost from its arcs (using the h values of its
         children) and mark its cheapest arc.
      3. REVISE (back-propagate): recompute cost / best arc / solved status of
         every expanded node, repeating until nothing changes.
    """
    estimate = dict(h)       # current cost estimates
    best_arc = {}            # node -> index of its currently best arc
    expanded = []            # nodes in the order they were expanded
    solved = {n for n in estimate if n not in graph and estimate[n] < INF}

    def tips_of_best_graph():
        """Nodes of the current best partial solution graph, in DFS order."""
        seen, order = set(), []

        def visit(node):
            if node in seen:
                return
            seen.add(node)
            order.append(node)
            if node in best_arc:                       # expanded: follow its best arc
                for child, _ in graph[node][best_arc[node]]:
                    visit(child)
        visit(start)
        return order

    def revise():
        """Back-propagate costs through all expanded nodes until stable."""
        changed = True
        while changed:
            changed = False
            for node in reversed(expanded):
                costs = [arc_cost(arc, estimate) for arc in graph[node]]
                new_index = min(range(len(costs)), key=lambda i: costs[i])
                new_cost = costs[new_index]
                arc = graph[node][new_index]
                new_solved = new_cost < INF and all(c in solved for c, _ in arc)
                if (new_cost != estimate[node] or best_arc.get(node) != new_index
                        or (new_solved and node not in solved)):
                    estimate[node], best_arc[node] = new_cost, new_index
                    if new_solved:
                        solved.add(node)
                    changed = True

    step = 0
    while start not in solved and estimate[start] < INF:
        candidates = [n for n in tips_of_best_graph()
                      if n not in solved and n not in best_arc]
        if not candidates:           # safety net: should not happen on an acyclic graph
            break
        node = candidates[0]
        expanded.append(node)
        estimate.setdefault(node, 0)
        step += 1
        # expansion: choose the cheapest arc using the children's current estimates
        costs = [arc_cost(arc, estimate) for arc in graph[node]]
        best_arc[node] = min(range(len(costs)), key=lambda i: costs[i])
        estimate[node] = costs[best_arc[node]]
        revise()
        if verbose:
            print(f"  Step {step}: expanded {node:>2}; best arc of {node} = "
                  f"{describe_arc(graph[node][best_arc[node]])}; "
                  f"cost estimate of start {start} = {estimate[start]}")
    return estimate[start], best_arc, start in solved, expanded


def describe_arc(arc):
    if len(arc) == 1:
        return f"OR -> {arc[0][0]}"
    return "AND -> (" + " AND ".join(child for child, _ in arc) + ")"


def solution_graph(graph, best_arc, start):
    """List of (node, chosen arc) pairs forming the final solution graph."""
    result, seen = [], set()

    def visit(node):
        if node in seen:
            return
        seen.add(node)
        if node in graph:
            arc = graph[node][best_arc[node]]
            result.append((node, arc))
            for child, _ in arc:
                visit(child)
    visit(start)
    return result


def exact_cost(graph, h, node, memo=None):
    """Brute-force optimal cost by full recursion (used only as a correctness check)."""
    memo = {} if memo is None else memo
    if node not in graph:
        return h[node]
    if node not in memo:
        memo[node] = min(sum(e + exact_cost(graph, h, c, memo) for c, e in arc)
                         for arc in graph[node])
    return memo[node]


def main():
    print("=" * 60)
    print("EXPERIMENT 5: A* AND AO* ALGORITHMS")
    print("=" * 60)

    print("\nPART A: A* search (ordinary graph, result = a PATH)")
    print("-" * 60)
    print("Heuristic h(n):", {k: v for k, v in ASTAR_H.items() if k != "X"})
    path, cost, expanded = a_star(ASTAR_GRAPH, ASTAR_H, "S", "G")
    print("Expansion order  (node, g, h, f):")
    for node, g, h_value, f in expanded:
        print(f"   {node}: g={g}, h={h_value}, f={f}")
    print(f"Optimal path: {' -> '.join(path)}   total cost = {cost}")
    check = uniform_cost(ASTAR_GRAPH, "S", "G")
    recomputed = sum(ASTAR_GRAPH[a][b] for a, b in zip(path, path[1:]))
    print(f"Check: Dijkstra cost = {check}, recomputed path cost = {recomputed}, "
          f"A* optimal = {cost == check == recomputed}")
    path, cost, _ = a_star(ASTAR_GRAPH, ASTAR_H, "S", "X")
    print("Unreachable goal X ->", "no path found" if path is None else path)

    print("\nPART B: AO* search (AND-OR graph, result = a SOLUTION GRAPH)")
    print("-" * 60)
    print("AND-OR graph (each arc: OR = single child, AND = several children):")
    for node, arcs in AO_GRAPH.items():
        print(f"   {node}: " + "  |  ".join(describe_arc(a) for a in arcs))
    print("Leaf costs:", {n: AO_H[n] for n in AO_H if n not in AO_GRAPH})
    print("Optimistic estimates for inner nodes:", {n: AO_H[n] for n in AO_GRAPH})
    print("\nAO* steps:")
    cost, best_arc, solved, order = ao_star(AO_GRAPH, AO_H, "A")
    print(f"\nExpansion order: {' , '.join(order)}")
    if solved:
        print(f"Minimum cost of solution graph for A = {cost}")
        print("Solution graph (node: chosen arc):")
        for node, arc in solution_graph(AO_GRAPH, best_arc, "A"):
            print(f"   {node}: {describe_arc(arc)}")
        brute = exact_cost(AO_GRAPH, AO_H, "A")
        print(f"Check: brute-force optimal cost = {brute}, AO* optimal = {cost == brute}")

    print("\nUnsolvable AND-OR graph demo:")
    cost, _, solved, _ = ao_star(AO_GRAPH_UNSOLVABLE, AO_H_UNSOLVABLE, "P", verbose=False)
    print("   Solved:", solved, "(every arc contains an unsolvable leaf)")

    print("\nDifference: A* returns one path through an OR graph; AO* returns a solution "
          "graph where AND arcs force several sub-problems to be solved together.")


if __name__ == "__main__":
    main()
```

## Sample Input

No input needed. A* runs on a 6-node weighted graph (S to G). AO* runs on the AND-OR graph printed by the program (nodes A-I).

## Expected Output

The outputs below were produced by actually running `main.py` (Python 3.12) with the inputs shown; text after each prompt is the input that was typed.

**Run (no input)**

```text
============================================================
EXPERIMENT 5: A* AND AO* ALGORITHMS
============================================================

PART A: A* search (ordinary graph, result = a PATH)
------------------------------------------------------------
Heuristic h(n): {'S': 7, 'A': 6, 'B': 4, 'C': 4, 'D': 2, 'G': 0}
Expansion order  (node, g, h, f):
   S: g=0, h=7, f=7
   A: g=1, h=6, f=7
   B: g=3, h=4, f=7
   C: g=5, h=4, f=9
   D: g=8, h=2, f=10
   G: g=11, h=0, f=11
Optimal path: S -> A -> B -> C -> D -> G   total cost = 11
Check: Dijkstra cost = 11, recomputed path cost = 11, A* optimal = True
Unreachable goal X -> no path found

PART B: AO* search (AND-OR graph, result = a SOLUTION GRAPH)
------------------------------------------------------------
AND-OR graph (each arc: OR = single child, AND = several children):
   A: OR -> B  |  AND -> (C AND D)
   B: OR -> E  |  OR -> F
   C: OR -> G  |  OR -> H
   D: AND -> (H AND I)
Leaf costs: {'E': 10, 'F': 9, 'G': 5, 'H': 2, 'I': 1}
Optimistic estimates for inner nodes: {'A': 5, 'B': 4, 'C': 2, 'D': 3}

AO* steps:
  Step 1: expanded  A; best arc of A = OR -> B; cost estimate of start A = 5
  Step 2: expanded  B; best arc of B = OR -> F; cost estimate of start A = 7
  Step 3: expanded  C; best arc of C = OR -> H; cost estimate of start A = 8
  Step 4: expanded  D; best arc of D = AND -> (H AND I); cost estimate of start A = 10

Expansion order: A , B , C , D
Minimum cost of solution graph for A = 10
Solution graph (node: chosen arc):
   A: AND -> (C AND D)
   C: OR -> H
   D: AND -> (H AND I)
Check: brute-force optimal cost = 10, AO* optimal = True

Unsolvable AND-OR graph demo:
   Solved: False (every arc contains an unsolvable leaf)

Difference: A* returns one path through an OR graph; AO* returns a solution graph where AND arcs force several sub-problems to be solved together.
```

## Result

A* returns the optimal path S -> A -> B -> C -> D -> G with cost 11 (confirmed against Dijkstra). AO* returns a solution graph of cost 10 in which A is solved through the **AND arc (C AND D)** - confirmed against a brute-force computation. An unsolvable AND-OR graph and an unreachable A* goal are both reported correctly.

## How to Run

```bat
cd Experiment_05_Astar_AOstar
python main.py
```

From the project root you can also run `run_experiment.bat 5`.
