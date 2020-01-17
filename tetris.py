#################################################
#Akshay Gupta
#CMU 112
#Tetris
#Task Description: Create Tetris Game
#https://www.cs.cmu.edu/~112n18/index.html
#################################################

from Tkinter import *
import math
import random
import copy
import time

def preLoad2D(data):
    for r in range(data.rows): #iterates through the number of cells
        row = [] #makes rows of empty color
        for c in range(data.cols):
            row.append(data.emptyColor)
        data.board.append(row) #fills board with rows of empty color

def drawCell(canvas, data, color, row, col): #draws cell based upon the row and col and color
    startX = data.cellWidth * col + data.margin 
    startY = data.cellHeight * row + data.margin 
    endX = data.cellWidth * (col+1) + data.margin 
    endY = data.cellHeight * (row+1) + data.margin 
    canvas.create_rectangle(startX, startY, endX, endY, fill = color, width = 4) 


def drawBoard(canvas, data):
    for r in range(data.rows): #iterates through board and draws every cell
        for c in range(data.cols):
            drawCell(canvas, data, data.board[r][c], r, c)

def listOfShapes(): #method that returns a list of all shapes, for more organized look
    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]

    #add any custom pieces above, just remember to return it in return statement :)
    return [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]

def newFallingPiece(data):
    randomIndex = random.randint(0, len(data.tetrisShapes) - 1) #picks a random number out of the number of different shapes

    data.fallingShape = data.tetrisShapes[randomIndex] #gets a random shape
    data.fallingColor = data.tetrisShapeColors[randomIndex] #takes color of that random shape

    middleTopRow = 0 #starting row 
    middleTopCol = data.cols//2 - ((len(data.fallingShape[0])//2)) #starting column

    data.fallingCoords = [middleTopRow, middleTopCol] #stores top left coords of shape

def drawFallingPiece(canvas, data):
    for r in range(len(data.fallingShape)): #iterates through row of booleans of the falling shape
        for c in range(len(data.fallingShape[r])): #iterataes through columns of booleans of falling shape
            if data.fallingShape[r][c]: #If the shape has a cell at that position, draws in the cell of the shapes color
                drawCell(canvas, data, data.fallingColor, r+data.fallingCoords[0], c+data.fallingCoords[1])

def fallingPieceIsLegal(data):
    startingRow = data.fallingCoords[0] #leftmost row
    startingCol = data.fallingCoords[1] #topmost column
    endingRow = startingRow + len(data.fallingShape) #right most row
    endingCol = startingCol + len(data.fallingShape[0]) #bottommost column
    if startingRow < 0 or startingCol < 0 or endingRow > data.rows or endingCol > data.cols: #checks to see if all of the shape is in the board
        return False

    for r in range(len(data.fallingShape)): #iterates through booleans of fallingShape
        for c in range(len(data.fallingShape[r])): 
            if data.fallingShape[r][c]: #if the shape has a cell at that position
                if data.board[r+startingRow][c+startingCol] != "blue": #if that cell is not empty, then not legal
                    return False
    return True


def moveFallingPiece(data, drow, dcol):
    data.tempCoords = [data.fallingCoords[0], data.fallingCoords[1]] #stores the last coordinates
    data.fallingCoords = [data.fallingCoords[0] + drow, data.fallingCoords[1] + dcol] #changes the coordinates of shape to next position
    if not fallingPieceIsLegal(data): #if the new coordinates aren't legal, resets to previous spot
        data.fallingCoords = data.tempCoords
        return False
    return True

def rotateFallingPiece(data):
    oldCoords = copy.deepcopy(data.fallingCoords) #saves coordinates of top left of falling piece
    oldShape = copy.deepcopy(data.fallingShape) #saves last shape

    newRow = oldCoords[0] + len(data.fallingShape) // 2 - len(data.fallingShape[0]) // 2 #gets the row of new top left of rotated shape
    newCol = oldCoords[1] + len(data.fallingShape[0]) // 2 - len(data.fallingShape) // 2 #gets the col of new top left of rotated shape
    newCoords = [newRow, newCol] #stores top left coordinates

    newFallingShape = [[None] * len(data.fallingShape) for i in range(len(data.fallingShape[0]))] #instanciates new shape 2d array with flipped dimensions

    for r in range(len(data.fallingShape)): #iterates through original shape and puts values in rotated position in newFalling Shape
        newC = r #new column position
        for c in range(len(data.fallingShape[r])):
            newR = len(data.fallingShape[r]) - 1 - c #new row position
            newFallingShape[newR][newC] = data.fallingShape[r][c] #rotates cell

    data.fallingShape = newFallingShape #changes falling shape to rotated version
    data.fallingCoords = newCoords #changes coordinates to rotated top left
    if not fallingPieceIsLegal(data): #if it is not legal, resets back to pre-rotation
        data.fallingCoords = oldCoords
        data.fallingShape = oldShape

def removeFullRows(data):
    rowsRemoved = 0 #counter of rows removed
    tempBoard = [] #temporary board to draw in without full rows
    for r in data.board: #iterates through board and adds to temp board any row that isn't full
        if "blue" in r: #if theres a blue, an empty it isn't full. Adds to temp board
            tempBoard.append(r)
        else: #if there isn't a blue, doesn't add to temp board and increments counter
            rowsRemoved += 1

    data.totalRowsRemoved += rowsRemoved #increments counter to total counter of rows removed
    if rowsRemoved >= 1: #increments points based upon the actual tetris system
        points = 100 * 2**(rowsRemoved-1)
        data.totalPoints += points


    row = []
    for r in range(rowsRemoved): #creates empty rows to add to the top of board to maintain number of cells
        for c in range(data.cols):
            row.append("blue")
        tempBoard.insert(0,row)

    data.board = tempBoard #sets board to version without full rows

def placeFallingPiece(data):
    for r in range(len(data.fallingShape)): #iterates through booleans of shape falling
        for c in range(len(data.fallingShape[r])):
            if data.fallingShape[r][c]: #if falling shape has a cell there
                data.board[r+data.fallingCoords[0]][c+data.fallingCoords[1]] = data.fallingColor #changes the board cell at that spot to the shape color
    removeFullRows(data)
    newFallingPiece(data) #creates a new shape at the top

def hardDrop(data):  
    while moveFallingPiece(data, 1, 0): #moves piece down by one until illegal
        pass 


def init(data):
    # load data.xyz as appropriate
    data.totalRowsRemoved = 0
    data.totalPoints = 0
    data.level = 0
    data.gameOver = False 
    data.timerDelay = 500
    data.margin = 25 #margin of board
    data.rows = 15 #number of rows
    data.cols = 10 #number of columns
    data.cellWidth = int((data.width - 2 * data.margin ) / data.cols) #width of cells
    data.cellHeight = int((data.height - 2 * data.margin )/ data.rows) #height of cells
    data.emptyColor = "blue" #defines the empty color for ease of access
    data.backgroundColor = "gold" #defines background color for earse of access
    data.board = []
    data.tetrisShapes = listOfShapes() #loads tetrisshapes with all possible shapes
    data.paused = False
    data.tetrisShapeColors = ["red", "yellow", "green", "pink", "orange", "white" , "brown", "black"] 
    

    #loads list with colors to corresponding index shapes
    preLoad2D(data) #preloads board with default blue colors


    newFallingPiece(data)
    rotateFallingPiece(data)
    

def mousePressed(event, data):
    # use event.x and event.y
    if data.paused == False: #if its unpaused
        data.paused = True #paused

    else:
        data.paused = False #unpauses if pauses


def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "c": #changes shape when c is pressed
        newFallingPiece(data)
    if event.keysym == "Down": #moves shape down when down is pressed
        moveFallingPiece(data, 1, 0)
    if event.keysym == "Right": # moves shape right when right is pressed 
        moveFallingPiece(data, 0,1)
    if event.keysym == "Left": #moves shape left when left is pressed
        moveFallingPiece(data, 0,-1)
    if event.keysym == "Up": #rotates shape wheen up is pressed
        rotateFallingPiece(data)
    if event.keysym == "r": #restarts game
        init(data)
    if event.char == " ": #hard drops when space is presesd
        hardDrop(data)


def timerFired(data):
    if not data.paused:
        if not data.gameOver: 
            if not moveFallingPiece(data, 1, 0): #if unable to move piece down one
                placeFallingPiece(data) #inscribes piece into board and draws new piece to fall
                if not fallingPieceIsLegal(data): #if the new piece isn't legal at the top, you lose
                    data.gameOver = True

def redrawAll(canvas, data):
    if data.paused:
        canvas.create_text(data.width//2, data.height//2, text = "Paused. To Keep Playing Click. To Restart Press R.", fill = "Red", font = "Helvetica 14 bold")

    else:
        if not data.gameOver:
            # draw in canvas
            canvas.create_rectangle(0,0,data.width,data.height, fill = data.backgroundColor) #creates background
            drawBoard(canvas, data) 

            drawFallingPiece(canvas, data)
            canvas.create_text(data.width//2, 14, text = "Rows Removed: " + str(data.totalRowsRemoved), fill = "black", font = "Helvetica 20 bold")
            canvas.create_text(data.width//2, data.height - 14, text = "Total Points: " + str(data.totalPoints) + " Level: " + str(data.level), fill =  "black", font = "Helvetica 20 bold")
            lev = data.totalPoints // 500 #gets level
            data.level = lev
            data.timerDelay -= lev # increases speed
            
            #displays falling piece and score
        else:
            canvas.create_rectangle(0,0,data.width, data.height, fill = "black")
            canvas.create_text(data.width//2, data.height//2, text = "You lose :(. Press R to try again!", fill = "white", font = "Helvetica 22 bold")
            #displays losing screen


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def playTetris(width = 400, height = 600):
    run(width, height)

playTetris(400,600)


