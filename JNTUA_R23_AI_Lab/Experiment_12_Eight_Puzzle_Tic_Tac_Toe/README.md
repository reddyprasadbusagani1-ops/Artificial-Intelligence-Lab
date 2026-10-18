# Experiment 12: 8-Puzzle (A*) and Tic-Tac-Toe (Minimax + Alpha-Beta)

**Artificial Intelligence Lab | Subject Code 23A31301P | JNTUA R23 | B.Tech AI & DS**

## Aim

To solve the 8-puzzle with A* using two heuristics (misplaced tiles and Manhattan distance), and to implement a playable Tic-Tac-Toe using minimax with alpha-beta pruning while reporting search statistics.

## Theory

**8-puzzle:** a 3x3 board with tiles 1-8 and a blank. A move slides a tile into the blank. **A\*** expands the state with the smallest f = g + h. Two admissible heuristics are compared:
* **h1 - misplaced tiles:** number of tiles not in their goal position.
* **h2 - Manhattan distance:** sum of the horizontal + vertical distances of every tile from its goal position. h2 is at least as informed as h1 (it dominates it), so it expands fewer nodes.
A baseline with h = 0 (uniform-cost search) shows the cost of having no heuristic. A state is solvable only if its number of inversions is even.

**Tic-Tac-Toe:** a two-player zero-sum game solved by **minimax** (MAX = computer, MIN = human). Scores favour quick wins (10 - depth) and slow losses. **Alpha-beta pruning** returns the same move as minimax but skips branches that cannot affect the decision.

**Statistics reported**
* *Generated* (8-puzzle): start state + every successor created. *Expanded*: states taken from the open list. *Pruned*: successors discarded because the state was already reached by an equal or shorter path. *Max open*: largest size of the open list.
* *Nodes* (Tic-Tac-Toe): board positions examined by the search including the root. *Cutoffs*: times alpha >= beta stopped the loop over moves.

## Algorithm / Procedure

**A\* for the 8-puzzle**
1. Insert the start state with f = h(start).
2. Remove the state with the smallest f; if it is the goal, rebuild the move list.
3. Generate legal moves of the blank; for each child compute g + 1; skip it (count as *pruned*) if the child was reached before with equal or smaller g; else store and insert it.
4. Replay the moves to verify they lead to the goal; print the statistics table for each heuristic.

**Tic-Tac-Toe AI**
1. For every empty cell, place the computer's mark and evaluate the position with minimax or alpha-beta (depth-adjusted scores).
2. Choose the first move with the highest value.
3. Run **both** minimax and alpha-beta for each computer move and assert they pick the same move and value; record nodes and cutoffs in the table.
4. The human enters cells 1-9; occupied cells and invalid entries are rejected; after each move the program checks for a win or draw.

## Source Code

The complete program is in [`main.py`](main.py) and is reproduced here.

```python
"""
Experiment 12: 8-Puzzle (A* with two heuristics) and Tic-Tac-Toe (Minimax + Alpha-Beta)
Subject: Artificial Intelligence Lab (23A31301P) - JNTUA R23

PART A - 8-puzzle, solved with A*  (f = g + h)  using:
    h1 = number of MISPLACED tiles
    h2 = MANHATTAN distance (sum of horizontal + vertical distances of each tile)
  Both never over-estimate, so A* returns a shortest solution. A baseline with
  h = 0 (uniform-cost search) is included to show how much the heuristics help.
  Statistics reported:
    generated = start state + every successor created
    expanded  = states removed from the open list and processed
    pruned    = successors discarded because the state was already reached
                by an equal or shorter path (duplicate cut-off)

PART B - Tic-Tac-Toe: the computer uses minimax with alpha-beta pruning.
  The table compares plain minimax with alpha-beta for each computer move.
    nodes   = board positions examined by the search (including the root)
    cutoffs = number of times alpha >= beta stopped the loop over moves
"""

import heapq
import itertools
import time

# =====================================================================
#                           PART A : 8-PUZZLE
# =====================================================================
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)          # 0 stands for the blank
MOVE_DELTAS = {"Up": -3, "Down": 3, "Left": -1, "Right": 1}

# Sample start states (all solvable): (description, state)
SAMPLE_PUZZLES = [
    ("Easy", (4, 1, 3, 7, 2, 6, 0, 5, 8)),
    ("Medium", (8, 1, 3, 4, 0, 2, 7, 6, 5)),
    ("Harder", (5, 2, 8, 4, 1, 7, 0, 3, 6)),
]


def ask(prompt, default):
    try:
        text = input(prompt).strip()
    except EOFError:
        return default
    return text if text else default


def misplaced_tiles(state):
    """h1: how many tiles (not counting the blank) are not in their goal position."""
    return sum(1 for tile, goal_tile in zip(state, GOAL) if tile != 0 and tile != goal_tile)


def manhattan_distance(state):
    """h2: sum over tiles of |row difference| + |column difference| to the goal."""
    total = 0
    for index, tile in enumerate(state):
        if tile != 0:
            goal_index = GOAL.index(tile)
            total += abs(index // 3 - goal_index // 3) + abs(index % 3 - goal_index % 3)
    return total


def zero_heuristic(state):
    """h = 0 : no knowledge, A* becomes uniform-cost search."""
    return 0


def is_solvable(state):
    """For a 3x3 board a state is solvable if the number of inversions is even."""
    tiles = [t for t in state if t != 0]
    inversions = sum(1 for i in range(len(tiles)) for j in range(i + 1, len(tiles))
                     if tiles[i] > tiles[j])
    return inversions % 2 == 0


def puzzle_successors(state):
    """Yield (move name, new state) for every legal move of the blank."""
    blank = state.index(0)
    row, col = divmod(blank, 3)
    for move, delta in MOVE_DELTAS.items():
        if move == "Up" and row == 0:
            continue
        if move == "Down" and row == 2:
            continue
        if move == "Left" and col == 0:
            continue
        if move == "Right" and col == 2:
            continue
        target = blank + delta
        board = list(state)
        board[blank], board[target] = board[target], board[blank]
        yield move, tuple(board)


def a_star_puzzle(start, heuristic):
    """A* search. Returns a dict with the move list and the search statistics."""
    counter = itertools.count()
    open_list = [(heuristic(start), next(counter), 0, start)]    # (f, tie, g, state)
    best_g = {start: 0}
    parent = {start: (None, None)}
    generated, expanded, pruned, max_open = 1, 0, 0, 1

    while open_list:
        f, _, g, state = heapq.heappop(open_list)
        if g > best_g[state]:
            continue                                  # outdated entry
        expanded += 1
        if state == GOAL:
            moves = []
            while parent[state][0] is not None:
                state, move = parent[state][0], parent[state][1]
                moves.append(move)
            return {"moves": moves[::-1], "generated": generated, "expanded": expanded,
                    "pruned": pruned, "max_open": max_open}
        for move, child in puzzle_successors(state):
            generated += 1
            new_g = g + 1
            if child in best_g and best_g[child] <= new_g:
                pruned += 1                           # already reached as cheaply
                continue
            best_g[child] = new_g
            parent[child] = (state, move)
            heapq.heappush(open_list, (new_g + heuristic(child), next(counter), new_g, child))
            max_open = max(max_open, len(open_list))
    return None


def apply_moves(state, moves):
    """Replay a move list on a state; raises ValueError if a move is illegal."""
    for move in moves:
        options = dict(puzzle_successors(state))
        if move not in options:
            raise ValueError(f"illegal move {move}")
        state = options[move]
    return state


def print_board(state, indent="   "):
    for r in range(3):
        print(indent + " ".join(str(t) if t else "_" for t in state[3 * r:3 * r + 3]))


def read_puzzle():
    """Ask for 9 numbers (0-8). Returns a valid, solvable state or None."""
    text = ask("Enter 9 numbers 0-8 separated by spaces (0 = blank), e.g. 1 2 3 4 0 6 7 5 8: ", "")
    parts = text.replace(",", " ").split()
    if len(parts) != 9 or not all(p.isdigit() for p in parts) \
            or sorted(int(p) for p in parts) != list(range(9)):
        print("  Invalid input: use each of the numbers 0-8 exactly once.")
        return None
    state = tuple(int(p) for p in parts)
    if not is_solvable(state):
        print("  This arrangement is NOT solvable (odd number of inversions).")
        return None
    return state


def compare_heuristics(puzzles, show_solution=False):
    """Solve each puzzle with every heuristic and print the statistics table."""
    heuristics = [("h=0 (uniform cost)", zero_heuristic),
                  ("Misplaced tiles", misplaced_tiles),
                  ("Manhattan distance", manhattan_distance)]
    for name, state in puzzles:
        if not is_solvable(state):
            print(f"\nPuzzle {name} is not solvable - skipped.")
            continue
        print(f"\nPuzzle: {name}   (h1 = {misplaced_tiles(state)}, "
              f"h2 = {manhattan_distance(state)} at the start)")
        print_board(state)
        print(f"   {'Heuristic':<20}{'Moves':>6}{'Generated':>11}{'Expanded':>10}"
              f"{'Pruned':>9}{'Max open':>10}{'Time(s)':>9}")
        lengths, first_moves = set(), None
        for label, heuristic in heuristics:
            begin = time.perf_counter()
            result = a_star_puzzle(state, heuristic)
            elapsed = time.perf_counter() - begin
            assert apply_moves(state, result["moves"]) == GOAL, "solution check failed"
            lengths.add(len(result["moves"]))
            first_moves = first_moves or result["moves"]
            print(f"   {label:<20}{len(result['moves']):>6}{result['generated']:>11}"
                  f"{result['expanded']:>10}{result['pruned']:>9}{result['max_open']:>10}"
                  f"{elapsed:>9.3f}")
        print(f"   All solutions valid and of equal (optimal) length: {len(lengths) == 1}")
        if show_solution:
            print("   Solution moves of the blank:", " ".join(first_moves))


# =====================================================================
#                         PART B : TIC-TAC-TOE
# =====================================================================
WIN_LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
             (2, 5, 8), (0, 4, 8), (2, 4, 6)]
INF = float("inf")


class Stats:
    """Counts the work done by one search."""
    def __init__(self):
        self.nodes = 0
        self.cutoffs = 0


def winner(board):
    """Return 'X' or 'O' if someone has three in a row, else None."""
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def empty_cells(board):
    return [i for i, cell in enumerate(board) if cell == " "]


def other(player):
    return "O" if player == "X" else "X"


def evaluate(board, ai, depth):
    """Score a finished game from the computer's view (earlier wins score higher)."""
    won = winner(board)
    if won == ai:
        return 10 - depth
    if won is not None:
        return depth - 10
    return 0 if not empty_cells(board) else None        # None = game not finished


def minimax(board, player, ai, depth, stats):
    """Plain minimax (no pruning)."""
    stats.nodes += 1
    score = evaluate(board, ai, depth)
    if score is not None:
        return score
    maximizing = player == ai
    best = -INF if maximizing else INF
    for cell in empty_cells(board):
        board[cell] = player
        value = minimax(board, other(player), ai, depth + 1, stats)
        board[cell] = " "
        best = max(best, value) if maximizing else min(best, value)
    return best


def alpha_beta(board, player, ai, depth, alpha, beta, stats):
    """Minimax with alpha-beta pruning."""
    stats.nodes += 1
    score = evaluate(board, ai, depth)
    if score is not None:
        return score
    maximizing = player == ai
    best = -INF if maximizing else INF
    for cell in empty_cells(board):
        board[cell] = player
        value = alpha_beta(board, other(player), ai, depth + 1, alpha, beta, stats)
        board[cell] = " "
        if maximizing:
            best = max(best, value)
            alpha = max(alpha, best)
        else:
            best = min(best, value)
            beta = min(beta, best)
        if alpha >= beta:                       # remaining moves cannot matter
            stats.cutoffs += 1
            break
    return best


def choose_move(board, ai, use_alpha_beta=True):
    """Return (best cell, value, Stats). Ties go to the lowest-numbered cell."""
    stats = Stats()
    best_cell, best_value = None, -INF
    alpha = -INF
    for cell in empty_cells(board):
        board[cell] = ai
        score = evaluate(board, ai, 1)
        if score is None:                       # game continues: search counts the node
            if use_alpha_beta:
                score = alpha_beta(board, other(ai), ai, 2, alpha, INF, stats)
            else:
                score = minimax(board, other(ai), ai, 2, stats)
        else:
            stats.nodes += 1                    # finished game: count this leaf here
        board[cell] = " "
        if score > best_value:                  # strictly better: keep first best move
            best_cell, best_value = cell, score
        alpha = max(alpha, best_value) if use_alpha_beta else alpha
    stats.nodes += 1                            # count the root position once
    return best_cell, best_value, stats


def draw_board(board):
    print()
    for r in range(3):
        row = [board[3 * r + c] if board[3 * r + c] != " " else str(3 * r + c + 1)
               for c in range(3)]
        print("   " + " | ".join(row))
        if r < 2:
            print("  ---+---+---")
    print()


def ai_turn(board, ai, history):
    """Computer move with BOTH algorithms; records the statistics in history."""
    cell_ab, value_ab, stats_ab = choose_move(board, ai, True)
    cell_mm, value_mm, stats_mm = choose_move(board, ai, False)
    assert (cell_ab, value_ab) == (cell_mm, value_mm), "alpha-beta must match minimax"
    board[cell_ab] = ai
    history.append((len(history) + 1, ai, cell_ab + 1, stats_mm.nodes,
                    stats_ab.nodes, stats_ab.cutoffs))
    print(f"Computer ({ai}) plays cell {cell_ab + 1}.   "
          f"[minimax nodes={stats_mm.nodes}, alpha-beta nodes={stats_ab.nodes}, "
          f"cutoffs={stats_ab.cutoffs}]")


def print_history(history):
    if not history:
        return
    print("\nSearch statistics per computer move")
    print(f"{'AI move':>8}{'Player':>8}{'Cell':>6}{'Minimax nodes':>15}"
          f"{'Alpha-beta nodes':>18}{'Cutoffs':>9}{'Nodes saved':>13}")
    total_mm = total_ab = total_cut = 0
    for number, player, cell, mm, ab, cuts in history:
        saved = 100 * (mm - ab) / mm
        print(f"{number:>8}{player:>8}{cell:>6}{mm:>15}{ab:>18}{cuts:>9}{saved:>12.1f}%")
        total_mm, total_ab, total_cut = total_mm + mm, total_ab + ab, total_cut + cuts
    print(f"{'Total':>8}{'':>8}{'':>6}{total_mm:>15}{total_ab:>18}{total_cut:>9}"
          f"{100 * (total_mm - total_ab) / total_mm:>12.1f}%")


def read_cell(board):
    """Ask the human for a legal cell (1-9). Returns the index, or None to quit."""
    while True:
        try:
            text = input("Your move (1-9, or q to quit): ").strip().lower()
        except EOFError:
            print("\nInput ended - game stopped.")
            return None
        if text == "q":
            return None
        if not text.isdigit() or not 1 <= int(text) <= 9:
            print("  Enter a number from 1 to 9.")
        elif board[int(text) - 1] != " ":
            print("  That cell is already taken.")
        else:
            return int(text) - 1


def announce(board):
    won = winner(board)
    if won:
        print(f"Game over: {won} wins!")
        return True
    if not empty_cells(board):
        print("Game over: it is a draw.")
        return True
    return False


def play_human_vs_computer():
    choice = ask("Do you want to be X (moves first) or O? [X]: ", "X").upper()
    human = "O" if choice == "O" else "X"
    ai = other(human)
    board, history, turn = [" "] * 9, [], "X"
    print(f"You are {human}; the computer is {ai}. Cells are numbered 1-9.")
    draw_board(board)
    while True:
        if turn == human:
            cell = read_cell(board)
            if cell is None:
                break
            board[cell] = human
        else:
            ai_turn(board, ai, history)
        draw_board(board)
        if announce(board):
            break
        turn = other(turn)
    print_history(history)


def play_computer_vs_computer():
    board, history, turn = [" "] * 9, [], "X"
    print("Computer (X) plays computer (O) with perfect play.")
    while winner(board) is None and empty_cells(board):
        ai_turn(board, turn, history)
        turn = other(turn)
    draw_board(board)
    announce(board)
    print_history(history)


def main():
    print("=" * 60)
    print("EXPERIMENT 12: 8-PUZZLE AND TIC-TAC-TOE")
    print("=" * 60)
    while True:
        print("\nMenu:")
        print("  1. 8-puzzle: compare heuristics on three sample puzzles")
        print("  2. 8-puzzle: enter your own start state")
        print("  3. Tic-Tac-Toe: play against the computer")
        print("  4. Tic-Tac-Toe: computer vs computer (statistics table)")
        print("  0. Exit")
        choice = ask("Choose [0]: ", "0")
        if choice == "1":
            print(f"\nGoal state:")
            print_board(GOAL)
            compare_heuristics(SAMPLE_PUZZLES, show_solution=True)
        elif choice == "2":
            state = read_puzzle()
            if state is not None:
                if state == GOAL:
                    print("  Already solved!")
                else:
                    compare_heuristics([("Your puzzle", state)], show_solution=True)
        elif choice == "3":
            print()
            play_human_vs_computer()
        elif choice == "4":
            print()
            play_computer_vs_computer()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("  Invalid choice. Please enter 0, 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
```

## Sample Input

Menu choices: `1` runs three sample puzzles; `2` accepts your own 9 numbers (0 = blank), e.g. `1 2 3 4 0 6 7 5 8`; `3` plays Tic-Tac-Toe (you choose X or O, then type cells 1-9; `q` quits); `4` shows computer vs computer; `0` exits.

## Expected Output

The outputs below were produced by actually running `main.py` (Python 3.12) with the inputs shown; text after each prompt is the input that was typed.

**Menu 1 (8-puzzle comparison) and menu 4 (computer vs computer)**

```text
============================================================
EXPERIMENT 12: 8-PUZZLE AND TIC-TAC-TOE
============================================================

Menu:
  1. 8-puzzle: compare heuristics on three sample puzzles
  2. 8-puzzle: enter your own start state
  3. Tic-Tac-Toe: play against the computer
  4. Tic-Tac-Toe: computer vs computer (statistics table)
  0. Exit
Choose [0]: 1

Goal state:
   1 2 3
   4 5 6
   7 8 _

Puzzle: Easy   (h1 = 6, h2 = 6 at the start)
   4 1 3
   7 2 6
   _ 5 8
   Heuristic            Moves  Generated  Expanded   Pruned  Max open  Time(s)
   h=0 (uniform cost)       6        143        53       52        39    0.001
   Misplaced tiles          6         18         7        5         7    0.000
   Manhattan distance       6         18         7        5         7    0.000
   All solutions valid and of equal (optimal) length: True
   Solution moves of the blank: Up Up Right Down Down Right

Puzzle: Medium   (h1 = 5, h2 = 10 at the start)
   8 1 3
   4 _ 2
   7 6 5
   Heuristic            Moves  Generated  Expanded   Pruned  Max open  Time(s)
   h=0 (uniform cost)      14      15867      5961     6846      3061    0.025
   Misplaced tiles         14        827       302      328       198    0.001
   Manhattan distance      14        207        77       79        52    0.000
   All solutions valid and of equal (optimal) length: True
   Solution moves of the blank: Right Down Left Left Up Up Right Down Left Down Right Up Right Down

Puzzle: Harder   (h1 = 6, h2 = 14 at the start)
   5 2 8
   4 1 7
   _ 3 6
   Heuristic            Moves  Generated  Expanded   Pruned  Max open  Time(s)
   h=0 (uniform cost)      22     230301     85698   122363     23972    0.546
   Misplaced tiles         22      20573      7600     8739      4233    0.071
   Manhattan distance      22       1770       668      720       378    0.006
   All solutions valid and of equal (optimal) length: True
   Solution moves of the blank: Up Right Right Down Left Up Right Up Left Left Down Down Right Up Right Down Left Up Up Right Down Down

Menu:
  1. 8-puzzle: compare heuristics on three sample puzzles
  2. 8-puzzle: enter your own start state
  3. Tic-Tac-Toe: play against the computer
  4. Tic-Tac-Toe: computer vs computer (statistics table)
  0. Exit
Choose [0]: 4

Computer (X) plays computer (O) with perfect play.
Computer (X) plays cell 1.   [minimax nodes=549946, alpha-beta nodes=16771, cutoffs=6744]
Computer (O) plays cell 5.   [minimax nodes=59705, alpha-beta nodes=2788, cutoffs=1060]
Computer (X) plays cell 2.   [minimax nodes=7332, alpha-beta nodes=871, cutoffs=322]
Computer (O) plays cell 3.   [minimax nodes=935, alpha-beta nodes=75, cutoffs=29]
Computer (X) plays cell 7.   [minimax nodes=198, alpha-beta nodes=64, cutoffs=24]
Computer (O) plays cell 4.   [minimax nodes=47, alpha-beta nodes=17, cutoffs=6]
Computer (X) plays cell 6.   [minimax nodes=14, alpha-beta nodes=10, cutoffs=3]
Computer (O) plays cell 8.   [minimax nodes=5, alpha-beta nodes=5, cutoffs=1]
Computer (X) plays cell 9.   [minimax nodes=2, alpha-beta nodes=2, cutoffs=0]

   X | X | O
  ---+---+---
   O | O | X
  ---+---+---
   X | O | X

Game over: it is a draw.

Search statistics per computer move
 AI move  Player  Cell  Minimax nodes  Alpha-beta nodes  Cutoffs  Nodes saved
       1       X     1         549946             16771     6744        97.0%
       2       O     5          59705              2788     1060        95.3%
       3       X     2           7332               871      322        88.1%
       4       O     3            935                75       29        92.0%
       5       X     7            198                64       24        67.7%
       6       O     4             47                17        6        63.8%
       7       X     6             14                10        3        28.6%
       8       O     8              5                 5        1         0.0%
       9       X     9              2                 2        0         0.0%
   Total                       618184             20603     8189        96.7%

Menu:
  1. 8-puzzle: compare heuristics on three sample puzzles
  2. 8-puzzle: enter your own start state
  3. Tic-Tac-Toe: play against the computer
  4. Tic-Tac-Toe: computer vs computer (statistics table)
  0. Exit
Choose [0]: 0
Goodbye.
```

**Playing Tic-Tac-Toe as X (includes an invalid entry and an occupied cell)**

```text
============================================================
EXPERIMENT 12: 8-PUZZLE AND TIC-TAC-TOE
============================================================

Menu:
  1. 8-puzzle: compare heuristics on three sample puzzles
  2. 8-puzzle: enter your own start state
  3. Tic-Tac-Toe: play against the computer
  4. Tic-Tac-Toe: computer vs computer (statistics table)
  0. Exit
Choose [0]: 3

Do you want to be X (moves first) or O? [X]: X
You are X; the computer is O. Cells are numbered 1-9.

   1 | 2 | 3
  ---+---+---
   4 | 5 | 6
  ---+---+---
   7 | 8 | 9

Your move (1-9, or q to quit): 5

   1 | 2 | 3
  ---+---+---
   4 | X | 6
  ---+---+---
   7 | 8 | 9

Computer (O) plays cell 1.   [minimax nodes=55505, alpha-beta nodes=2459, cutoffs=965]

   O | 2 | 3
  ---+---+---
   4 | X | 6
  ---+---+---
   7 | 8 | 9

Your move (1-9, or q to quit): x
  Enter a number from 1 to 9.
Your move (1-9, or q to quit): 5
  That cell is already taken.
Your move (1-9, or q to quit): 9

   O | 2 | 3
  ---+---+---
   4 | X | 6
  ---+---+---
   7 | 8 | X

Computer (O) plays cell 3.   [minimax nodes=1173, alpha-beta nodes=288, cutoffs=111]

   O | 2 | O
  ---+---+---
   4 | X | 6
  ---+---+---
   7 | 8 | X

Your move (1-9, or q to quit): 6

   O | 2 | O
  ---+---+---
   4 | X | X
  ---+---+---
   7 | 8 | X

Computer (O) plays cell 2.   [minimax nodes=34, alpha-beta nodes=18, cutoffs=7]

   O | O | O
  ---+---+---
   4 | X | X
  ---+---+---
   7 | 8 | X

Game over: O wins!

Search statistics per computer move
 AI move  Player  Cell  Minimax nodes  Alpha-beta nodes  Cutoffs  Nodes saved
       1       O     1          55505              2459      965        95.6%
       2       O     3           1173               288      111        75.4%
       3       O     2             34                18        7        47.1%
   Total                        56712              2765     1083        95.1%

Menu:
  1. 8-puzzle: compare heuristics on three sample puzzles
  2. 8-puzzle: enter your own start state
  3. Tic-Tac-Toe: play against the computer
  4. Tic-Tac-Toe: computer vs computer (statistics table)
  0. Exit
Choose [0]: 0
Goodbye.
```

**Own 8-puzzle state; unsolvable state rejected**

```text
============================================================
EXPERIMENT 12: 8-PUZZLE AND TIC-TAC-TOE
============================================================

Menu:
  1. 8-puzzle: compare heuristics on three sample puzzles
  2. 8-puzzle: enter your own start state
  3. Tic-Tac-Toe: play against the computer
  4. Tic-Tac-Toe: computer vs computer (statistics table)
  0. Exit
Choose [0]: 2
Enter 9 numbers 0-8 separated by spaces (0 = blank), e.g. 1 2 3 4 0 6 7 5 8: 1 2 3 4 0 6 7 5 8

Puzzle: Your puzzle   (h1 = 2, h2 = 2 at the start)
   1 2 3
   4 _ 6
   7 5 8
   Heuristic            Moves  Generated  Expanded   Pruned  Max open  Time(s)
   h=0 (uniform cost)       2         23         9        7         8    0.000
   Misplaced tiles          2          8         3        1         5    0.000
   Manhattan distance       2          8         3        1         5    0.000
   All solutions valid and of equal (optimal) length: True
   Solution moves of the blank: Down Right

Menu:
  1. 8-puzzle: compare heuristics on three sample puzzles
  2. 8-puzzle: enter your own start state
  3. Tic-Tac-Toe: play against the computer
  4. Tic-Tac-Toe: computer vs computer (statistics table)
  0. Exit
Choose [0]: 2
Enter 9 numbers 0-8 separated by spaces (0 = blank), e.g. 1 2 3 4 0 6 7 5 8: 1 2 3 4 5 6 8 7 0
  This arrangement is NOT solvable (odd number of inversions).

Menu:
  1. 8-puzzle: compare heuristics on three sample puzzles
  2. 8-puzzle: enter your own start state
  3. Tic-Tac-Toe: play against the computer
  4. Tic-Tac-Toe: computer vs computer (statistics table)
  0. Exit
Choose [0]: 0
Goodbye.
```

## Result

All three heuristic settings return the same optimal solution length, but Manhattan distance expands far fewer nodes than misplaced tiles, and both beat h = 0. Tic-Tac-Toe is fully playable with legal-move checking; alpha-beta chooses exactly the same moves as plain minimax while examining about 97% fewer nodes over a full game (the table shows nodes and cutoffs for every computer move). Time values in the tables depend on the computer.

## How to Run

```bat
cd Experiment_12_Eight_Puzzle_Tic_Tac_Toe
python main.py
```

From the project root you can also run `run_experiment.bat 12`.
