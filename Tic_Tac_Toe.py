#Tic-Tac-Toe
#Sam Baker 01/13/2020

import random
from time import *

######################################################

def chooseMode():
    choice = 0
    while choice < 1 or choice > 5:
        print("Please choose a mode:")
        print("1 - Player Vs Player")
        print("2 - Player Vs RandomAI")
        print("3 - Player Vs ListAI")
        print("4 - Player Vs LineAI")
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

def checkBoard(x, y, board):
    if board[y][x] == 0:
        return True
    return False

def markBoard(x, y, mark, board):
    if (checkBoard(x, y, board) != True):
        print("Not a valid move!")
        return 0
    else:
        board[y][x] = mark
    return board

def possibleMoves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                moves.append((j, i))
    return moves

def takeInput():
    x, y = 0, 0
    print("please choose a square")
    print("X:")
    x = int(input())
    print("Y:")
    y = int(input())
    return (x, y)

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

def takeTurn(player, board):
    
    print("")
    print("Player", player, ": ")
    print("")
    x, y = takeInput()
    new_board = markBoard(x, y, player, board)
    while(new_board == 0):
        x, y = takeInput()
        new_board = markBoard(x, y, player, board)
    drawBoard(new_board)
    return new_board

def takeTurnAI(board, mode):
    x, y = -1, -1
    switcher = {
        2: takeTurnRandomAI(board),
        3: takeTurnListAI(board),
        4: takeTurnLineAI(board)}
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
    sleep(0.5)
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
       
    for (i, j) in possible_moves:
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
        x, y = random.choice(possible_moves)

    return x, y


##################Game Loop###########################
def main():
    mode = 2
    running = True
    won = False
    player = 1
    board = setBoard()
    while(running):
        mode = chooseMode()
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

######################################################

main()
