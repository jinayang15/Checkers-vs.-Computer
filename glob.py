from graphics import *

def init():
    global win
    win = GraphWin("Checkers", 800, 600, autoflush = False)
    win.setBackground("white")
    
    global mainBoard, graphBoard, graphRedPieces, graphWhitePieces, playerMoves, graphplayerMoves, aiMoves, playerKings, playerCaptures, aiKings, aiCaptures, aiBlanks
    mainBoard, graphBoard, graphRedPieces, graphWhitePieces, playerMoves, graphplayerMoves, aiMoves, playerKings, playerCaptures, aiKings, aiCaptures, aiBlanks = ([] for i in range(12))
    mainBoard = [[] for i in range(8)]
    graphBoard = [[] for i in range(8)]

    global WorL
    WorL = 0

    global select
    select = None
    
    global selrow, selcol
    selrow = None
    selcol = None

    global aiLastMove
    aiLastMove = []
    global aiSurrender
    aiSurrender = False
    

def new():
    global mainBoard, graphBoard, graphRedPieces, graphWhitePieces, playerMoves, graphplayerMoves, aiMoves, playerKings, playerCaptures, aiKings, aiCaptures, aiBlanks
    mainBoard, graphBoard, graphRedPieces, graphWhitePieces, playerMoves, graphplayerMoves, aiMoves, playerKings, playerCaptures, aiKings, aiCaptures, aiBlanks = ([] for i in range(12))
    mainBoard = [[] for i in range(8)]
    graphBoard = [[] for i in range(8)]

    global WorL
    WorL = 0

    global select
    select = None
    
    global selrow, selcol
    selrow = None
    selcol = None

    global aiLastMove
    aiLastMove = []
    global aiSurrender
    aiSurrender = False

    
    
