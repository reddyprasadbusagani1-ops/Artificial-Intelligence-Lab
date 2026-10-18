# Experiment 7: Minimax with Alpha-Beta Pruning

**Artificial Intelligence Lab | Subject Code 23A31301P | JNTUA R23 | B.Tech AI & DS**

## Aim

To implement the minimax algorithm with alpha-beta pruning and display the best value, the visited nodes and the pruning information.

## Theory

**Minimax** is used in two-player zero-sum games. MAX tries to maximise the value, MIN tries to minimise it, and the values of leaves are propagated up the game tree.

**Alpha-beta pruning** keeps two bounds: **alpha** = best value MAX can already guarantee, **beta** = best value MIN can already guarantee. When **alpha >= beta**, the remaining children of the current node cannot influence the final decision and are **pruned** (not evaluated). The result is identical to minimax, but fewer nodes are visited (best case about the square root of the nodes of plain minimax).

## Algorithm / Procedure

1. Represent the game tree as nested lists (a number = leaf).
2. `alpha_beta(node, is_max, alpha, beta)`:
   1. If node is a leaf, record it as visited and return its value.
   2. For each child: compute its value recursively.
   3. At a MAX node raise alpha = max(alpha, best); at a MIN node lower beta = min(beta, best).
   4. If alpha >= beta, record a pruning message for the remaining children and stop the loop.
3. Return the best value found.
4. Verify by running plain minimax and comparing the root values.

## Source Code

The complete program is in [`main.py`](main.py) and is reproduced here.

```python
"""
Experiment 7: Minimax with Alpha-Beta Pruning
Subject: Artificial Intelligence Lab (23A31301P) - JNTUA R23

Minimax: MAX picks the child with the highest value, MIN the lowest.
Alpha  = best value MAX can already guarantee on the path to the root.
Beta   = best value MIN can already guarantee on the path to the root.
If alpha >= beta, the remaining children cannot change the result and are PRUNED.
Alpha-beta always returns the same value as plain minimax, but visits fewer nodes.

The game tree is written as nested lists: a number is a leaf value,
a list is an internal node whose items are its children.
"""

import ast

INF = float("inf")

# Depth-3 tree: root (MAX) -> MIN nodes -> MAX nodes -> leaves
SAMPLE_TREE = [[[3, 5], [6, 9]], [[1, 2], [0, -1]]]


def ask(prompt, default):
    try:
        text = input(prompt).strip()
    except EOFError:
        return default
    return text if text else default


def is_valid_tree(node):
    """A valid tree is a number, or a non-empty list of valid trees."""
    if isinstance(node, bool):
        return False
    if isinstance(node, (int, float)):
        return True
    return isinstance(node, list) and len(node) > 0 and all(is_valid_tree(c) for c in node)


def count_leaves(node):
    return 1 if not isinstance(node, list) else sum(count_leaves(c) for c in node)


def minimax(node, is_max):
    """Plain minimax (no pruning). Used to double-check the alpha-beta result."""
    if not isinstance(node, list):
        return node
    values = [minimax(child, not is_max) for child in node]
    return max(values) if is_max else min(values)


def alpha_beta(node, name, is_max, alpha, beta, info):
    """Alpha-beta search. info collects visited leaves and pruning messages."""
    if not isinstance(node, list):                 # leaf: just return its value
        info["visited"].append((name, node))
        return node

    best = -INF if is_max else INF
    role = "MAX" if is_max else "MIN"
    for index, child in enumerate(node):
        child_name = f"{name}.{index}"
        value = alpha_beta(child, child_name, not is_max, alpha, beta, info)
        if is_max:
            best = max(best, value)
            alpha = max(alpha, best)               # MAX raises alpha
        else:
            best = min(best, value)
            beta = min(beta, best)                 # MIN lowers beta
        if alpha >= beta:                          # cut-off condition
            skipped = node[index + 1:]
            if skipped:
                info["pruned"].append(
                    f"At {role} node {name}: alpha={alpha}, beta={beta} after child "
                    f"{child_name}; pruned {len(skipped)} remaining child(ren) "
                    f"({count_leaves(skipped)} leaves skipped)")
                info["skipped_leaves"] += count_leaves(skipped)
            break
    return best


def read_tree():
    """Let the user type their own tree, or press Enter for the sample tree."""
    text = ask("\nEnter a tree as nested lists (e.g. [[3,5],[2,9]]) or press Enter "
               "for the sample: ", "")
    if not text:
        return SAMPLE_TREE
    try:
        tree = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        print("  Could not read that tree. Using the sample tree instead.")
        return SAMPLE_TREE
    if not is_valid_tree(tree) or not isinstance(tree, list):
        print("  Invalid tree (use non-empty nested lists of numbers). Using the sample tree.")
        return SAMPLE_TREE
    return tree


def main():
    print("=" * 60)
    print("EXPERIMENT 7: MINIMAX WITH ALPHA-BETA PRUNING")
    print("=" * 60)
    tree = read_tree()
    print("Game tree:", tree)
    print("Root is a MAX node; levels alternate MAX, MIN, MAX, ...")

    info = {"visited": [], "pruned": [], "skipped_leaves": 0}
    best_value = alpha_beta(tree, "R", True, -INF, INF, info)

    print(f"\nBest value at the root (alpha-beta) : {best_value}")
    print(f"Leaf nodes visited ({len(info['visited'])}):")
    print("   " + ", ".join(f"{name}={value}" for name, value in info["visited"]))
    print(f"Total leaves in tree        : {count_leaves(tree)}")
    print(f"Leaves skipped due to pruning: {info['skipped_leaves']}")
    print("\nPruning information:")
    if info["pruned"]:
        for message in info["pruned"]:
            print("   " + message)
    else:
        print("   No pruning happened for this tree.")

    plain = minimax(tree, True)
    print(f"\nCheck: plain minimax value = {plain}; "
          f"alpha-beta matches minimax = {plain == best_value}")


if __name__ == "__main__":
    main()
```

## Sample Input

Press Enter to use the sample tree `[[[3,5],[6,9]],[[1,2],[0,-1]]]`, or type your own nested list such as `[[3,5],[2,9]]`. Invalid text falls back to the sample tree.

## Expected Output

The outputs below were produced by actually running `main.py` (Python 3.12) with the inputs shown; text after each prompt is the input that was typed.

**Sample tree (Enter)**

```text
============================================================
EXPERIMENT 7: MINIMAX WITH ALPHA-BETA PRUNING
============================================================

Enter a tree as nested lists (e.g. [[3,5],[2,9]]) or press Enter for the sample: 
Game tree: [[[3, 5], [6, 9]], [[1, 2], [0, -1]]]
Root is a MAX node; levels alternate MAX, MIN, MAX, ...

Best value at the root (alpha-beta) : 5
Leaf nodes visited (5):
   R.0.0.0=3, R.0.0.1=5, R.0.1.0=6, R.1.0.0=1, R.1.0.1=2
Total leaves in tree        : 8
Leaves skipped due to pruning: 3

Pruning information:
   At MAX node R.0.1: alpha=6, beta=5 after child R.0.1.0; pruned 1 remaining child(ren) (1 leaves skipped)
   At MIN node R.1: alpha=5, beta=2 after child R.1.0; pruned 1 remaining child(ren) (2 leaves skipped)

Check: plain minimax value = 5; alpha-beta matches minimax = True
```

**Custom tree [[3,5],[2,9]]**

```text
============================================================
EXPERIMENT 7: MINIMAX WITH ALPHA-BETA PRUNING
============================================================

Enter a tree as nested lists (e.g. [[3,5],[2,9]]) or press Enter for the sample: [[3,5],[2,9]]
Game tree: [[3, 5], [2, 9]]
Root is a MAX node; levels alternate MAX, MIN, MAX, ...

Best value at the root (alpha-beta) : 3
Leaf nodes visited (3):
   R.0.0=3, R.0.1=5, R.1.0=2
Total leaves in tree        : 4
Leaves skipped due to pruning: 1

Pruning information:
   At MIN node R.1: alpha=3, beta=2 after child R.1.0; pruned 1 remaining child(ren) (1 leaves skipped)

Check: plain minimax value = 3; alpha-beta matches minimax = True
```

**Invalid tree text**

```text
============================================================
EXPERIMENT 7: MINIMAX WITH ALPHA-BETA PRUNING
============================================================

Enter a tree as nested lists (e.g. [[3,5],[2,9]]) or press Enter for the sample: []
  Invalid tree (use non-empty nested lists of numbers). Using the sample tree.
Game tree: [[[3, 5], [6, 9]], [[1, 2], [0, -1]]]
Root is a MAX node; levels alternate MAX, MIN, MAX, ...

Best value at the root (alpha-beta) : 5
Leaf nodes visited (5):
   R.0.0.0=3, R.0.0.1=5, R.0.1.0=6, R.1.0.0=1, R.1.0.1=2
Total leaves in tree        : 8
Leaves skipped due to pruning: 3

Pruning information:
   At MAX node R.0.1: alpha=6, beta=5 after child R.0.1.0; pruned 1 remaining child(ren) (1 leaves skipped)
   At MIN node R.1: alpha=5, beta=2 after child R.1.0; pruned 1 remaining child(ren) (2 leaves skipped)

Check: plain minimax value = 5; alpha-beta matches minimax = True
```

## Result

The best value at the root is 5. Only 5 of the 8 leaves are evaluated; 3 leaves are pruned (one under the MAX node R.0.1 and two under the MIN node R.1). The alpha-beta value matches plain minimax.

## How to Run

```bat
cd Experiment_07_Alpha_Beta_Pruning
python main.py
```

From the project root you can also run `run_experiment.bat 7`.
