#Tic-Tac-Toe
#Sam Baker 01/13/2020

import random
from time import *
from One import *

#######################################################
#                     Constants                       #
#######################################################

WIN_INC = 0.005
DRAW_INC = 0.001
LOSS_INC = 0.005

#######################################################
#                       General                       #
#######################################################

def chooseMode():
    choice = 0
    while choice < 1 or choice > 7:
        print("Please choose a mode:")
        print("1 - Player Vs Player")
        print("2 - Player Vs RandomAI")
        print("3 - Player Vs ListAI")
        print("4 - Player Vs LineAI")
        print("5 - Player Vs Blind1")
        print("6 - Player Vs OneEye")
        print("7 - Training")
        choice = int(input())    
    return choice

def setBoard():
    board = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
    return board

def drawBoard(board):
    k = 0
    print("     0   1   2 ")
    print("   /-----------")
    for i in range(3):
        print(k, " |", end = "")
        k += 1
        for j in range(3):
            if board[i][j] == 0:
                print("   ", end = " ")
            elif board[i][j] == 1: 
                print(" O ", end = " ")
            elif board[i][j] == 2:
                print(" X ", end = " ")
            else:
                print('something went wrong', i,',', j)
        print("")

def takeInput():
    x, y = -1, -1
    while (x < 0 or x > 3) or (y < 0 or y > 3):
        print("please choose a square")
        print("X:")
        x = int(input())
        print("Y:")
        y = int(input())
    return (x, y)

#######################################################
#                Turn / Board Checks                  #
#######################################################

def takeTurn(player, board):
    
    print("")
    print("Player", player, ": ")
    print("")
    (x, y) = takeInput()
    new_board = markBoard(x, y, player, board)
    while(new_board == -1):
        (x, y) = takeInput()
        new_board = markBoard(x, y, player, board)
    drawBoard(new_board)
    return new_board

def checkBoard(x, y, board):
    if board[y][x] == 0:
        return True
    return False

def markBoard(x, y, mark, board):
    if (checkBoard(x, y, board) != True):
        print("Not a valid move!")
        return 
    else:
        board[y][x] = mark
    return board

def possibleMoves(board):
    moves = []
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == 0:
                moves.append((j, i))
    return moves

def checkWin(board):
    for i in range(3):
        if board[i][0] != 0:
            if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
                return True
        if board[0][i] != 0: 
            if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
                return True
    if board[1][1] != 0:
        if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return True
        elif board[2][0] == board[1][1] and board[1][1] == board[0][2]:
            return True
   
    return False

#######################################################
#                     Learning                        #
#######################################################

class BlindAI:
    def __init__(self, name):
        self.AI_name = name
        self.moves_taken = []
        self.win_count = 0
        self.loss_count = 0
        self.draw_count = 0
        self.move_array = self.buildMoveArray()
        self.type = 1

    def buildMoveArray(self):
        move_array = {}
        for i in range(3):
            for j in range(3):
                move_array[(i, j)] = random.uniform(0.49999, 0.50001)
        return move_array

    def resetCounts(self):
        self.win_count = 0
        self.loss_count = 0
        self.draw_count = 0

    def chooseMove(self, board):
        (x, y), w = (-1, -1), 0
        possible_moves = possibleMoves(board)
        for move in possible_moves:
            if self.move_array[move] > w:
                (x, y) = move
                #print(move, ",", end = ' ')
        return x,y

    def printWeights(self):
        for i in range(3):
            for j in range(3):
                print('X, Y: ', i, j, ' Weight:', self.move_array[(i,j)])

    def updateWeightsDraw(self):
        print("Draw : ", end = '')
        for move in self.moves_taken:
            print(move, ",", end = ' ')
            self.move_array[move] = self.move_array[move] + ((1 - self.move_array[move])*DRAW_INC)
        self.moves_taken = []

    def updateWeightsWin(self):
        print("Win : ", end = '')
        for move in self.moves_taken:
            print(move, ",", end = ' ')
            self.move_array[move] = self.move_array[move] + ((1 - self.move_array[move])*WIN_INC)
        self.moves_taken = []

    def updateWeightsLoss(self):
        print("Loss: ", end = '')
        for move in self.moves_taken:
            print(move, ",", end = ' ')
            self.move_array[move] = abs(self.move_array[move] - (self.move_array[move])*LOSS_INC)
        self.moves_taken = []

class OneEyeAI:
    def __init__(self):
        self.Net = self.getNet()
        self.tileweights = [[[], [], []],[[], [], []],[[], [], []]]
        self.linksused = []
        self.win_count = 0
        self.loss_count = 0
        self.draw_count = 0
        self.type = 2

    #Troubleshooting function to show variables
    def showMe(self, board, move):
        possible = possibleMoves(board)
        print('PMOVES:', possible)
        #for move in possible:
         #   x, y = move
          #  total = 0
           # for weight in self.tileweights[x][y]:
            #    total += weight 
            #total = total/9
            #print('X, Y' , x, ',', y, 'Total', total)
        print('MOVE: ', move)
        
    def resetCounts(self):
        self.win_count = 0
        self.loss_count = 0
        self.draw_count = 0

    def getNet(self):    
        in_list = []
        out_list = []
        for i in range(3):
            for j in range(3):
                in_list.append((i, j, 0))
                in_list.append((i, j, 1))
                in_list.append((i, j, 2))
                out_list.append((i,j))
        Net = buildNet(in_list, out_list)
        return Net

    # This is all very inneficient, will need work
    def chooseMove(self, board):
        possible = possibleMoves(board)
        
        #define weights for each tile
        for link in self.Net:
            x, y, mark = link.source
            if board[y][x] == mark:
                self.tileweights[x][y].append(link.weight)

        #check possible moves for heighest weight
        w = 0
        choice = possible[0]

        for move in possible:
            (x, y) = move
            total = 0
            for weight in self.tileweights[x][y]:
                total += weight 
            total = total/9

            if total > w:
                w = total
                choice = move
        if choice == (-1, -1):
            print('Something has gone awry with the chooseMove function')

        self.resetTileWeights()
        return choice

    def updateLinksUsed(self, x, y, board):
        for link in self.Net:
            xs, ys, mark = link.source
            xd, yd = link.destination
            if (board[ys][xs] == mark) and (xd, yd) == (x, y):
                self.linksused.append(link)

    def updateWeightsDraw(self):
        for link in self.linksused:
            link.weight = link.weight + ((1 - link.weight)*DRAW_INC)
        self.linksused = []

    def updateWeightsWin(self):
        for link in self.linksused:
            link.weight = link.weight + ((1 - link.weight)*random.uniform(0.01, 0.5))
        self.linksused = []

    def updateWeightsLoss(self):
        for link in self.linksused:
            link.weight = link.weight - ((link.weight)*random.uniform(0.01, 0.5))
        self.linksused = []

    def resetTileWeights(self): self.tileweights = [[[], [], []],[[], [], []],[[], [], []]]

#######################################################
#                   Logical   AI                      #
#######################################################

def takeTurnAI(board, mode):
    x, y = -1, -1
    switcher = {
        2: Random.chooseMove(board),
        3: List.chooseMove(board),
        4: Line.chooseMove(board),
        5: Blind1.chooseMove(board),
        6: OneEye.chooseMove(board)}
    x, y = switcher.get(mode, "Invalid Mode Selection")
    if (x >= 0 and x < 3) and y >= 0 and y < 3:
        board = markBoard(x, y, 2, board)
    else:
        print('Something has gone terribly wrong')
        print('X returned: ', x)
        print('Y returned: ', y)
    print("")
    print("Player 2: ")
    print("")

    drawBoard(board)
    return board  

class RandomAI():
    def __init__(self):
        self.type = 0

    def chooseMove(self, board):
        possible_moves = possibleMoves(board)
        x, y = random.choice(possible_moves)
        return x, y
    
class ListAI():
    def __init__(self):
        self.type = 0

    def chooseMove(self,board):
        move_list = [(1, 1), (0, 0), (2, 2), 
                     (2, 0), (0, 2), (0, 1), 
                     (2, 1), (1, 0), (1, 2)]
        for (x, y) in move_list:
            if checkBoard(x, y, board):
                return x, y

class LineAI():
    def __init__(self):
        self.type = 0

    def chooseMove(self, board):
        x, y = -1, -1
        possible_moves = possibleMoves(board)
       
        for (j, i) in possible_moves:
            if (board[(i+1)%3][j] != 0) and (board[(i+1)%3][j] == board[(i+2)%3][j]):
                x, y =  j, i
            elif (board[i][(j+1)%3] != 0) and (board[i][(j+1)%3] == board[i][(j+2)%3]):
                x, y = j, i
            elif i == j:
                if (board[(i+1)%3][(j+1)%3] != 0) and (board[(i+1)%3][(j+1)%3] == board[(i+2)%3][(j+2)%3]):
                    x, y = j, i
            elif i+j == 2:
                if (board[(i-1)%3][(j+1)%3] != 0) and (board[(i-1)%3][(j+1)%3] == board[(i-2)%3][(j+2)%3]):
                    x, y = j, i

        if x == -1 or y == -1:
            (x, y) = random.choice(possible_moves)

        return x, y

#######################################################
#                       Training                      #
#######################################################
  
def chooseRounds():
    print('How many rounds of training')
    n = int(input())
    return n

def chooseTrainType():
    type = -1
    while type < 0 or type > 3:
        print('Choose Training Type:')
        print('1 : Linear')
        print('2 : Batch')
        type = int(input())
    return type

def choosePlayer1():
    player = -1
    print('Choose AI to Train:')
    print('1 : Blind')
    print('2 : OneEye')
    n = int(input())
    switcher = {
        1: Blind,
        2: OneEye}
    player = switcher.get(n, "Invalid Mode Selection")
    return player

def choosePlayer2():
    player = -1
    print('Choose Player2:')
    print('1 : Blind')
    print('2 : OneEye')
    print('3 : Random')
    print('4 : Line')
    n = int(input())
    switcher = {
        1: Blind2,
        2: OneEye2,
        3: Random,
        4: Line}
    player = switcher.get(n, "Invalid Mode Selection")
    return player

def trainStart():

    train_type = chooseTrainType()
    player1 = choosePlayer1()
    player2 = choosePlayer2()
    n = chooseRounds()

    if train_type == 2:
        trainBatch(player1, player2, n, train_type)
    else:
        trainCycle(player1, player2, n, train_type)

def trainCycle(player1, player2, n, type):
        
        player1.resetCounts()
        if player2.type: player2.resetCounts()
        
        win_hold = 0

        while (n > 0):
            turn_count = 0
            n -= 1
            board = setBoard()
            game = 1
            player = random.randint(1,2)

            if player1.type == 2: player1.linksused = []
            if player2.type == 2: player2.linksused = []
            
            while(game):
                
                if player > 2:
                    player = 1
                
                #Primary AI's turn
                if player == 1:
                    (x,y) = (-1, -1)
                    (x,y) = player1.chooseMove(board)
                   
                    if (x == -1) or (y == -1):
                        print("Something went wrong, BLIND, PMOVES: ", possibleMoves(board),
                              "Turn Count: ", turn_count, "X, Y : ", x, y)
                        game = 0
                        break
                    else:
                        
                        board = markBoard(x, y, player, board)
                        if player1.type == 2: player1.updateLinksUsed(x, y, board)

                    if checkWin(board):
                        if player1.type: 
                            player1.updateWeightsWin()
                            player1.win_count += 1
                        if player2.type:
                            player2.updateWeightsLoss()
                            player2.loss_count += 1
                        game = 0
                        break
    
                #Player 2's turn
                if player == 2:
                    (x,y) = (-1, -1)
                    (x,y) = player2.chooseMove(board)
                   
                    if (x == -1) or (y == -1):
                        print("Something went wrong, BLIND, PMOVES: ", possibleMoves(board),
                              "Turn Count: ", turn_count, "X, Y : ", x, y)
                        game = 0
                        break
                    else:
                        
                        board = markBoard(x, y, player, board)
                        if player2.type == 2: player2.updateLinksUsed(x, y, board)

                    if checkWin(board):
                        if player2.type: 
                            player2.updateWeightsWin()
                            player2.win_count += 1
                        if player1.type:
                            player1.updateWeightsLoss()
                            player1.loss_count += 1
                        game = 0
                        break
                
                player += 1
                turn_count += 1

                #Check for draw
                if turn_count > 8:
                    game = 0
                    if player1.type:
                        player1.updateWeightsDraw()
                        player1.draw_count += 1
                    if player2.type:
                        player2.updateWeightsDraw()
                        player2.draw_count += 1
                    break

            if n%100 == 0 and type == 1: 
                print('Games Remaining : ', n, 'Win Count: ', player1.win_count, 'Win/100', player1.win_count-win_hold)
                win_hold = player1.win_count

        print('Computer 1 : Wins:', player1.win_count, ' Losses: ', player1.loss_count, ' Draws : ', player1.draw_count)

def trainBatch(player1, player2, n):

    if player1.type != 2 or player2.type != 2:
        print('Batch training is currently only implemented for OneEye')
    
    else:
        print('How many batches?')
        m = int(input())
        for round in range(m):
            trainCycle(player1, player2, n)
            if player1.win_count < player2.win_count:
                for i in range(len(self.Net)):
                    player1.Net[i].weight = (player1.Net[i].weight + player2.Net[i].weight)/2 
            player2.Net = player2.getNet()

#######################################################
#                        Main                         #
#######################################################

Random = RandomAI()
List = ListAI()
Line = LineAI()

Blind = BlindAI('Blind1')
Blind2 = BlindAI('Blind2')

OneEye = OneEyeAI()
OneEye2 = OneEyeAI()

def main():

    mode = 2
    running = True
    won = False
    player = 1
    board = setBoard()
    while(running):
        mode = chooseMode()

        if mode == 7:
            trainStart()
            won = True

        turn_count = 0
        player = random.randint(1,2)
        drawBoard(board)
        while(not(won)):
            if player == 2 and mode != 1:
                board = takeTurnAI(board, mode)
            else:
                board = takeTurn(player, board)
            
            if checkWin(board) == True:
                print("")
                print("PLAYER", player, "WINS!!!!!!!")
                print("")
                break

            player += 1
            turn_count += 1 

            if player > 2:
                player = 1

            if turn_count > 8:
                print("DRAW!!")
                won = True

            sleep(0.5)
        
        print("")
        print("Would you like to continue: y/n")
        if input() == "y":
            won = False
            board = setBoard()
            continue
        else:
            running = False

#######################################################

main()
