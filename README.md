# Tic-Tac-Toe

Sam Baker - 01/12/2020

 A simple command line based Tic Tac Toe game created as a testing ground for logical and machine learning algorithms.
 
 Note in this project I have not used Tensorflow or any other Machine Learning libraries. My thought process with this project is that by incrementaly building up the logic or neural networks I will be able to obtain a greater understanding of how they work and what considerations go into developing AI for less trivial applications. As this is a learning excercise it is likely that these learning algorithms will not be as efficient or elegant however I will be working on an ongoing bases to refine them.

 # Game Modes

  - 1 - Player Vs Player - Standard Player Vs Player Tic-Tac-Toe
  - 2 - Player Vs RandomAI - Computer will check possible moves and choose 1 at random
  - 3 - Player Vs ListAI - Computer has a list of possible moves, it will make the first available move from this list
  - 4 - Player Vs LineAI - Computer will search the free spaces on the board for lines which can be completed during it's turn and completes them. This algorithm will both complete the computers lines to win the game and your lines to block you. If no possible lines are present the computer moves at random.
  - 5 - Player Vs BlindAI - Play against Blind AI (Note: Will need to be trained first) 
  - 6 - Blind Training - Training module for blind AI

  # Blind Learning AI
  
  Blind Learning is an extremely simplified machine learning script. The AI has 9 nodes (one for each square on the board) with a weight associated with each. As the AI wins or loses in training these weight values are updated up or down accordingly. As this setup allows the system no visability to the state of the board the AI is ultimately ineffective at developing a strategy to win consistantly against a human player however it functions as a good first step before moving into more complex networks of nodes.
  
# One-Eyed Learning (In Progress)

 After playing with Blind learning I wanted to add additional complexity to work towards an algorithm with the capability of learning the game and possibly developing a winning strategy. For One-Eyed learning I will be creating a set of 27 (9x3) nodes. There will be 9 inputs (one for each tile on the board.) These 9 inputs will have one of three states (free space, x, o) which will each point to one of the afformentioned nodes. These nodes will each in turn connect to the 9 possible outputs on the board with a weight attached. By tallying the weights associated with each possible move the algorithm will decide how to move. After each game the algorithm will modify the weights as required.
 
 I am still in the very early stages of building out this algorithm but will provide more details as I develope the code.
