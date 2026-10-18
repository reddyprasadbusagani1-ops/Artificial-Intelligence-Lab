"""
Experiment 6: Water Jug Problem (state-space search)
Subject: Artificial Intelligence Lab (23A31301P) - JNTUA R23

State  : (x, y) = litres of water in jug 1 and jug 2.
Start  : (0, 0)  - both jugs empty.
Goal   : either jug contains exactly the target amount.
Rules  : fill a jug, empty a jug, pour one jug into the other
         (until the source is empty or the destination is full).
BFS explores the state space, so the solution has the FEWEST steps.
"""

from collections import deque
from math import gcd


def ask(prompt, default):
    try:
        text = input(prompt).strip()
    except EOFError:
        return default
    return text if text else default


def ask_positive_int(prompt, default, allow_zero=False):
    """Keep asking until the user enters a valid whole number."""
    while True:
        text = ask(prompt, str(default))
        if text.isdigit() and (int(text) > 0 or allow_zero):
            return int(text)
        print("  Please enter a positive whole number.")


def successors(state, cap1, cap2):
    """Return a list of (action description, new state) reachable in one step."""
    x, y = state
    result = [
        ("Fill jug 1", (cap1, y)),
        ("Fill jug 2", (x, cap2)),
        ("Empty jug 1", (0, y)),
        ("Empty jug 2", (x, 0)),
    ]
    pour = min(x, cap2 - y)                      # amount poured from jug 1 to jug 2
    result.append((f"Pour jug 1 into jug 2 ({pour} L)", (x - pour, y + pour)))
    pour = min(y, cap1 - x)                      # amount poured from jug 2 to jug 1
    result.append((f"Pour jug 2 into jug 1 ({pour} L)", (x + pour, y - pour)))
    return result


def solve(cap1, cap2, target):
    """BFS over states. Returns list of (action, state) from the start, or None."""
    start = (0, 0)
    queue = deque([start])
    parent = {start: (None, None)}               # state -> (previous state, action)
    while queue:
        state = queue.popleft()
        if target in state:                      # goal test
            steps = []
            while state is not None:
                previous, action = parent[state]
                steps.append((action, state))
                state = previous
            return steps[::-1]
        for action, new_state in successors(state, cap1, cap2):
            if new_state not in parent:
                parent[new_state] = (state, action)
                queue.append(new_state)
    return None


def solution_is_valid(steps, cap1, cap2, target):
    """Replay every step and make sure it follows the rules and reaches the goal."""
    if steps[0][1] != (0, 0) or target not in steps[-1][1]:
        return False
    for (_, before), (_, after) in zip(steps, steps[1:]):
        if after not in [s for _, s in successors(before, cap1, cap2)]:
            return False
        if not (0 <= after[0] <= cap1 and 0 <= after[1] <= cap2):
            return False
    return True


def main():
    print("=" * 60)
    print("EXPERIMENT 6: WATER JUG PROBLEM")
    print("=" * 60)
    cap1 = ask_positive_int("Capacity of jug 1 [4]: ", 4)
    cap2 = ask_positive_int("Capacity of jug 2 [3]: ", 3)
    target = ask_positive_int("Target amount in litres [2]: ", 2)

    divisor = gcd(cap1, cap2)
    print(f"\nTheory check: gcd({cap1}, {cap2}) = {divisor}; target must be a multiple of "
          f"{divisor} and at most {max(cap1, cap2)}.")
    steps = solve(cap1, cap2, target)

    if steps is None:
        print(f"No solution: {target} litres cannot be measured with these jugs.")
        return

    print(f"\nSolution found in {len(steps) - 1} steps:")
    print(f"{'Step':<5}{'Jug1':<6}{'Jug2':<6}Action")
    for number, (action, (x, y)) in enumerate(steps):
        print(f"{number:<5}{x:<6}{y:<6}{action or 'Start (both jugs empty)'}")
    print("\nSolution check (all moves legal, goal reached):",
          solution_is_valid(steps, cap1, cap2, target))


if __name__ == "__main__":
    main()
