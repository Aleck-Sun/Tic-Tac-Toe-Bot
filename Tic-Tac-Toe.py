########################################
## Name: Aleck Bowen Sun              ##
##                                    ##
## Program: Tic-Tac-Toe AI            ##
##                                    ##
## Date: November 28, 2020            ##
########################################

#Imports
from tkinter import *
from math import *
from time import *
from random import *

#Size of window
w = 600

root = Tk()
s = Canvas(root, width = w, height = w, background = "white")
s.pack()

#Initial values
def variables():
    global startState, playerState, cpState, finishState, movex, moveo, grid, xMouse, yMouse, moveState
    startState = 0
    playerState = 1
    cpState = 2
    finishState = 3
    movex = "x"
    moveo = "o"
    grid = [0 for x in range(9)]
    xMouse = 0
    yMouse = 0
    moveState = startState

#User choose to go first or second
def pickTurn():
    global grid, moveState

    #Reset game
    variables()
    s.delete("all")
    
    s.create_rectangle(w/6, w/3, w/2, 2*w/3)
    s.create_rectangle(w/2, w/3, 5*w/6, 2*w/3)
    s.create_text(w/3, w/2, text = "first", font = "Arial " + str(int(w/20)))
    s.create_text(2*w/3, w/2, text = "second", font = "Arial " + str(int(w/20)))

#Displays who the winner is
def winnerDisplay(text):
    global moveState

    sleep(1)
    s.delete("all")
    s.create_text(w/2, w/3, text = text, font = "Arial " + str(int(w/10)))
    s.create_text(w/2, 2*w/3, text = "Play Again", font = "Arial " + str(int(w/20)))
    moveState = finishState

#Prints board
def gridBackground():
    s.delete("all")

    #Creates table
    s.create_line(w/3, 0, w/3, w)
    s.create_line(2*w/3, 0, 2*w/3, w)
    s.create_line(0, w/3, w, w/3)
    s.create_line(0, 2*w/3, w, 2*w/3)

    #Cp goes first
    if moveState == cpState:
        compMove()
    
#Updates grid with new move
def updateGrid(move, pos):
    if pos == 0 or pos == 1 or pos == 2:
        yMove = w/6
        xMove = (pos)*w/3 + w/6
        
    elif pos == 3 or pos == 4 or pos == 5:
        yMove = w/2
        xMove = (pos-3)*w/3 + w/6
        
    else:
        yMove = 5*w/6
        xMove = (pos-6)*w/3 + w/6

    #Creates x or o on the board and updates grid to contain move
    grid[pos] = move
    s.create_text(xMove, yMove, text = move, font = "Arial " + str(int(w/4)))
    s.update()

    #Checks if the game has ended, otherwise switch turns
    if winner(grid, plMove):
        winnerDisplay("Player Wins")

    elif winner(grid, cpMove):
        winnerDisplay("Computer wins")

    elif draw(grid):
        winnerDisplay("Draw")

    else:
        #Switches turns after a move
        changeStates()
        if moveState == cpState:
            compMove()

#Checks if the grid spot has space or not
def spaceFree(grid, pos):
    return grid[pos] == 0

#Changes turns between the computer and player
def changeStates():
    global moveState

    #switches the state
    if moveState == playerState:
        moveState = cpState
        
    else:
        moveState = playerState

#Handles player moves and menu options
def mouseClickHandler(event):
    global xMouse, yMouse, moveState, plMove, cpMove

    #Mouse coordinates
    xMouse = event.x
    yMouse = event.y

    #Checks if it is player's turn
    if moveState == playerState:

        #First column
        if xMouse > 0 and xMouse < w/3:
            if yMouse > 0 and yMouse < w/3:
                if spaceFree(grid, 0):
                    updateGrid(plMove, 0)
                
            elif yMouse > w/3 and yMouse < 2*w/3:
                if spaceFree(grid, 3):
                    updateGrid(plMove, 3)
                    
            else:
                if spaceFree(grid, 6):
                    updateGrid(plMove, 6)
            
        #Second column
        elif xMouse > w/3 and xMouse < 2*w/3:
            if yMouse > 0 and yMouse < w/3:
                if spaceFree(grid, 1):
                    updateGrid(plMove, 1)
                
            elif yMouse > w/3 and yMouse < 2*w/3:
                if spaceFree(grid, 4):
                    updateGrid(plMove, 4)

            else:
                if spaceFree(grid, 7):
                    updateGrid(plMove, 7)

        #Third column
        elif yMouse > 0 and yMouse < w/3:
            if spaceFree(grid, 2):
                updateGrid(plMove, 2)
                
        elif yMouse > w/3 and yMouse < 2*w/3:
            if spaceFree(grid, 5):
                updateGrid(plMove, 5)

        else:
            if spaceFree(grid, 8):
                updateGrid(plMove, 8)

    #If in startmenu   
    if moveState == startState:

        #Player chooses to go first
        if xMouse > w/6 and xMouse < w/2 and yMouse > w/3 and yMouse < 2*w/3:
            plMove = movex
            cpMove = moveo
            moveState = playerState
            gridBackground()

        #Player chooses to go second
        if xMouse > w/2 and xMouse < 5*w/6 and yMouse > w/3 and yMouse < 2*w/3:
            plMove = moveo
            cpMove = movex
            moveState = cpState
            gridBackground()
            
    #Play again menu
    if moveState == finishState:

        #User choose to play again
        if xMouse > w/3 and xMouse < 2*w/3 and yMouse > w/2 and yMouse < 3*w/4:
            pickTurn()
            
        

#Computer move
def compMove():
    global moveState

    #Start with arbitrarily small score
    bestScore = float('-inf')

    #If computer is going first, always go top left corner to save computing power
    empty = True
    for i in range(9):
        if not(spaceFree(grid, i)):
            empty = False

    #If not computers first move
    if empty == False:

        #Check all possible moves
        for i in range (9):
            
            #Tests all possible moves and undos later
            if spaceFree(grid, i):
                tryMove(i)
                score = minimax()
                undoMove(i)
                
                if score > bestScore:
                    bestScore = score
                    bestMove = i

    else:
        #Top left corner
        bestMove = 0
        
    #Apply move            
    moveState = cpState
    updateGrid(cpMove, bestMove)


#Minimax algorithm trying to find best move based on testing all outcomes
def minimax():
    #End game states
    #If win
    if winner(grid, cpMove):
        return 5

    #If lose
    elif winner(grid, plMove):
        return -5

    #If drawn
    elif draw(grid):
        return 0

    else:
        #Finds the most favourable outcome in the list of outcomes
        scores = []
        
        for i in range(9):
            #Tests all possible moves recursively and undos later
            if spaceFree(grid, i):
                tryMove(i)
                scores.append(minimax())
                undoMove(i)

        #Takes max if player is computer and min otherwise
        if moveState == cpState:
            return max(scores)
            
        else:
            return min(scores)

#Tests a positive move and see it's results 
def tryMove(pos):
    global grid
    
    if moveState == cpState:
        grid[pos] = cpMove

    else:
        grid[pos] = plMove

    changeStates()

#Undo test moves
def undoMove(pos):
    global grid
    
    grid[pos] = 0

    changeStates()

#Checks if the game is a draw
def draw(grid):

    #Checks if the board is full or not
    i = 0
    full = True
    while i < 9 and full:
        if grid[i] == 0:
            full = False
        i += 1

    return full

#Checks if player has won
def winner(grid, move):
    return (grid[0] == move and grid[1] == move and grid[2] == move or
    grid[3] == move and grid[4] == move and grid[5] == move or
    grid[6] == move and grid[7] == move and grid[8] == move or
    grid[0] == move and grid[3] == move and grid[6] == move or
    grid[1] == move and grid[4] == move and grid[7] == move or
    grid[2] == move and grid[5] == move and grid[8] == move or
    grid[0] == move and grid[4] == move and grid[8] == move or
    grid[2] == move and grid[4] == move and grid[6] == move)
    
    
#Prints Background
root.after(0, pickTurn)

#Mouse Clicks
s.bind("<Button-1>", mouseClickHandler)

s.focus_set()
root.mainloop()

