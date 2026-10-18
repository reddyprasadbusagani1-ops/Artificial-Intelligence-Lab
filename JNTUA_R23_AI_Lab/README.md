# JNTUA R23 - Artificial Intelligence Lab

| | |
|---|---|
| **Subject** | Artificial Intelligence Lab |
| **Subject Code** | 23A31301P |
| **Regulations** | JNTUA R23 (B.Tech Artificial Intelligence & Data Science) |
| **Language** | Python 3.10 or newer (standard library only) |
| **Platform** | Windows 11 (also runs on macOS/Linux) |

This project contains all 12 experiments as runnable Python programs. Each experiment folder has a `main.py` and a `README.md` with the aim, theory, algorithm, full source code, sample input, expected output (captured from a real run) and result.

> The list of 12 experiments follows the project brief used to create this package. Please compare it with your official R23 syllabus copy and your lab instructor's instructions.

## 1. The 12 Experiments

| No. | Folder | Description |
|---|---|---|
| 1 | `Experiment_01_BFS` | **Breadth First Search** - traverses a graph level by level with a queue, shows traversal order, levels and the fewest-edge path. |
| 2 | `Experiment_02_Best_First_Search` | **Greedy Best First Search** - uses heuristic values to choose the next node, shows each step and the path, and compares its cost with the optimal cost. |
| 3 | `Experiment_03_DFS` | **Depth First Search** - recursive and stack-based traversal of a graph, plus a path to the goal. |
| 4 | `Experiment_04_Heuristic_Search` | **Heuristic Search** - Manhattan-distance heuristic on a maze; compares BFS, hill climbing (gets stuck) and greedy best-first. |
| 5 | `Experiment_05_Astar_AOstar` | **A\* and AO\*** - A* shortest path on a graph and AO* solution-graph search on an AND-OR graph, with the differences explained. |
| 6 | `Experiment_06_Water_Jug` | **Water Jug Problem** - BFS over the state space; prints every state of the solution. |
| 7 | `Experiment_07_Alpha_Beta_Pruning` | **Minimax with Alpha-Beta Pruning** - best value, visited leaves and pruning messages. |
| 8 | `Experiment_08_Eight_Queens` | **8-Queens** - backtracking; shows valid boards and the number of solutions (92). |
| 9 | `Experiment_09_Default_Reasoning_Meeting` | **Meeting Scheduling by Default Reasoning** - five people, rooms, day/time/place, documented assumptions, and retraction of a conclusion when new information arrives. |
| 10 | `Experiment_10_Unification` | **Unification** - first-order terms, substitutions, compound terms, occurs check, successful and failed examples. |
| 11 | `Experiment_11_Knowledge_Base` | **Knowledge-Based System** - family facts and rules, backward chaining, queries with proof explanations. |
| 12 | `Experiment_12_Eight_Puzzle_Tic_Tac_Toe` | **8-Puzzle and Tic-Tac-Toe** - A* with misplaced-tiles and Manhattan heuristics (statistics table), and playable Tic-Tac-Toe with minimax + alpha-beta (nodes/cutoffs table). |

See also [`EXPERIMENT_INDEX.md`](EXPERIMENT_INDEX.md).

## 2. Software Requirements

* Windows 11 (or Windows 10), any modern PC
* **Python 3.10 or newer** (3.12 recommended)
* Optional: Visual Studio Code with the *Python* extension; Git or GitHub Desktop (only for uploading to GitHub)
* No third-party packages, paid software, API keys or internet connection are needed to run the programs (`requirements.txt` only documents this).

## 3. Installing Python on Windows 11

1. Open <https://www.python.org/downloads/> and download the latest **Python 3** installer for Windows.
2. Run the installer. On the first screen **tick "Add python.exe to PATH"**, then click *Install Now*.
3. Open **Command Prompt** (press the Windows key, type `cmd`, press Enter) and check:

```bat
python --version
```

It should print `Python 3.10.x` or higher. If `python` is not recognised, try `py --version`. (If Windows opens the Microsoft Store when you type `python`, install Python from python.org as above, or turn off the *python.exe* "App execution alias" in *Settings > Apps > Advanced app settings > App execution aliases*.)

## 4. Downloading and Opening the Project

1. Download `JNTUA_R23_Artificial_Intelligence_Lab_Master.zip`.
2. Right-click the ZIP file, choose **Extract All...**, pick a folder (for example `C:\Users\<you>\Documents`) and click *Extract*. You get a folder named `JNTUA_R23_AI_Lab`.

**Option A - Visual Studio Code**

1. Start VS Code, choose **File > Open Folder...** and select `JNTUA_R23_AI_Lab`.
2. Open an experiment, e.g. `Experiment_01_BFS\main.py`.
3. Click the **Run (triangle)** button at the top right, or open the terminal (**Terminal > New Terminal**) and type a command from section 5.

**Option B - Command Prompt**

```bat
cd C:\Users\<you>\Documents\JNTUA_R23_AI_Lab
```

(Replace the path with the folder where you extracted the project.)

## 5. Running an Individual Experiment

From the project root (`JNTUA_R23_AI_Lab`):

```bat
python Experiment_01_BFS\main.py
python Experiment_05_Astar_AOstar\main.py
python Experiment_12_Eight_Puzzle_Tic_Tac_Toe\main.py
```

or change into the experiment folder first:

```bat
cd Experiment_08_Eight_Queens
python main.py
```

Use `py main.py` instead of `python main.py` if `python` is not recognised. Many programs ask for input; **press Enter to accept the default value shown in square brackets**. Experiments 4, 5 need no input; Experiments 11 and 12 have interactive prompts / menus (type `quit` or `0` to leave).

## 6. Using `run_experiment.bat`

Double-click `run_experiment.bat` (or run it in Command Prompt from the project folder):

```bat
run_experiment.bat
```

A menu lists the 12 experiments. Type a number from 1 to 12 and press Enter; the program runs, then press any key to return to the menu. Type `0` to exit.

You can also run an experiment directly by giving its number:

```bat
run_experiment.bat 7
```

The script looks for the `py` launcher first and then `python`, and tells you if Python is not installed.

## 7. Uploading the Project to GitHub

First create an **empty** repository on <https://github.com> (click **New**, give it a name such as `JNTUA_R23_AI_Lab`; do not add a README or licence because the project already has them).

**Method 1 - Git (Command Prompt or VS Code terminal)**

Install Git from <https://git-scm.com/download/win>, then in the project folder:

```bat
git init
git add .
git commit -m "Add JNTUA R23 AI Lab experiments"
git branch -M main
git remote add origin https://github.com/<your-username>/JNTUA_R23_AI_Lab.git
git push -u origin main
```

If Git asks who you are, set it once with `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"`. When pushing, sign in through the browser window that opens.

**Method 2 - GitHub Desktop**

1. Install and sign in to GitHub Desktop (<https://desktop.github.com/>).
2. Choose **File > Add local repository...**, select the `JNTUA_R23_AI_Lab` folder, and if asked, click *create a repository*.
3. Type a summary (e.g. "Add JNTUA R23 AI Lab experiments") and click **Commit to main**.
4. Click **Publish repository**, choose the name, and click *Publish*.

The included `.gitignore` keeps cache folders and virtual environments out of the repository.

## 8. Project Structure

```text
JNTUA_R23_AI_Lab/
|-- README.md                  (this file)
|-- requirements.txt
|-- .gitignore
|-- LICENSE                    (MIT)
|-- run_experiment.bat
|-- EXPERIMENT_INDEX.md
|-- Experiment_01_BFS/ ... Experiment_12_Eight_Puzzle_Tic_Tac_Toe/
|     |-- README.md
|     `-- main.py
```

## 9. Notes and Limitations

* Programs print plain ASCII text so they work in any Windows console.
* AO* (Experiment 5) is implemented for **acyclic** AND-OR graphs.
* The knowledge base (Experiment 11) uses the closed-world assumption: what cannot be proven is answered *No*.
* Experiment 12 runs a full minimax search for comparison, so the first computer move on an empty board takes about a second.
* Sample data (busy schedules, graphs, mazes) is invented for demonstration; edit the constants at the top of each `main.py` to experiment.

## 10. Licence

Released under the MIT Licence - see [`LICENSE`](LICENSE).
