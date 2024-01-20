#Jina Yang
#06/20/21
#This is my code for checkers with basically the same rules as regular checkers (except you can jump over your own pieces) where the player can play against the AI
#until either wins or loses or the AI surrenders. The player can exit game or reset the board at any time and can choose to play again. 
from graphics import *
import time
from random import randint
import glob
glob.init()
import func

'''
Bugs:
- in a very specific board configuration where neither red or white has any moves, you have to create a new game
- white jumps over invisible pieces

***below are the bugs I think are fixed but hard to verify 100%
- white does not capture an orange piece after jumping over
- orange piece does not capture white piece
- white stops moving
- white errors because the piece that is selected is a rectangle
'''

#Colors:
#Brown - #451e00
#Tan - #ffe5b5
#Orange - #fc861e
#Gray - #c4c8cf

#opening
func.opening()
glob.win.getMouse()
func.reset()
func.rules()
glob.win.getMouse()
func.reset()

#board setup
#if player wants to play again
playagain = True
while playagain == True:
    #keeps track of whether player wanted a new game
    newgame = False
    #resets variables
    glob.new()
    #sets up board
    func.boardSetup()
    update()
    
    #player turn
    ######################################################################################################################################################
    #keeps track of game state
    while glob.WorL == 0:
        #keep track of AI turn
        ai = False
        #keep track whether option was selected
        option = False
        click = glob.win.getMouse()
        #check for exit game and new game buttons
        #exit game
        if click.getX() >= 625 and click.getX() <= 750 and click.getY() >= 50 and click.getY() <= 100:
            playagain = False
            break
        #new game
        elif click.getX() >= 625 and click.getX() <= 750 and click.getY() >= 125 and click.getY() <= 175:
            glob.new()
            newgame = True
            break
        else:
            #undraw current options
            func.undrawOptions(glob.graphplayerMoves)
            update()
            #creates selection highlights and shows move options
            i = 0
            while i < len(glob.graphRedPieces):
                piece = glob.graphRedPieces[i]
                #if option was selected don't go in
                if (click.getX()-piece.getCenter().getX())**2 + (click.getY()-piece.getCenter().getY())**2 <= piece.getRadius()**2 and option == False:                
                    #if no piece is selected, draw highlight
                    if glob.select == None:
                        highlight = Circle(piece.getCenter(), piece.getRadius())
                        func.selHighlight(highlight)    
                        glob.select = piece
                        glob.selrow,glob.selcol = func.findIndex(glob.select)
                    #if player clicked on the same piece, undraw current highlight
                    elif glob.select == piece:
                        highlight.undraw()
                        glob.select = None
                    #if a different piece was selected, undraw current highlight and draw new highlight
                    else:
                        highlight.undraw()
                        highlight = Circle(piece.getCenter(), piece.getRadius())
                        func.selHighlight(highlight)
                        glob.select = piece
                        glob.selrow,glob.selcol = func.findIndex(glob.select)
                    break
                #if a current piece was not clicked
                elif option == False:
                    if glob.select != None:
                        #check if the player clicked an option
                        for j in range(len(glob.graphplayerMoves)):
                            piece = glob.graphplayerMoves[j]
                            if (click.getX()-piece.getCenter().getX())**2 + (click.getY()-piece.getCenter().getY())**2 <= piece.getRadius()**2:
                                #move piece and removes pieces if necessary
                                func.movePiece(glob.selrow,glob.selcol, j, glob.select, glob.playerMoves)
                                func.removePiece(glob.select, glob.playerCaptures)
                                #check for promotion for red pieces
                                for z in range(len(glob.graphBoard[0])):
                                    if func.isRed(glob.graphBoard[0][z]) and not(func.isKing(glob.graphBoard[0][z], glob.playerKings)):
                                            glob.playerKings.append(glob.select)
                                #reset some stuff for next click
                                highlight.undraw()
                                glob.playerMoves = []
                                glob.graphplayerMoves = []
                                glob.select = None
                                option = True
                                update()
                                break
                #ai turn
                #########################################################################################################################################
                if option == True and len(glob.graphWhitePieces) > 0:
                    ai = True
                    #reset AI lists
                    glob.aiMoves = []
                    glob.aiCaptures = []
                    glob.aiBlanks = []
                    #generate all possible diagonal moves and jumps
                    for g in range (len(glob.graphWhitePieces)):
                        piece = glob.graphWhitePieces[g]
                        a, b = func.findIndex(piece)
                        tempBoard = [[b for b in a] for a in glob.mainBoard]
                        path = []
                        func.findJumps(glob.aiMoves, a, b, piece, glob.aiKings, tempBoard, glob.aiCaptures, path, a, b)
                        func.findBlankSpaces(glob.aiMoves, a, b, piece, glob.aiKings, ai)
                    #point system to determine the next move
                    points = 0
                    #index of aiMoves that will be the next move
                    movesIndex = 0
                    #the piece that will be moved
                    piece = None
                    #index of piece that will be moved
                    row = col = 0
                    #if there are jumps to check
                    if len(glob.aiCaptures) > 0:
                        for c in range (len(glob.aiCaptures)):
                            #check every possible jump path against each other and the one that adds up to the most points will be the next move
                            temprow = glob.aiCaptures[c][0][0]
                            tempcol = glob.aiCaptures[c][0][1]
                            temppiece = glob.graphBoard[temprow][tempcol]
                            temppoints = 1
                            for d in range(len(glob.aiCaptures[c])):
                                mover = glob.aiCaptures[c][d][0]
                                movec = glob.aiCaptures[c][d][1]
                                #incentivizing captures
                                if glob.mainBoard[mover][movec] == 3:
                                    temppoints += 10
                                #incentivizing kings
                                if mover == 7 and not(func.isKing(temppiece,glob.aiKings)):
                                    temppoints += 15
                                #incentivising moving further down the board
                                if mover > temprow and not(func.isKing(temppiece,glob.aiKings)):
                                    temppoints += 2
                                #deter moving back up the board if the piece is a king
                                if mover > temprow and func.isKing(temppiece,glob.aiKings):
                                    temppoints -= 2
                                #incentivise moving back down the board if the piece is a king
                                if mover < temprow and func.isKing(temppiece, glob.aiKings):
                                    temppoints += 1
                            if temppoints > points:
                                points = temppoints
                                piece = temppiece
                                row = temprow
                                col = tempcol
                                for e in range(len(glob.aiMoves)):
                                    if glob.aiMoves[e] == [mover,movec]:
                                        movesIndex = e
                                        break
                    #if there is no jumps or the jumps arent beneficial, pick a random move from the diagonal moves
                    #also if the proposed move is the same as the previous move then pick a new move
                    if points <= 1 or glob.aiLastMove == glob.aiMoves[movesIndex]:
                        randPiece = randint(0,len(glob.aiBlanks)-1)
                        randSpace = randint(1,len(glob.aiBlanks[randPiece])-1)
                        row = glob.aiBlanks[randPiece][0][0]
                        col = glob.aiBlanks[randPiece][0][1]
                        piece = glob.graphBoard[row][col]
                        mover = glob.aiBlanks[randPiece][randSpace][0]
                        movec = glob.aiBlanks[randPiece][randSpace][1]
                        for f in range(len(glob.aiMoves)):
                            if glob.aiMoves[f] == [mover,movec]:
                                movesIndex = f
                                break
                    time.sleep(1.5)
                    #moving piece and removing pieces as needed
                    piece = func.movePiece(row, col, movesIndex, piece, glob.aiMoves)
                    func.removePiece(piece, glob.aiCaptures)
                    #putting highlight to show which piece was moved
                    moved = Circle(piece.getCenter(), piece.getRadius())
                    moved.setOutline("blue")
                    moved.setWidth(5)
                    moved.draw(glob.win)
                    update()
                    time.sleep(1)
                    moved.undraw()
                    #check for white piece promotion
                    for g in range(len(glob.graphBoard[7])):
                        if func.isWhite(glob.graphBoard[7][g]) and not(func.isKing(glob.graphBoard[7][g],glob.aiKings)):
                            glob.aiKings.append(glob.graphBoard[7][g])
                    glob.aiLastMove = [row,col]
                    break    
                i += 1
            update()
            
            #shows player's moves based on selected piece
            ################################################################################################################################################################
            #if piece is selected
            if glob.select != None:
                #find possible moves
                glob.playerMoves = []
                tempBoard = [[col for col in row] for row in glob.mainBoard]
                path = []
                glob.playerCaptures = []
                func.findJumps(glob.playerMoves, glob.selrow, glob.selcol, glob.select, glob.playerKings, tempBoard, glob.playerCaptures, path, glob.selrow, glob.selcol)
                func.findBlankSpaces(glob.playerMoves,glob.selrow ,glob.selcol,glob.select,glob.playerKings, ai)
                #show possible moves
                glob.graphplayerMoves = func.showOptions(glob.playerMoves,glob.graphplayerMoves)

            #win/lose conditions
            ################################################################################################################################################################
            #if there are no white pieces left, red wins
            if len(glob.graphWhitePieces) == 0:
                glob.WorL = 1
            #if there are no red pieces left, white wins
            elif len(glob.graphRedPieces) == 0:
                glob.WorL = -1
            #if there is one red piece left, but no available moves, you lose
            elif len(glob.graphRedPieces) == 1 and len(glob.playerMoves) == 0 and glob.select != None:
                glob.WorL = -1
            #if there is at least 6 more red pieces than white pieces, white surrenders
            elif len(glob.graphRedPieces) - len(glob.graphWhitePieces) >= 6:
                glob.WorL = 1
                glob.aiSurrender = True
            update()
    
    func.reset()
    #if the player wants to play again but didn't press new game
    if playagain == True and newgame == False:
        func.gameover()
        update()
        #WorL = 1 is win for player WorL = -1 is win for AI
        #if player lost
        if glob.WorL == -1:
            #if ran out of moves
            if len(glob.graphRedPieces) == 1 and len(glob.playerMoves) == 0 and glob.select != None:
                text = Text(Point(400,300), "No moves left... You Lost...")
                text.setSize(25)
                text.setFace("courier")
                text.setStyle("italic")
                text.draw(glob.win)
            else:
                text = Text(Point(400,300), "You Lost...")
                text.setSize(25)
                text.setFace("courier")
                text.setStyle("italic")
                text.draw(glob.win)
        #if player won
        elif glob.WorL == 1:
            #if AI surrendered
            if glob.aiSurrender == True:
                text = Text(Point(400,300), "White Surrendered. You Won!")
                text.setSize(25)
                text.setFace("courier")
                text.setStyle("italic")
                text.draw(glob.win)
            else:
                text = Text(Point(410,300), "You Won!")
                text.setSize(25)
                text.setFace("courier")
                text.setStyle("italic")
                text.draw(glob.win)

        #check for button clicks
        while True:
            click = glob.win.getMouse()
            if click.getX() >= 200 and click.getX() <= 350 and click.getY() >= 400 and click.getY() <= 450:
                playagain = True
                break
            elif click.getX() >= 450 and click.getX() <= 600 and click.getY() >= 400 and click.getY() <= 450:
                playagain = False
                break
    func.reset()
#if player exits game
text = Text(Point(400,200), "Game Over!")
text.setSize(36)
text.setFace("courier")
text.setStyle("bold")
text.draw(glob.win)
text = Text(Point(400,300), "Thanks for playing!")
text.setSize(25)
text.setFace("courier")
text.setStyle("italic")
text.draw(glob.win)
update()
time.sleep(1)
glob.win.close()
    
                        
                            
                        
            


            
