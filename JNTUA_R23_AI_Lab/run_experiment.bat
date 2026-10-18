@echo off
setlocal
cd /d "%~dp0"
title JNTUA R23 - Artificial Intelligence Lab (23A31301P)

rem ---- Find Python 3 (the "py" launcher is preferred on Windows) ----
set "PY="
where py >nul 2>nul
if not errorlevel 1 set "PY=py -3"
if not defined PY (
    where python >nul 2>nul
    if not errorlevel 1 set "PY=python"
)
if not defined PY (
    echo Python 3 was not found.
    echo Install it from https://www.python.org/downloads/ and tick Add python.exe to PATH.
    pause
    exit /b 1
)

rem ---- Optional: run_experiment.bat 5   runs experiment 5 directly ----
set "FROM_ARG="
if not "%~1"=="" (
    set "CHOICE=%~1"
    set "FROM_ARG=1"
    goto run
)

:menu
cls
echo ============================================================
echo   JNTUA R23 - ARTIFICIAL INTELLIGENCE LAB  [23A31301P]
echo ============================================================
echo    1. Breadth First Search (BFS)
echo    2. Best First Search
echo    3. Depth First Search (DFS)
echo    4. Heuristic Search
echo    5. A* and AO* Algorithms
echo    6. Water Jug Problem
echo    7. Alpha-Beta Pruning
echo    8. Eight Queens Problem
echo    9. Meeting Scheduling (Default Reasoning)
echo   10. Unification Algorithm
echo   11. Knowledge-Based System
echo   12. 8-Puzzle and Tic-Tac-Toe
echo    0. Exit
echo.
set "CHOICE="
set /p "CHOICE=Enter experiment number (1-12), or 0 to exit: "
if "%CHOICE%"=="0" goto end

:run
set "FOLDER="
if "%CHOICE%"=="1" set "FOLDER=Experiment_01_BFS"
if "%CHOICE%"=="2" set "FOLDER=Experiment_02_Best_First_Search"
if "%CHOICE%"=="3" set "FOLDER=Experiment_03_DFS"
if "%CHOICE%"=="4" set "FOLDER=Experiment_04_Heuristic_Search"
if "%CHOICE%"=="5" set "FOLDER=Experiment_05_Astar_AOstar"
if "%CHOICE%"=="6" set "FOLDER=Experiment_06_Water_Jug"
if "%CHOICE%"=="7" set "FOLDER=Experiment_07_Alpha_Beta_Pruning"
if "%CHOICE%"=="8" set "FOLDER=Experiment_08_Eight_Queens"
if "%CHOICE%"=="9" set "FOLDER=Experiment_09_Default_Reasoning_Meeting"
if "%CHOICE%"=="10" set "FOLDER=Experiment_10_Unification"
if "%CHOICE%"=="11" set "FOLDER=Experiment_11_Knowledge_Base"
if "%CHOICE%"=="12" set "FOLDER=Experiment_12_Eight_Puzzle_Tic_Tac_Toe"
if not defined FOLDER (
    echo.
    echo Invalid choice. Please type a number from 1 to 12.
    if defined FROM_ARG exit /b 1
    pause
    goto menu
)

echo.
echo Running %FOLDER%\main.py
echo ------------------------------------------------------------
%PY% "%FOLDER%\main.py"
echo ------------------------------------------------------------
if defined FROM_ARG goto end
pause
goto menu

:end
endlocal
