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
