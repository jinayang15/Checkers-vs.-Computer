from graphics import *
import sys
import threading
import glob

def opening():
    #draw opening
    text = Text(Point(400,200), "Checkers")
    text.setSize(36)
    text.setFace("courier")
    text.setStyle("bold")
    text.draw(glob.win)
    line = Line(Point(275, 200), Point(250, 134))
    line.setWidth(3)
    line.draw(glob.win)
    line = Line(Point(250, 135), Point(340, 160))
    line.setWidth(3)
    line.draw(glob.win)
    line = Line(Point(340, 160), Point(400, 120))
    line.setWidth(3)
    line.draw(glob.win)
    line = Line(Point(400, 120), Point(460, 160))
    line.setWidth(3)
    line.draw(glob.win)
    line = Line(Point(550, 135), Point(460, 160))
    line.setWidth(3)
    line.draw(glob.win)
    line = Line(Point(525, 200), Point(550, 135))
    line.setWidth(3)
    line.draw(glob.win)
    text = Text(Point(400,235), "but not really....")
    text.setSize(11)
    text.setFace("courier")
    text.draw(glob.win)
    text = Text(Point(400,350), "Play Game")
    text.setSize(36)
    text.setFace("courier")
    text.setStyle("bold")
    text.draw(glob.win)
    circle = Circle(Point(225,350),10)
    circle.setFill("black")
    circle.draw(glob.win)
    circle = Circle(Point(575,350),10)
    circle.setFill("black")
    circle.draw(glob.win)

def rules():
    #rules screen
    text = Text(Point(400,100), "Checkers Rules")
    text.setSize(36)
    text.setFace("courier")
    text.setStyle("bold")
    text.draw(glob.win)
    text = Text(Point(340,175), "1. The goal of the game is to capture all of the opponents pieces.")
    text.setSize(12)
    text.setFace("courier")
    text.draw(glob.win)
    text = Text(Point(400,200), "2. To capture opponents pieces you can jump over them diagonally as many times")
    text.setSize(12)
    text.setFace("courier")
    text.draw(glob.win)
    text = Text(Point(185,225), "as possible within the rules.")
    text.setSize(12)
    text.setFace("courier")
    text.draw(glob.win)
    text = Text(Point(310,250), "3. You can jump over your own pieces without capturing them.")
    text.setSize(12)
    text.setFace("courier")
    text.draw(glob.win)
    text = Text(Point(380,275), "4. Pieces can only move forward diaginally, red can only move up and white")
    text.setSize(12)
    text.setFace("courier")
    text.draw(glob.win)
    text = Text(Point(130,300), "can only move down")
    text.setSize(12)
    text.setFace("courier")
    text.draw(glob.win)
    text = Text(Point(400,325), "5. Pieces can be 'kinged' once they reach the eighth row on the other side and")
    text.setSize(12)
    text.setFace("courier")
    text.draw(glob.win)
    text = Text(Point(265,350), "and then can move in any direction diagonally")
    text.setSize(12)
    text.setFace("courier")
    text.draw(glob.win)
    text = Text(Point(150,400), "by Jina Yang")
    text.setSize(24)
    text.setFace("courier")
    text.draw(glob.win)

def buttons():
    #exit game and new game buttons
    button1 = Rectangle(Point(625,50),Point(750,100))
    txt = Text(Point(687.5, 75), "Exit Game")
    txt.draw(glob.win)
    button1.draw(glob.win)
    button1 = Rectangle(Point(625,125),Point(750,175))
    txt = Text(Point(687.5, 150), "New Game")
    txt.draw(glob.win)
    button1.draw(glob.win)

def boardSetup():   
    #in the main board, 0 will denote light spaces,1 for black empty spaces, 2 for white pieces, 3 for orange pieces
    #in the graphics board, I will be adding every object into their designated list
    x = y = start = 40
    side = 65
    radius = 25
    
    for i in range(8):
        for j in range(8):
            block = Rectangle(Point(x,y), Point(x+side,y+side))
            #if the coordinates of the square are both even the block is tan
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                block.setFill("#ffe5b5")
                block.setOutline("#ffe5b5")
                glob.mainBoard[i].append(0)
                glob.graphBoard[i].append(block)
                block.draw(glob.win)
            #otherwise it is brown
            else:
                block.setFill("#451e00")
                block.setOutline("#451e00")
                block.draw(glob.win)
                piece = Circle(Point((2*x+side)/2, (2*y+side)/2), 25)
                #the last three rows of the board that are black contain white pieces
                if i < 3:
                    piece.setFill("white")
                    piece.setOutline("white")
                    glob.graphWhitePieces.append(piece)
                    glob.mainBoard[i].append(2)
                    glob.graphBoard[i].append(piece)
                #the first three rows of the board that are black contain orange pieces
                elif i > 4:
                    piece.setFill("#fc861e")
                    piece.setOutline("#fc861e")
                    glob.graphRedPieces.append(piece)
                    glob.mainBoard[i].append(3)
                    glob.graphBoard[i].append(piece)
                else:
                    glob.mainBoard[i].append(1)
                    glob.graphBoard[i].append(block)
            #if reached end of the row
            if x >= start + side*7:
                x = start
                y += side
            else:
                x += side
    #draw pieces
    for i in glob.graphWhitePieces:
        i.draw(glob.win)
    for i in glob.graphRedPieces:
        i.draw(glob.win)
    #border
    border = Rectangle(Point(start-3,start-3),Point(start+side*8+3,start + side*8+3))
    border.setWidth(5)
    border.draw(glob.win)
    buttons()

def selHighlight(highlight):
    #draws highlight around selected piece
    highlight.setOutline("red")
    highlight.setWidth(5)
    highlight.draw(glob.win)

def isRed(piece):
    #check if piece is red
    if piece in glob.graphRedPieces:
        return True
    return False

def isWhite(piece):
    #check if piece is white
    if piece in glob.graphWhitePieces:
        return True
    return False

def isKing(piece, kings):
    #check if piece is a king
    if piece in kings:
        return True
    return False

def findIndex(piece):
    #find the index of piece in graphBoard
    for a in range(8):
        for b in range(8):
            #if the current piece matches on graphBoard
            if piece == glob.graphBoard[a][b]:
                return a, b

def findBlankSpaces(movesList, i, j, ogpiece, kings, ai):
    #path is for AI so every move can be tracked properly
    path = [[i,j]]
    #if piece is a king
    if isKing(ogpiece,kings):
        if i - 1 >= 0:
            #check top left
            if j - 1 >= 0:
                #if empty space is found
                if glob.mainBoard[i-1][j-1] == 1:
                    #if the move is not already in the movesList
                    if [i-1,j-1] not in movesList:
                        movesList.append([i-1,j-1])
                    #if its AI's turn, add this move to current path
                    if ai == True:
                        path.append([i-1,j-1])
            #same as above
            #check top right
            if j + 1 <= 7:
                if glob.mainBoard[i-1][j+1] == 1:
                    if [i-1,j+1] not in movesList:
                        movesList.append([i-1,j+1])
                    if ai == True:
                        path.append([i-1,j+1])
        if i + 1 <= 7:
            #check bottom left
            if j - 1 >= 0:
                if glob.mainBoard[i+1][j-1] == 1:
                    if [i+1,j-1] not in movesList:
                        movesList.append([i+1,j-1])
                    if ai == True:
                        path.append([i+1,j-1])
            #check bottom right
            if j + 1 <= 7:
                if glob.mainBoard[i+1][j+1] == 1:
                    if [i+1,j+1] not in movesList:
                        movesList.append([i+1,j+1])
                    if ai == True:
                        path.append([i+1,j+1])
    else:
        #i is calculated based on the color of the piece bc they go in opposite directions
        if isRed(ogpiece):
            direct = -1
        elif isWhite(ogpiece):
            direct = 1
        #if red, check top left and top right, if white, check bottom left and right
        #make sure i is in range
        if i + direct >= 0 and i + direct <= 7:
            if j - 1 >= 0:
                if glob.mainBoard[i+direct][j-1] == 1:
                    if [i+direct,j-1] not in movesList:
                        movesList.append([i+direct,j-1])
                    if ai == True:
                        path.append([i+direct,j-1])
            if j + 1 <= 7:
                if glob.mainBoard[i+direct][j+1] == 1:
                    if [i+direct,j+1] not in movesList:
                        movesList.append([i+direct,j+1])
                    if ai == True:
                        path.append([i+direct,j+1])
    #add path to the list of AI's available directly diagonal spaces
    if ai == True and len(path) > 1:
        glob.aiBlanks.append(path)
    return

def findJumps(movesList, i, j, ogpiece, kings, tempBoard, captures, path, a ,b):
    #i, j changes depending on the current space that is being checked
    #a, b is the ogpiece's index
    #tempBoard is to help find jumps
    #captures keeps track of potential captures
    jump = 2
    #this is to check if moves were added
    checkList = movesList.copy()
    if isKing(ogpiece, kings):
        if i - jump >= 0:
            #check top left
            if j - jump >= 0:
                #if the diagonal 2 spaces away is empty, check if there is a piece that can be jumped
                if tempBoard[i-jump][j-jump] == 1 and tempBoard[i-jump+1][j-jump+1] > 1:
                    if [i-jump,j-jump] not in movesList:
                        movesList.append([i-jump,j-jump])
                    #depending on the original piece's color, change the found empty space in tempBoard. This is to prevent infinite loops
                    if isRed(ogpiece):
                        tempBoard[i-jump][j-jump] = 3
                    elif isWhite(ogpiece):
                        tempBoard[i-jump][j-jump] = 2
                    #add current piece and the piece to be jumped to the path
                    path.append([i,j])
                    path.append([i-jump+1, j-jump+1])
                    #continue finding more pieces to jump over by finding jumps for the jump we just found
                    findJumps(movesList, i-jump, j-jump, ogpiece, kings, tempBoard, captures, path, a ,b)
                    #reset path if new jump paths were not found from the original piece
                    if i == a and j == b:
                        path = []
                    else:
                        #if alternative jumps were found (ex. if the first jump can then make a second jump in two different directions), make a new list that starts
                        #before the previous paths jumped piece
                        for q in range (len(path)):
                            if path[q] == [i-jump+1, j-jump+1]:
                                path = path[:q-1]
                                break
            #same as above
            #check top right
            if j + jump <= 7:
                if tempBoard[i-jump][j+jump] == 1 and tempBoard[i-jump+1][j+jump-1] > 1:
                    if [i-jump,j+jump] not in movesList:
                        movesList.append([i-jump,j+jump])
                    if isRed(ogpiece):
                        tempBoard[i-jump][j+jump] = 3
                    elif isWhite(ogpiece):
                        tempBoard[i-jump][j+jump] = 2
                    path.append([i,j])
                    path.append([i-jump+1, j+jump-1])
                    findJumps(movesList,i-jump,j+jump,ogpiece,kings, tempBoard, captures, path, a ,b)
                    if i == a and j == b:
                        path = []
                    else:
                        for q in range (len(path)):
                            if path[q] == [i-jump+1, j+jump-1]:
                                path = path[:q-1]
                                break
        if i + jump <= 7:
            #check bottom left
            if j - jump >= 0:
                if tempBoard[i+jump][j-jump] == 1 and tempBoard[i+jump-1][j-jump+1] > 1:
                    if [i+jump,j-jump] not in movesList:
                        movesList.append([i+jump,j-jump])
                    if isRed(ogpiece):
                        tempBoard[i+jump][j-jump] = 3
                    elif isWhite(ogpiece):
                        tempBoard[i+jump][j-jump] = 2
                    path.append([i,j])
                    path.append([i+jump-1, j-jump+1])
                    findJumps(movesList,i+jump,j-jump,ogpiece,kings,tempBoard, captures, path, a ,b)
                    if i == a and j == b:
                        path = []
                    else:
                        for q in range (len(path)):
                            if path[q] == [i+jump-1, j-jump+1]:
                                path = path[:q-1]
                                break
            #check bottom right
            if j + jump <= 7:
                if tempBoard[i+jump][j+jump] == 1 and tempBoard[i+jump-1][j+jump-1] > 1:
                    if [i+jump,j+jump] not in movesList:
                        movesList.append([i+jump,j+jump])
                    if isRed(ogpiece):
                        tempBoard[i+jump][j+jump] = 3
                    elif isWhite(ogpiece):
                        tempBoard[i+jump][j+jump] = 2
                    path.append([i,j])
                    path.append([i+jump-1, j+jump-1])
                    findJumps(movesList,i+jump,j+jump,ogpiece,kings,tempBoard, captures, path, a ,b)
                    if i == a and j == b:
                        path = []
                    else:
                       for q in range (len(path)):
                            if path[q] == [i+jump-1, j+jump-1]:
                                path = path[:q-1]
                                break
    else:
        #same as above except for non-king pieces
        if isRed(ogpiece):
            direct = -1
        elif isWhite(ogpiece):
            direct = 1
        #if red, check top left and top right, if white, check bottom left and right
        if i + direct*jump >= 0 and i + direct*jump <= 7:
            #top/bottom left
            if j - jump >= 0:
                if tempBoard[i+direct*jump][j-jump] == 1 and tempBoard[i+direct*jump+1*(-direct)][j-jump+1] > 1:
                    if [i+direct*jump,j-jump] not in movesList:
                        movesList.append([i+direct*jump,j-jump])
                    if isRed(ogpiece):
                        tempBoard[i+direct*jump][j-jump] = 3
                    elif isWhite(ogpiece):
                        tempBoard[i+direct*jump][j-jump] = 2
                    path.append([i,j])
                    path.append([i+direct*jump+1*(-direct),j-jump+1])
                    findJumps(movesList,i+jump*direct,j-jump,ogpiece,kings,tempBoard, captures, path, a ,b)
                    if i == a and j == b:
                        path = []
                    else:
                        for q in range (len(path)):
                            if path[q] == [i+direct*jump+1*(-direct),j-jump+1]:
                                path = path[:q-1]
                                break
            #top/bottom right
            if j + jump <= 7:
                if tempBoard[i+direct*jump][j+jump] == 1 and tempBoard[i+direct*jump+1*(-direct)][j+jump-1] > 1:
                    if [i+direct*jump,j+jump] not in movesList:
                        movesList.append([i+direct*jump,j+jump])
                    if isRed(ogpiece):
                        tempBoard[i+direct*jump][j+jump] = 3
                    elif isWhite(ogpiece):
                        tempBoard[i+direct*jump][j+jump] = 2
                    path.append([i,j])
                    path.append([i+direct*jump+1*(-direct),j+jump-1])
                    findJumps(movesList,i+jump*direct,j+jump,ogpiece,kings,tempBoard, captures, path, a ,b)
                    if i == a and j == b:
                        path = []
                    else:
                        for q in range (len(path)):
                            if path[q] == [i+direct*jump+1*(-direct),j+jump-1]:
                                path = path[:q-1]
                                break
    #if no new moves were added to path
    if checkList == movesList:
        #if there is moves in path add path to the potential captures list and reset tempBoard
        if len(path) > 0:
            path.append([i,j])
            captures.append(path)
            tempBoard = [[col for col in row] for row in glob.mainBoard]
        return
                    

def showOptions(movesList, graphMoves):
    #draws all available options according to movesList
    graphMoves = []
    for k in range (len(movesList)):
        movei = movesList[k][0]
        movej = movesList[k][1]
        block = glob.graphBoard[movei][movej]
        x = (block.getP1().getX() + block.getP2().getX())/2
        y = (block.getP1().getY() + block.getP2().getY())/2
        option = Circle(Point(x,y), glob.select.getRadius())
        option.setOutline("#c4c8cf")
        graphMoves.append(option)
        option.draw(glob.win)
    return graphMoves

def undrawOptions(graphMoves):
    #undraws options
    for i in range(len(graphMoves)):
        graphMoves[i].undraw()

def movePiece(row,col, move, piece, movesList):
    #moves the piece
    movetorow = movesList[move][0]
    movetocol = movesList[move][1]
    ydirect = movetorow - row
    xdirect = movetocol - col
    #calculates piece move directions
    ydirect *= 65
    xdirect *= 65
    #updating boards
    #get the current selected piece coordinates to calculate the block it is on
    centerx = piece.getCenter().getX()
    centery = piece.getCenter().getY()
    #update selection
    glob.graphBoard[row][col].move(xdirect,ydirect)
    piece = glob.graphBoard[row][col]
    #switch where the piece is in graphBoard and replace its spot with a block
    glob.graphBoard[movetorow][movetocol] = piece
    glob.graphBoard[row][col] = Rectangle(Point(centerx-65/2,centery-65/2),Point(centerx+65/2,centery+65/2))
    glob.graphBoard[row][col].setFill("#451e00")
    glob.graphBoard[row][col].setOutline("#451e00")
    #coordinate mainBoard
    glob.mainBoard[movetorow][movetocol] = glob.mainBoard[row][col]
    glob.mainBoard[row][col] = 1
    return piece

def removePiece(piece, captures):
    a,b = findIndex(piece)
    for i in range(len(captures)):
        for j in range(len(captures[i])):
            #if the piece that was just moved is in the path that is in the potential captures list
            #shorten captures if needed based on selected move
            if captures[i][j] == [a,b]:
                captures[i] = captures[i][:j+1]
                #path keeps track of all the jumped pieces
                path = [captures[i][k] for k in range(len(captures[i])) if k % 2 == 1]
                #check to see if opponents pieces were jumped
                #remove pieces and update boards as necessary
                for n in range (len(path)):
                    row = path[n][0]
                    col = path[n][1]
                    centerx = glob.graphBoard[row][col].getCenter().getX()
                    centery = glob.graphBoard[row][col].getCenter().getY()
                    if isRed(piece) and isWhite(glob.graphBoard[row][col]):
                        glob.graphWhitePieces.remove(glob.graphBoard[row][col])
                        glob.graphBoard[row][col].undraw()
                        glob.graphBoard[row][col] = Rectangle(Point(centerx-65/2,centery-65/2),Point(centerx+65/2,centery+65/2))
                        glob.graphBoard[row][col].setFill("#451e00")
                        glob.graphBoard[row][col].setOutline("#451e00")
                        glob.mainBoard[row][col] = 1
                    elif isWhite(piece) and isRed(glob.graphBoard[row][col]):
                        glob.graphRedPieces.remove(glob.graphBoard[row][col])
                        glob.graphBoard[row][col].undraw()
                        glob.graphBoard[row][col] = Rectangle(Point(centerx-65/2,centery-65/2),Point(centerx+65/2,centery+65/2))
                        glob.graphBoard[row][col].setFill("#451e00")
                        glob.graphBoard[row][col].setOutline("#451e00")
                        glob.mainBoard[row][col] = 1
                return

def reset():
    #draws blank slate
    reset = Rectangle(Point(0,0),Point(800,600))
    reset.setFill("white")
    reset.setOutline("white")
    reset.draw(glob.win)

def gameover():
    #draws game over screen
    text = Text(Point(400,200), "Game Over!")
    text.setSize(36)
    text.setFace("courier")
    text.setStyle("bold")
    text.draw(glob.win)
    text = Text(Point(275,425), "Play Again")
    text.setFace("courier")
    text.draw(glob.win)
    text = Text(Point(525,425), "Exit Game")
    text.setFace("courier")
    text.draw(glob.win)
    button = Rectangle(Point(200,400),Point(350, 450))
    button.draw(glob.win)
    button = Rectangle(Point(450,400),Point(600, 450))
    button.draw(glob.win)




