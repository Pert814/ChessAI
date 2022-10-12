from tkinter import Image
from turtle import Screen, color
from matplotlib import colors
import pygame as p 

import ChessEngine 

p.init()
WIDTH = HEIGHT = 512
DIMENSIOM = 8
SQ_SIZE = HEIGHT // DIMENSIOM # there are two types of division operators: / : Divides the number on its left by the number on its right and returns a floating point value. // : Divides the number on its left by the number on its right, rounds down the answer, and returns a whole number.
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wR','wN','wB','wQ','wK','wB','wN','wR','bR','bN','bB','bQ','bK','bB','bN','bR','bp','wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('ChessAI/images/' + piece + '.png'),(SQ_SIZE,SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameover = False        

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameover:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row,col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True  
                                #print('moveMade = True')
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
                            
                        print(move.getChessNotation())
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # press z button on keyboard
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: # press r but. to reset
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    moveMade = False
                    animate = False
                    sqSelected = ()
                    playerClicks = []
        if moveMade:
            if animate:
                animatedMove(gs.movelog[-1] , screen , gs.board , clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        drawGameState(screen, gs , validMoves , sqSelected)
        if gs.checkMate:
            gameover = True
            if gs.whiteToMove:
                drawText(screen,'Black win by checkmate!')
            else:
                drawText(screen,'White win by checkmate!')
        elif gs.staleMate:
            gameover = True
            drawText(screen,'stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs , validMoves , squareSelected):
    drawBoard(screen)
    drawPiece(screen,gs.board)
    hightsquares(screen , gs , validMoves , squareSelected)

def drawBoard(screen):
    for row in range(DIMENSIOM):
        for col in range(DIMENSIOM):
            if (row + col)%2 == 0:
                p.draw.rect(screen,p.Color('white'),p.Rect(col * SQ_SIZE,row * SQ_SIZE,SQ_SIZE,SQ_SIZE ))
            else:
                p.draw.rect(screen,p.Color('gray'),p.Rect(col * SQ_SIZE,row * SQ_SIZE,SQ_SIZE,SQ_SIZE ))

def drawPiece( screen, board):
    for row in range(DIMENSIOM):
        for col in range(DIMENSIOM):
            piece = board[row][col]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE,row * SQ_SIZE,SQ_SIZE,SQ_SIZE ))  

def hightsquares(screen , gs , validMoves , squareSelected):
    if squareSelected != ():
        r , c = squareSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100) #transperacy value 0~255
            s.fill(p.Color('red'))
            screen.blit(s,(c * SQ_SIZE,r * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for moves in validMoves:
                if moves.startRow == r and moves.startCol == c:
                    screen.blit(s,(moves.endCol * SQ_SIZE , moves.endRow * SQ_SIZE))
 
def animatedMove(move , screen , board , clock):
    global colors
    colors = [p.Color('white') , p.Color('gray')]
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framePerSquare
    for frame in range(frameCount + 1):
        r , c = (move.startRow + dR * frame / frameCount , 
                        move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPiece(screen , board)
        color = colors[(move.endRow + move.endCol) % 2]
        endsquare = p.Rect(move.endCol * SQ_SIZE , move.endRow * SQ_SIZE , SQ_SIZE , SQ_SIZE)
        p.draw.rect(screen , color , endsquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured] , endsquare)
        screen.blit(IMAGES[move.pieceMoved] , p.Rect(c * SQ_SIZE , r * SQ_SIZE , SQ_SIZE , SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen , text):
    font = p.font.SysFont('Helvitca' , 32 , True , False)
    textObject = font.render(text , 0 ,p.Color('Black'))
    textLocation = p.Rect(0 , 0 , WIDTH , HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2 ,
                                                         HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject , textLocation)
    textObject = font.render(text , 0 ,p.Color('Gray'))
    screen.blit(textObject , textLocation.move(2 , 2))

    
if __name__ == '__main__':
    main()

