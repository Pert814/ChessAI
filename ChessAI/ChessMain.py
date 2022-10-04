from tkinter import Image
from turtle import Screen
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
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []

    while running:

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
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
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # press z button on keyboard
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPiece(screen,gs.board)

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


if __name__ == '__main__':
    main()

