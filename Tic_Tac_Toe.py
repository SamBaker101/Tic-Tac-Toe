#Tic-Tac-Toe
#Sam Baker 01/13/2020

import random
from time import *
from One import *
import matplotlib.pyplot as plt

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
    def __init__(self):
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
        for move in self.moves_taken:
            print(move, ",", end = ' ')
            self.move_array[move] = self.move_array[move] + ((1 - self.move_array[move])*DRAW_INC)
        self.moves_taken = []

    def updateWeightsWin(self):
        for move in self.moves_taken:
            print(move, ",", end = ' ')
            self.move_array[move] = self.move_array[move] + ((1 - self.move_array[move])*WIN_INC)
        self.moves_taken = []

    def updateWeightsLoss(self):
        for move in self.moves_taken:
            print(move, ",", end = ' ')
            self.move_array[move] = abs(self.move_array[move] - (self.move_array[move])*LOSS_INC)
        self.moves_taken = []

class OneEyeAI:
    def __init__(self, w_range):
        self.Net = self.getNet(w_range)
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

    def getNet(self, w_range):    
        in_list = []
        out_list = []
        for i in range(3):
            for j in range(3):
                in_list.append((i, j, 0))
                in_list.append((i, j, 1))
                in_list.append((i, j, 2))
                out_list.append((i,j))
        Net = buildNet(in_list, out_list, w_range)
        return Net

    def simpleFlatten(self):
        mean = 0
        for link in self.Net:
            mean += link.weight
        mean = mean/len(self.Net)

        for link in self.Net:
            link.weight = (link.weight + mean + 0.5)/3

    # This is all very inneficient, will need work
    def chooseMove(self, board):
        possible = possibleMoves(board)
        
        #define weights for each tile
        for link in self.Net:
            x, y, mark = link.source
            if board[y][x] == mark:
                self.tileweights[x][y].append(link)

        #check possible moves for heighest weight
        w = 0
        choice = possible[0]

        for move in possible:
            (x, y) = move
            total = 0
            for link in self.tileweights[x][y]:
                total += link.weight 
            total = total/len(self.tileweights[x][y])

            if total > w:
                w = total
                choice = self.tileweights[x][y][0].destination
        if choice == (-1, -1):
            print('Something has gone awry with the chooseMove function')

        self.updateLinksUsed(self.tileweights[x][y])
        self.resetTileWeights()
        return choice

    def updateLinksUsed(self, linklist):
        for link in linklist:
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
        5: Blind.chooseMove(board),
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
    while type < 0 or type > 5:
        print('Choose Training Type:')
        print('1 : Linear')
        print('2 : Batch')
        print('3 : Linear 2 - Increments repeated moves after a set number of games')
        print('4 : Linear 3 - Increments weights exclusive to wins or exclusive to losses')
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


def trainPlot(data):
    games = []
    wins = []
    for point in data:
        g, w = point
        games.append(g)
        wins.append(w)
    plt.plot(games, wins)
    plt.show()

def updateCounts(player1, player2, result):
    if result == 0:
        if player1.type: player1.draw_count += 1
        if player2.type: player2.draw_count += 1
    elif result == 1:
        if player1.type: player1.win_count += 1
        if player2.type: player2.loss_count += 1
    elif result == 2:
        if player2.type: player2.win_count += 1
        if player1.type: player1.loss_count += 1

def increment(player, result):
    if player.type:
        if result == 0:
            player.updateWeightsDraw()
        if result == 1:
            player.updateWeightsWin()
        if result == 2:
            player.updateWeightsLoss()

def trainStart():

    train_type = chooseTrainType()
    player1 = choosePlayer1()
    player2 = choosePlayer2()
    n = chooseRounds()

    if train_type == 1:
        trainLinear(player1, player2, n)
    elif train_type == 2:
        trainBatch(player1, player2, n)
    elif train_type == 3:
        trainLinear2(player1, player2, n)
    elif train_type == 4:
        trainLinear3(player1, player2, n)
    else:
        print('Something is wrong: Train start')

def trainTurn(player, opponent, mark, game, turn_count, board):
    (x,y) = (-1, -1)
    (x,y) = player.chooseMove(board)
                   
    if (x == -1) or (y == -1):
        print("Something went wrong, BLIND, PMOVES: ", possibleMoves(board),
                "Turn Count: ", turn_count, "X, Y : ", x, y)
        game = 0
        return game

    else:          
        board = markBoard(x, y, mark, board)

    if checkWin(board):
        game = 0
        return game
    return game

def trainCycle(player1, player2):
        
        turn_count = 0
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
                result = trainTurn(player1, player2, 1, game, turn_count, board)
                if result == 0: return 1

            #Player 2's turn
            if player == 2:
                result = trainTurn(player2, player1, 2, game, turn_count, board)
                if result == 0: return 2

            player += 1
            turn_count += 1

            #Check for draw
            if turn_count > 8:
                game = 0
                return 0

def trainLinear(player1, player2, n):

    player1.resetCounts()
    if player2.type: player2.resetCounts()
        
    win_hold = 0
    game_count = 0
    game_stats = []

    while (game_count < n):
        game_count += 1
        result = trainCycle(player1, player2)
        updateCounts(player1, player2, result)

        increment(player1, result)
        
        if result == 0:
            p2 = 0
        elif result == 1:
            p2 = 2
        else: p2 = 1

        increment(player2, p2)

        if (n-game_count)%100 == 0: 
            print('Games Remaining : ', n-game_count, 'Win Count: ', player1.win_count, 'Win in last 100:', player1.win_count-win_hold)
            game_stats.append((game_count, player1.win_count-win_hold))
            win_hold = player1.win_count

            if player1.type == 2: player1.simpleFlatten()
            if player2.type == 2: player2.simpleFlatten()

    print('Computer 1 : Wins:', player1.win_count, ' Losses: ', player1.loss_count, ' Draws : ', player1.draw_count)
    trainPlot(game_stats)

def trainBatch(player1, player2, n):

    data = []
    batch_count=0
    win_hold = 0

    player1.resetCounts()
    if player2.type: player2.resetCounts()

    if player1.type != 2 or player2.type != 2:
        print('Batch training is currently only implemented for OneEye')
    
    else:
        print('How many batches?')
        m = int(input())
        for round in range(m):
            batch_count += 1

            for game in range(n):
                result = trainCycle(player1, player2)
                updateCounts(player1, player2, result)

            if player1.win_count < player2.win_count:
                for i in range(len(player1.Net)):
                    player1.Net[i].weight = (player1.Net[i].weight + player2.Net[i].weight)/2 
            player2.Net = player2.getNet((0, 1))

            print('Batch: ', batch_count, 'Total Wins: ', player1.win_count, 'Batch Wins: ', player1.win_count - win_hold)
            data.append((batch_count, win_hold - player1.win_count))
            win_hold = player1.win_count
        trainPlot(data)

def trainLinear2(player1, player2, n):
    player1.resetCounts()
    if player2.type: player2.resetCounts()
        
    print('Increment every how many rounds?')
    m = int(input())

    win_links = []
    loss_links = []
    win_last = 0
    loss_last = 0
        

    win_hold = 0
    game_count = 0
    game_stats = []

    while (game_count < n):
        game_count += 1
        result = trainCycle(player1, player2)
        updateCounts(player1, player2, result)

        if result == 1:
            for link in player1.linksused:
                win_links.append(link)
        elif result == 2:
            for link in player1.linksused:
                loss_links.append(link)

        if (game_count%m) == 0:
            

            player1.linksused = []

            for i in range(len(win_links)):
                for j in range(len(win_links)):
                    if i != j and win_links[i] == win_links[j]:
                        for k in range(len(player1.linksused)):
                            if win_links[i] == player1.linksused[k]:
                                break
                            else: player1.linksused.append(win_link[i])

            increment(player1, 1)
            print('WIN LINKS :', end = '')
            for link in player1.linksused:
                print(link, end = ', ')

            player1.linksused = []

            for i in range(len(loss_links)):
                for j in range(int((len(loss_links))/2)+1):
                    if i != j and loss_links[i] == loss_links[j]:
                        for k in range(len(player1.linksused)):
                            if loss_links[i] == player1.linksused[k]:
                                break
                            else: player1.linksused.append(win_link[i])
            increment(player1, 2)
            player1.simpleFlatten()

            print('LOSS LINKS :', end = '')
            for link in player1.linksused:
                print(link, end = ', ')

            win_last = player1.win_count
            loss_last = player1.loss_count
            win_links = []
            loss_links = []

            if player2.type == 2:
                player2.Net = player2.getNet()

        if (n-game_count)%100 == 0: 
            print('Games Remaining : ', n-game_count, 'Win Count: ', player1.win_count, 'Win in last 100:', player1.win_count-win_hold)
            game_stats.append((game_count, player1.win_count-win_hold))
            win_hold = player1.win_count

    print('Computer 1 : Wins:', player1.win_count, ' Losses: ', player1.loss_count, ' Draws : ', player1.draw_count)
    trainPlot(game_stats)

def trainLinear3(player1, player2, n):
    player1.resetCounts()
    if player2.type: player2.resetCounts()
        
    print('Increment every how many rounds?')
    m = int(input())

    win_links = []
    loss_links = []
    win_last = 0
    loss_last = 0
        

    win_hold = 0
    game_count = 0
    game_stats = []

    while (game_count < n):
        game_count += 1
        result = trainCycle(player1, player2)
        updateCounts(player1, player2, result)

        if result == 1:
            for link in player1.linksused:
                win_links.append(link)
        elif result == 2:
            for link in player1.linksused:
                loss_links.append(link)
        if (game_count%m) == 0:

            player1.linksused = []

            for link in win_links:
                temp = 0
                for j in loss_links:
                    if link.source == j.source:
                        temp = 1
                if temp == 0:
                    player1.linksused.append(link)
            
            print('WIN LINKS :', end = '')
            for link in player1.linksused:
                print(link.source, ',', link.destination, ',', end = ' - ')
            print('')
            
            increment(player1, 1)
            player1.linksused = []

            for link in loss_links:
                temp = 0
                for j in win_links:
                    if link.source == j.source:
                        temp = 1
                if temp == 0:
                    player1.linksused.append(link)

            print('LOSS LINKS :', end = '')
            for link in player1.linksused:
                print(link.source, ',', link.destination, ',', end = ' - ')
            print('')

            increment(player1, 2)
            player1.simpleFlatten()

            win_last = player1.win_count
            loss_last = player1.loss_count
            win_links = []
            loss_links = []

            if player2.type == 2:
                player2.Net = player2.getNet()

        if (n-game_count)%100 == 0: 
            print('Games Remaining : ', n-game_count, 'Win Count: ', player1.win_count, 'Win in last 100:', player1.win_count-win_hold)
            game_stats.append((game_count, player1.win_count-win_hold))
            win_hold = player1.win_count



#######################################################
#                        Main                         #
#######################################################

Random = RandomAI()
List = ListAI()
Line = LineAI()

Blind = BlindAI()
Blind2 = BlindAI()

OneEye = OneEyeAI((0.499, 0.501))
OneEye2 = OneEyeAI((0, 1))

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
