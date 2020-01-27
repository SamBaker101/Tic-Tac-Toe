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
    while choice < 1 or choice > 8:
        print("Please choose a mode:")
        print("1 - Player Vs Player")
        print("2 - Player Vs RandomAI")
        print("3 - Player Vs ListAI")
        print("4 - Player Vs LineAI")
        print("5 - Player Vs Blind1")
        print("6 - Blind Training")
        print("7 - Player Vs OneEye")
        print("8 - OneEye Training")
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

    def buildMoveArray(self):
        move_array = {}
        for i in range(3):
            for j in range(3):
                move_array[(i, j)] = random.uniform(0.49999, 0.50001)
        return move_array

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

    def train(self, opponent):
        print('How many rounds of training')
        n = int(input())
        train_type = -1
        while train_type < 1 or train_type > 2:
            print('Training Type?')
            print('1 - Random Vs List')
            print('2 - Blind Vs List')
            train_type = int(input())
        while (n >= 0):
            turn_count = 0
            n = n - 1
            board = setBoard()
            game = 1
            player = random.randint(1,2)
            while(game):
                if player > 2:
                    player = 1
                
                if player == 1:
                    if train_type == 1:
                        x, y = takeTurnRandomAI(board)
                    else:
                        x, y = self.chooseMove(board)
                    
                    if (x == -1) or (y == -1):
                        print("Something went wrong, BLIND, PMOVES: ", possibleMoves(board),
                              "Turn Count: ", turn_count, "X, Y : ", x, y)
                        game = 0
                        break
                    else:
                        board = markBoard(x, y, player, board)
                        self.moves_taken.append((x,y))
                    if checkWin(board):
                        self.updateWeightsWin()
                        self.win_count = self.win_count + 1
                        #opponent.updateWeightsLoss()
                        opponent.loss_count = opponent.loss_count + 1
                        game = 0
                        break
    
                if player == 2:
                   if train_type == 3:
                       x, y = self.chooseMove(board)
                   else:
                       x, y = takeTurnLineAI(board)
                   if (x == -1) or (y == -1):
                        print("Something went wrong, LINE, PMOVES: ", possibleMoves(board),
                              "Turn Count: ", turn_count, "X, Y : ", x, y)
                        game = 0
                        break
                   else:
                       board = markBoard(x, y, 2, board)

                   if checkWin(board):
                       #opponent.updateWeightsWin()
                       opponent.win_count = opponent.win_count + 1
                       self.updateWeightsLoss()
                       self.loss_count = self.loss_count + 1
                       game = 0
                       break
                
                player = player + 1
                turn_count = turn_count + 1
                if turn_count > 8:
                    game = 0
                    self.updateWeightsDraw()
                    self.draw_count = self.draw_count + 1
                    #opponent.updateWeightsDraw()
                    opponent.draw_count = opponent.draw_count + 1
                    break

            print('Games Remaining : ', n)
        print('Computer 1 : Wins:', self.win_count, ' Losses: ', self.loss_count, ' Draws : ', self.draw_count)
        self.printWeights()

        print('Computer 2 : Wins:', opponent.win_count, ' Losses: ', opponent.loss_count, ' Draws : ', opponent.draw_count)
        opponent.printWeights()

class OneEyeAI:
    def __init__(self):
        self.Net = self.getNet()
        self.tileweights = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
        self.linksused = []
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
                self.tileweights[x][y] += link.weight
        
        #check possible moves for heighest weight
        w = 0
        choice = (-1, -1)
        for move in possible:
            if self.tileweights[x][y] > w:
                w = self.tileweights[x][y]
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
        print("Draw : ", end = '')
        for link in self.linksused:
            link.weight = link.weight + ((1 - link.weight)*DRAW_INC)
        self.linksused = []

    def updateWeightsWin(self):
        print("Win : ", end = '')
        for link in self.linksused:
            link.weight = link.weight + ((1 - link.weight)*WIN_INC)
        self.linksused = []

    def updateWeightsLoss(self):
        print("Loss: ", end = '')
        for link in self.linksused:
            link.weight = link.weight - ((link.weight)*LOSS_INC)
        self.linksused = []

    def resetTileWeights(self): 
        self.tileweights = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]

    def trainOneEye(self):
        print('How many rounds of training')
        n = int(input())
        train_type = -1
        while train_type < 1 or train_type > 2:
            print('Training Type?')
            print('1 - Random Vs List')
            print('2 - OneEye Vs List')
            train_type = int(input())
        while (n >= 0):
            turn_count = 0
            n = n - 1
            board = setBoard()
            game = 1
            player = random.randint(1,2)
            self.linksused = []
            while(game):
                if player > 2:
                    player = 1
                
                if player == 1:
                    if train_type == 1:
                        x, y = takeTurnRandomAI(board)

                    else:
                        x, y = self.chooseMove(board)
                    
                    if (x == -1) or (y == -1):
                        print("Something went wrong, BLIND, PMOVES: ", possibleMoves(board),
                              "Turn Count: ", turn_count, "X, Y : ", x, y)
                        game = 0
                        break
                    else:
                        board = markBoard(x, y, player, board)                      
                        OneEye.updateLinksUsed(x, y, board)

                    if checkWin(board):
                        self.updateWeightsWin()
                        self.win_count = self.win_count + 1
                        game = 0
                        break
    
                if player == 2:
                   x, y = takeTurnLineAI(board)
                   if (x == -1) or (y == -1):
                        print("Something went wrong, LINE, PMOVES: ", possibleMoves(board),
                              "Turn Count: ", turn_count, "X, Y : ", x, y)
                        game = 0
                        break
                   else:
                       board = markBoard(x, y, 2, board)

                   if checkWin(board):
                       self.updateWeightsLoss()
                       self.loss_count = self.loss_count + 1
                       game = 0
                       break
                
                player = player + 1
                turn_count = turn_count + 1

                if turn_count > 8:
                    game = 0
                    self.updateWeightsDraw()
                    self.draw_count = self.draw_count + 1
                    break

            print('Games Remaining : ', n)
        print('Computer 1 : Wins:', self.win_count, ' Losses: ', self.loss_count, ' Draws : ', self.draw_count)

        for link in self.Net:
            print(link.weight, ', ', end = '')

#######################################################
#                   Logical   AI                      #
#######################################################

def takeTurnAI(board, mode):
    x, y = -1, -1
    switcher = {
        2: takeTurnRandomAI(board),
        3: takeTurnListAI(board),
        4: takeTurnLineAI(board),
        5: Blind1.chooseMove(board),
        7: OneEye.chooseMove(board)}
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

def takeTurnRandomAI(board):
    possible_moves = possibleMoves(board)
    x, y = random.choice(possible_moves)
    return x, y
    
def takeTurnListAI(board):
    move_list = [(1, 1), (0, 0), (2, 2), 
                 (2, 0), (0, 2), (0, 1), 
                 (2, 1), (1, 0), (1, 2)]
    for (x, y) in move_list:
        if checkBoard(x, y, board):
            return x, y

def takeTurnLineAI(board):
    x, y = -1, -1
    possible_moves = possibleMoves(board)
       
    for (j, i) in possible_moves:
        if (board[(i+1)%3][j] != 0) and (board[(i+1)%3][j] == board[(i+2)%3][j]):
            x, y =  j, i
            #print("horizontal")
            #print(board[(i+1)%3][j], board[(i+2)%3][j])
        elif (board[i][(j+1)%3] != 0) and (board[i][(j+1)%3] == board[i][(j+2)%3]):
            x, y = j, i
            #print("Vertical")
            #print(board[i][(j+1)%3], board[i][(j+2)%3])
        elif i == j:
            if (board[(i+1)%3][(j+1)%3] != 0) and (board[(i+1)%3][(j+1)%3] == board[(i+2)%3][(j+2)%3]):
                x, y = j, i
             #   print('Diag 1')
        elif i+j == 2:
            if (board[(i-1)%3][(j+1)%3] != 0) and (board[(i-1)%3][(j+1)%3] == board[(i-2)%3][(j+2)%3]):
                x, y = j, i
             #   print('Diag 2')

    if x == -1 or y == -1:
        (x, y) = random.choice(possible_moves)

    return x, y

#######################################################
#                        Main                         #
#######################################################

Blind1 = BlindAI('Blind1')
Blind2 = BlindAI('Blind2')

OneEye = OneEyeAI()


def main():
    mode = 2
    running = True
    won = False
    player = 1
    board = setBoard()
    while(running):
        mode = chooseMode()

        if mode == 6:
            Blind1.train(Blind2)
            won = True

        if mode == 8:
            OneEye.trainOneEye()
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
