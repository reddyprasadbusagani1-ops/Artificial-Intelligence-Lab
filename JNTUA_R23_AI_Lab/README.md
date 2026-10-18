
# Artificial Intelligence Lab

**JNTUA R23 | B.Tech Artificial Intelligence and Data Science**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Course](https://img.shields.io/badge/Course-AI%20Lab-purple.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Project Information

| Detail | Information |
|---|---|
| Subject | Artificial Intelligence Lab |
| Subject Code | 23A31301P |
| Regulations | JNTUA R23 |
| Branch | B.Tech Artificial Intelligence and Data Science |
| Programming Language | Python 3.10 or later |
| Platform | Windows 10/11, macOS, Linux |
| Author | Busagani Reddy Prasad |
| GitHub | [reddyprasadbusagani1-ops](https://github.com/reddyprasadbusagani1-ops) |

## About This Repository

This repository contains Python implementations of 12 Artificial Intelligence lab experiments for academic learning and practical programming.

Each experiment is organized into a separate folder with a runnable `main.py` program and a `README.md` containing the aim, theory, algorithm, source code, sample input, expected output, and result, where applicable.

The programs are designed to run using Python's standard library without requiring third-party packages.

**Academic note:** Please compare the experiment list with your official JNTUA R23 syllabus and your faculty's instructions before treating it as the prescribed lab list.

## Table of Contents

1. [List of Experiments](#list-of-experiments)
2. [Software Requirements](#software-requirements)
3. [Installation and Setup](#installation-and-setup)
4. [Project Structure](#project-structure)
5. [Running an Experiment](#running-an-experiment)
6. [Experiment Launcher](#experiment-launcher)
7. [Learning Objectives](#learning-objectives)
8. [Notes and Limitations](#notes-and-limitations)
9. [Author](#author)
10. [License](#license)

## List of Experiments

| No. | Experiment | Description |
|---|---|---|
| 1 | Breadth First Search (BFS) | Traverses a graph level by level using a queue and finds shortest paths in an unweighted graph. |
| 2 | Greedy Best-First Search | Uses heuristic values to select the next node and explores a path toward the goal. |
| 3 | Depth First Search (DFS) | Implements recursive and stack-based graph traversal. |
| 4 | Heuristic Search | Explores maze-solving techniques using Manhattan distance, BFS, hill climbing, and greedy best-first search. |
| 5 | A* and AO* Search | Demonstrates A* shortest-path search and AO* search on an AND-OR graph. |
| 6 | Water Jug Problem | Models the water jug problem as a state space and solves it using BFS. |
| 7 | Minimax with Alpha-Beta Pruning | Evaluates game trees and prunes branches that cannot affect the final decision. |
| 8 | Eight Queens Problem | Uses backtracking to find valid arrangements of eight queens on a chessboard. |
| 9 | Default Reasoning and Meeting Scheduling | Demonstrates reasoning with assumptions and revising conclusions when new information arrives. |
| 10 | Unification | Demonstrates logical terms, substitutions, compound expressions, and the occurs check. |
| 11 | Knowledge-Based System | Demonstrates facts, rules, backward chaining, and query explanations. |
| 12 | Eight Puzzle and Tic-Tac-Toe | Uses A* search for the Eight Puzzle and Minimax with Alpha-Beta Pruning for Tic-Tac-Toe. |

For the experiment folder names and additional details, see [`EXPERIMENT_INDEX.md`](EXPERIMENT_INDEX.md).

## Software Requirements

- Python 3.10 or later.
- A computer running Windows, macOS, or Linux.
- Command Prompt or a terminal.
- A text editor such as Notepad or Visual Studio Code.

Optional tools:

- Git for version control.
- GitHub account for hosting the project.
- GitHub Desktop for graphical repository management.

No third-party Python packages, API keys, or internet connection are required to run the programs locally.

## Installation and Setup

### Step 1: Install Python

Download Python from the official website:

https://www.python.org/downloads/

On Windows, enable **Add Python to PATH** during installation if the option is available.

### Step 2: Verify Python Installation

Open Command Prompt and run:

```bat
python --version
```

If the command is not recognized, try:

```bat
py --version
```

Confirm that Python 3.10 or later is installed.

### Step 3: Download the Repository

Open the repository:

https://github.com/reddyprasadbusagani1-ops/Artificial-Intelligence-Lab

Click **Code → Download ZIP**, then extract the downloaded file.

Alternatively, clone it using Git:

```bat
git clone https://github.com/reddyprasadbusagani1-ops/Artificial-Intelligence-Lab.git
```

Open the extracted or cloned project folder in Command Prompt.

For example, if the folder is in Downloads:

```bat
cd "%USERPROFILE%\Downloads\Artificial-Intelligence-Lab"
```

Adjust the path if your folder is located elsewhere.

## Project Structure

The intended folder organization is:

```text
Artificial-Intelligence-Lab/
|
|-- README.md
|-- EXPERIMENT_INDEX.md
|-- requirements.txt
|-- .gitignore
|-- LICENSE
|-- run_experiment.bat
|
|-- Experiment_01_BFS/
|   |-- README.md
|   `-- main.py
|
|-- Experiment_02_Best_First_Search/
|   |-- README.md
|   `-- main.py
|
|-- Experiment_03_DFS/
|   |-- README.md
|   `-- main.py
|
|-- Experiment_04_Heuristic_Search/
|   |-- README.md
|   `-- main.py
|
|-- Experiment_05_Astar_AOstar/
|   |-- README.md
|   `-- main.py
|
|-- Experiment_06_Water_Jug/
|   |-- README.md
|   `-- main.py
|
|-- Experiment_07_Alpha_Beta_Pruning/
|   |-- README.md
|   `-- main.py
|
|-- Experiment_08_Eight_Queens/
|   |-- README.md
|   `-- main.py
|
|-- Experiment_09_Default_Reasoning_Meeting/
|   |-- README.md
|   `-- main.py
|
|-- Experiment_10_Unification/
|   |-- README.md
|   `-- main.py
|
|-- Experiment_11_Knowledge_Base/
|   |-- README.md
|   `-- main.py
|
`-- Experiment_12_Eight_Puzzle_Tic_Tac_Toe/
    |-- README.md
    `-- main.py
```

This is the intended structure. Your actual repository may contain additional files; verify the folder names and files before relying on the example commands.

## Running an Experiment

Run commands from the project root directory.

### Experiment 1: Breadth First Search

```bat
python Experiment_01_BFS\main.py
```

### Experiment 5: A* and AO* Search

```bat
python Experiment_05_Astar_AOstar\main.py
```

### Experiment 8: Eight Queens Problem

```bat
python Experiment_08_Eight_Queens\main.py
```

### Experiment 12: Eight Puzzle and Tic-Tac-Toe

```bat
python Experiment_12_Eight_Puzzle_Tic_Tac_Toe\main.py
```

If `python` is not recognized, use `py` instead.

For example:

```bat
py Experiment_01_BFS\main.py
```

You can also enter an experiment folder and run its program directly:

```bat
cd Experiment_08_Eight_Queens
python main.py
```

Follow the program's on-screen instructions. If a default input is shown in square brackets, press Enter to accept it.

## Experiment Launcher

If `run_experiment.bat` is present in the project root, you can use it to launch experiments on Windows.

### Open the experiment menu

```bat
run_experiment.bat
```

Choose a number from 1 to 12 and press Enter.

Enter `0` to exit the menu.

### Run a specific experiment

For example, to launch Experiment 7:

```bat
run_experiment.bat 7
```

The launcher must be present and correctly configured for these commands to work.

## Learning Objectives

Through these experiments, students can practise:

- Graph traversal using BFS and DFS.
- Uninformed and heuristic search techniques.
- A* and AO* search concepts.
- State-space representation and problem solving.
- Minimax and Alpha-Beta Pruning.
- Backtracking for constraint-satisfaction problems.
- Default reasoning and unification.
- Knowledge representation and backward chaining.
- Applying classical Artificial Intelligence techniques to practical problems.

## Notes and Limitations

- The programs are intended for educational use.
- Input formats and sample outputs are documented in individual experiment folders where provided.
- Sample graphs, mazes, schedules, and other demonstration data may be illustrative.
- The AO* implementation is intended for acyclic AND-OR graphs.
- The knowledge-based system uses a closed-world assumption: a query that cannot be proven is treated as false by the described implementation.
- Search and game-tree execution times depend on the input and computer.
- Always check the actual source code and run the programs to verify their behavior.

## Author

**Busagani Reddy Prasad**

B.Tech — Artificial Intelligence and Data Science

GitHub: [@reddyprasadbusagani1-ops](https://github.com/reddyprasadbusagani1-ops)

## License

This project is distributed under the MIT License, provided the repository's `LICENSE` file contains the MIT License text.

See [`LICENSE`](LICENSE) for the complete terms.
