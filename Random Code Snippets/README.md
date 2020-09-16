# Random Code Snippets
This repository contains some of the smaller projects and concepts that I have used Python to solve or explore.

## Games
### reversi.py
A simple reversi Player vs Player game built in Python that runs on the Command Prompt window.

### connectFour-MCTS-AI.py
A Connect Four game that has Player vs Player or Player vs AI option. The AI uses the Monte Carlo Tree Search (MCTS) algorithm to determine the move with the best payout by exploring (expanding) the search tree using random sampling to determine the move with the highest payout.

## Simulations
### cell_sim.py
This simulation demonstrates the growth or death of a population of cells (either normal or cancer cells) following the conditions provided:
- BIRTH: A new cell can only happen if there is 3 neighboring cells and the space is not occupied 
- DEATH: Cell dies from Overpopulation or Loneliness
  - Overpopulation: (NORMAL CELLS) If there is 4 or more neighboring cells; (CANCER CELLS) If there is 5 or more neighboring cells
  - Loneliness: If there is 1 or less neighboring cells
- STASIS: The cell does not change
Following these conditions, the program then simulates the state changes of the cells accordingly on a randomly populated board. Also note that the Normal Cells are marked with a "O" and the Cancer Cells are marked with an "X". 

This program demonstrates the usage of classes and inheritance to show a simple Monte Carlo simulation process applied to Biology. This is a Python implementation of a Programming II coursework in University that was originally implemented in C++.

### pi_estimator.py
A Monte Carlo simulation showing how \pi can be estimated by using normal distribution sampling.