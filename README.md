# Tic-Tac-Toe

Sam Baker - 01/12/2020

 A simple command line based Tic Tac Toe game created as a testing ground for logical and machine learning algorithms.
 
 Note in this project I have not used Tensorflow or any other Machine Learning libraries. My thought process with this project is that by incrementaly building up the logic or nueral networks I use I will be able to obtain a greater understanding of how they work and what considerations go into developing AI for less trivial applications.

 # Game Modes

  - 1 - Player Vs Player - Standard Player Vs Player Tic-Tac-Toe
  - 2 - Player Vs RandomAI - Computer will check possible moves and choose 1 at random
  - 3 - Player Vs ListAI - Computer has a list of possible moves, it will make the first available move from this list
  - 4 - Player Vs LineAI - Computer will search the free spaces on the board for lines which can be completed during it's turn and completes them. This algorithm will both complete the computers lines to win the game and your lines to block you. If no possible lines are present the computer moves at random.
  - 5 - Player Vs BlindAI - Play against Blind AI (Note: Will need to be trained first) 
  - 6 - Blind Training - Training module for blind AI

  # Blind Learning AI
  
  Blind Learning is an extremely simplified machine learning script. The AI has 9 nodes (one for each square on the board) with a weight associated with each. As the AI wins or loses in training these weight values are updated up or down accordingly. As this setup allows the system no visability to the state of the board the AI is ultimately ineffective at developing a strategy to win consistantly against a human player however it functions as a good first step before moving into more complex networks of nodes.
  
  - Metrics - As this AI is unable to read the current state of the board (beyond knowing what moves are available) it is not reasonable to expect it to develop the ability to win consistantly or beat human players. Instead I will judge this script to be successful if it consistantly completes training sessions with the center square as its highest weighted move as this is the most advantageous position on the board. At this point the center square is typically within the top 2-3 moves however It has not yet reached the top. 

  - Training - I initially was attempting to train the Blind Learning AI against itself however this proved ineffective as currently there is no element of randomness in the bots decisionmaking. This lead to the two copies of the algorithm incrementing their values up and down in equal measures and ultimately making very little progress. I have now changed the training to play against the Line Check AI which is giving far more encouraging results.

  - Randomness - At this time the only randomness in the algorithm is in the starting weights of the 9 moves. This however can cause some issues as once a move has a high weight it can often run away. For example if the move (2,2) has the highest weight the AI will use it every game, if the AI is winning more games than losing the weight will continue to grow in spite of it not being the best move. One way to combat this may be to have the AI intermittantely take random moves to keep the move set dynamic.

  - Weights - In the randomness segment I pointed to an issue with run away values. One way I have worked to combat this is through my weight adjustment formula. I am using a fomula of w = w + (1-w)*i for wins/draws and w = w - (w)*i for losses where w is the weight and i is the incrementation percent associated with that outcome. This means that if the outcome is contradictory to a moves weight the weight will be adjusted significantly more than if it reinforces it. That is to say a move with a weight of 0.95 will drop far more than a move with weight 0.20 if it is used in a losing game.
