# Experiment Index

**Artificial Intelligence Lab (23A31301P) - JNTUA R23 - Python 3.10+**

| No. | Experiment | Folder | Topic | What the program shows | Input |
|---|---|---|---|---|---|
| 1 | BFS | [`Experiment_01_BFS`](Experiment_01_BFS/) | Uninformed search | Traversal order, levels, fewest-edge path, unreachable nodes | Start/goal node (Enter = defaults) |
| 2 | Greedy best-first search | [`Experiment_02_Best_First_Search`](Experiment_02_Best_First_Search/) | Informed search (h only) | Expansion steps, path, comparison with optimal cost | Start node |
| 3 | DFS | [`Experiment_03_DFS`](Experiment_03_DFS/) | Uninformed search | Recursive and stack traversal orders, a path | Start/goal node |
| 4 | Heuristic search (Manhattan distance) | [`Experiment_04_Heuristic_Search`](Experiment_04_Heuristic_Search/) | BFS vs hill climbing vs greedy | Grids with paths, local-minimum failure, cells expanded | None |
| 5 | A* and AO* | [`Experiment_05_Astar_AOstar`](Experiment_05_Astar_AOstar/) | Informed search; AND-OR graph search | A* path/cost; AO* solution graph/cost; both verified | None |
| 6 | Water jug | [`Experiment_06_Water_Jug`](Experiment_06_Water_Jug/) | State-space search (BFS) | Table of every state and action | Capacities and target |
| 7 | Alpha-beta pruning | [`Experiment_07_Alpha_Beta_Pruning`](Experiment_07_Alpha_Beta_Pruning/) | Adversarial search | Best value, visited leaves, pruning messages | Optional nested-list tree |
| 8 | 8-queens | [`Experiment_08_Eight_Queens`](Experiment_08_Eight_Queens/) | Backtracking | Valid boards, number of solutions (92) | Board size N (default 8) |
| 9 | Meeting scheduling | [`Experiment_09_Default_Reasoning_Meeting`](Experiment_09_Default_Reasoning_Meeting/) | Default (non-monotonic) reasoning | Day, time, place; retraction after new information | Meeting duration |
| 10 | Unification | [`Experiment_10_Unification`](Experiment_10_Unification/) | First-order logic | Unifier, occurs check, failure reasons | Optional pairs of terms |
| 11 | Knowledge base | [`Experiment_11_Knowledge_Base`](Experiment_11_Knowledge_Base/) | Rule-based inference (backward chaining) | Answers with proof trees | Optional queries |
| 12 | 8-puzzle and Tic-Tac-Toe | [`Experiment_12_Eight_Puzzle_Tic_Tac_Toe`](Experiment_12_Eight_Puzzle_Tic_Tac_Toe/) | A* with 2 heuristics; minimax + alpha-beta | Statistics tables, playable game | Menu choices, own puzzle, game moves |

Every experiment folder contains `main.py` (the program) and `README.md` (aim, theory, algorithm, full source code, sample input, expected output captured from a real run, and result).

Run one experiment: `python Experiment_01_BFS\main.py` or use `run_experiment.bat`.
