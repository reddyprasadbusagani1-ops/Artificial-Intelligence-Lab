# Experiment 6: Water Jug Problem

**Artificial Intelligence Lab | Subject Code 23A31301P | JNTUA R23 | B.Tech AI & DS**

## Aim

To solve the water jug problem using state-space search and display every state in the solution.

## Theory

A **state** is a pair (x, y): the litres in jug 1 and jug 2. The **initial state** is (0, 0). The **operators** are: fill a jug, empty a jug, pour jug 1 into jug 2, pour jug 2 into jug 1 (stopping when the source is empty or the target is full). The **goal** is any state where a jug holds exactly the target amount.

Breadth First Search over this state space finds a solution with the **minimum number of steps**. Number theory predicts solvability: a target T can be measured iff T is a multiple of gcd(capacity1, capacity2) and T <= max(capacity1, capacity2).

## Algorithm / Procedure

1. Read the two capacities and the target (reject non-numbers).
2. Put (0, 0) in a queue.
3. Remove a state; if either jug holds the target, rebuild the path using stored parents.
4. Generate the 6 successor states using the operators; add every state not seen before to the queue (remember its parent and the action used).
5. If the queue empties, the target cannot be measured.
6. Print the table of states and replay the solution to verify every move is legal.

## Source Code

The complete program is in [`main.py`](main.py) and is reproduced here.

```python
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
```

## Sample Input

Capacities 4 and 3, target 2 (press Enter three times). Also try 6, 4, target 3 (impossible) and 5, 3, target 4.

## Expected Output

The outputs below were produced by actually running `main.py` (Python 3.12) with the inputs shown; text after each prompt is the input that was typed.

**Default input (4, 3, target 2)**

```text
============================================================
EXPERIMENT 6: WATER JUG PROBLEM
============================================================
Capacity of jug 1 [4]: 
Capacity of jug 2 [3]: 
Target amount in litres [2]: 

Theory check: gcd(4, 3) = 1; target must be a multiple of 1 and at most 4.

Solution found in 4 steps:
Step Jug1  Jug2  Action
0    0     0     Start (both jugs empty)
1    0     3     Fill jug 2
2    3     0     Pour jug 2 into jug 1 (3 L)
3    3     3     Fill jug 2
4    4     2     Pour jug 2 into jug 1 (1 L)

Solution check (all moves legal, goal reached): True
```

**Impossible target (6, 4, target 3)**

```text
============================================================
EXPERIMENT 6: WATER JUG PROBLEM
============================================================
Capacity of jug 1 [4]: 6
Capacity of jug 2 [3]: 4
Target amount in litres [2]: 3

Theory check: gcd(6, 4) = 2; target must be a multiple of 2 and at most 6.
No solution: 3 litres cannot be measured with these jugs.
```

**Invalid input then 5, 3, 4**

```text
============================================================
EXPERIMENT 6: WATER JUG PROBLEM
============================================================
Capacity of jug 1 [4]: x
  Please enter a positive whole number.
Capacity of jug 1 [4]: 5
Capacity of jug 2 [3]: 3
Target amount in litres [2]: 4

Theory check: gcd(5, 3) = 1; target must be a multiple of 1 and at most 5.

Solution found in 6 steps:
Step Jug1  Jug2  Action
0    0     0     Start (both jugs empty)
1    5     0     Fill jug 1
2    2     3     Pour jug 1 into jug 2 (3 L)
3    2     0     Empty jug 2
4    0     2     Pour jug 1 into jug 2 (2 L)
5    5     2     Fill jug 1
6    4     3     Pour jug 1 into jug 2 (1 L)

Solution check (all moves legal, goal reached): True
```

## Result

For jugs of 4 L and 3 L with target 2 L, BFS finds a 4-step solution and prints every state. Impossible targets are reported, invalid input is rejected, and each solution is verified by replaying the moves.

## How to Run

```bat
cd Experiment_06_Water_Jug
python main.py
```

From the project root you can also run `run_experiment.bat 6`.
