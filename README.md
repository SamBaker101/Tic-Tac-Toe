# Tic-Tac-Toe

Sam Baker - 01/12/2020

 A simple command line based Tic Tac Toe game created as a simple testing ground for AI algorithms.

 # Game Modes
  - 1 - Player Vs Player - Standard Player Vs Player Tic-Tac-Toe
  - 2 - Player Vs RandomAI - Computer will check possible moves and choose 1 at random
  - 3 - Player Vs ListAI - Computer has a list of possible moves, it will make the first available move from this list
  - 4 - Player Vs LineAI - Computer will search the free spaces on the board for lines which can be completed during it's turn and completes them. This algorithm will both complete the computers lines to win the game and your lines to block you. If no possible lines are present the computer moves at random.
  - 5,6 - Player Vs BlindAI - (IN PROGRESS - Basic framework is implemented but training uneffective) Rudementary machine learning algorithm. Keeps a list of all moves on the board with weights associated with how often making each move led to victory in training. 
  - 7 - Blind Training - (IN PROGRESS - Basic framework is implemented but training uneffective) Training module for blind AI