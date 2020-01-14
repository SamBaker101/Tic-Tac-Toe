#Tic-Tac-Toe
#Sam Baker 01/13/2020

import random
from time import *

######################################################

def chooseMode():
    choice = 0
    while choice < 1 or choice > 3:
        print("Please choose a mode:")
        print("1 - Player Vs Player")
        print("2 - Player Vs RandomAI")
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

def takeTurnAI(board):
    sleep(0.5)
    possible_moves = []
    for i in range(3):
       for j in range(3):
           if checkBoard(i, j, board) == True:
               possible_moves.append((i, j))
    movex, movey = random.choice(possible_moves)
    board = markBoard(movex, movey, 2, board)
    print("")
    print("Player 2: ")
    print("")

    drawBoard(board)
    return board  

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
        drawBoard(board)
        while(not(won)):
            if mode == 2 and player == 2:
                board = takeTurnAI(board)
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
