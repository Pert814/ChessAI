from inspect import BoundArguments
from shutil import move
from tkinter.tix import Tree
from xml.dom.pulldom import START_ELEMENT

from numpy import true_divide


class GameState():

    def __init__(self):
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],  
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ['--','--','--','--','--','--','--','--',],
            ['--','--','--','--','--','--','--','--',],
            ['--','--','--','--','--','--','--','--',],
            ['--','--','--','--','--','--','--','--',],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']]
        self.moveFunctions = {'p':self.getPawnMoves,
        'R':self.getRockMoves,'N':self.getKnightMoves,'B':self.getBishopMoves,
        'Q':self.getQueenMoves,'K':self.getKingMoves}
        self.whiteToMove = True
        self.movelog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False
        self.empassantPossible = ()
        # self.inCheck = False
        # self.pin = []
        # self.checks = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow,move.endCol)
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        if move.isEnpassantMoves:
            print('here')
            self.board[move.startRow][move.endCol] == '--'
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.empassantPossible = ((move.startRow + move.endRow)//2 , move.startCol)
        else:
            self.empassantPossible = ()

    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.startRow,move.startCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.startRow,move.startCol)
        if move.isEnpassantMoves:
            self.board[move.endRow][move.endCol] = '--'
            self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.empassantPossible = (move.endRow, move.endCol)
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.empassantPossible = ()

    def getValidMoves(self):
        tempEnpassantPossible = self.empassantPossible
        moves = self.getAllPossibleMove()
        for i in range(len(moves)-1 , -1 , -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            #print(self.inCheck())
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        self.empassantPossible = tempEnpassantPossible
        return moves

    def inCheck(self):
        if self.whiteToMove:
            #print(self.whiteKingLocation)
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else: 
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])
            
    def squareUnderAttack(self,r,c): 
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMove()
        self.whiteToMove = not self.whiteToMove
        for moves in oppMoves:
            if moves.endRow == r and moves.endCol == c:
                return True
        return False   

    def getAllPossibleMove(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r,c,moves)
                    elif piece == 'R':
                        self.getRockMoves(r,c,moves)
                    elif piece == 'B':
                        self.getBishopMoves(r,c,moves)
                    elif piece == 'N':
                        self.getKnightMoves(r,c,moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r,c,moves)
                    elif piece == 'K':
                        self.getKingMoves(r,c,moves)
                    
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == '--':
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c > 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1) == self.empassantPossible:
                    moves.append(Move((r,c),(r-1,c-1),self.board, isEnpassantMoves = True))
            if c < 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1) == self.empassantPossible:
                    moves.append(Move((r,c),(r-1,c+1),self.board, isEnpassantMoves = True))
        else:
            if self.board[r+1][c] == '--':
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c > 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1) == self.empassantPossible:
                    moves.append(Move((r,c),(r+1,c-1),self.board, isEnpassantMoves = True))
            if c < 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif (r+1,c+1) == self.empassantPossible:
                    moves.append(Move((r,c),(r+1,c+1),self.board, isEnpassantMoves = True))

    def getRockMoves(self, r, c, moves):
        rockDirections = ((1,0),(-1,0),(0,1),(0,-1))
        for d in rockDirections:
            for i in range(1,7):
                if 0 <= r + d[0] * i <= 7 and 0 <= c + d[1] * i <= 7:
                    endpiece = self.board[r + d[0] * i][c + d[1] * i]
                    if endpiece == '--':
                        moves.append(Move((r,c),(r + d[0] * i,c + d[1] * i),self.board))
                    elif endpiece[0] == 'b' and self.whiteToMove:
                        moves.append(Move((r,c),(r + d[0] * i,c + d[1] * i),self.board))
                        break
                    elif endpiece[0] == 'w' and not self.whiteToMove:
                        moves.append(Move((r,c),(r + d[0] * i,c + d[1] * i),self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knightDirections = ((2,1),(1,2),(-2,1),(-1,2),(2,-1),(1,-2),(-2,-1),(-1,-2))
        for d in knightDirections:
            if 0 <= r + d[0] <= 7 and 0 <= c + d[1] <= 7:
                endpiece = self.board[r + d[0]][c + d[1]]
                if endpiece == '--':
                    moves.append(Move((r,c),(r + d[0],c + d[1]),self.board))
                elif endpiece[0] == 'b' and self.whiteToMove:
                    moves.append(Move((r,c),(r + d[0],c + d[1]),self.board))
                elif endpiece[0] == 'w' and not self.whiteToMove:
                    moves.append(Move((r,c),(r + d[0],c + d[1]),self.board))
                else:
                    continue
            else:
                continue

    def getBishopMoves(self, r, c, moves):
        bishopDirections = ((1,1),(-1,1),(1,-1),(-1,-1))
        for d in bishopDirections:
            for i in range(1,7):
                if 0 <= r + d[0] * i <= 7 and 0 <= c + d[1] * i <= 7:
                    endpiece = self.board[r + d[0] * i][c + d[1] * i]
                    if endpiece == '--':
                        moves.append(Move((r,c),(r + d[0] * i,c + d[1] * i),self.board))
                    elif endpiece[0] == 'b' and self.whiteToMove:
                        moves.append(Move((r,c),(r + d[0] * i,c + d[1] * i),self.board))
                        break
                    elif endpiece[0] == 'w' and not self.whiteToMove:
                        moves.append(Move((r,c),(r + d[0] * i,c + d[1] * i),self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRockMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
                
    def getKingMoves(self, r, c, moves):
        for rDir in (-1,0,1):
            for yDir in (-1,0,1):
                if 0 <= r + rDir <= 7 and 0 <= c + yDir <= 7:
                    endpiece = self.board[r + rDir][c + yDir]
                    if endpiece == '--':
                        moves.append(Move((r,c),(r + rDir,c + yDir),self.board))
                    elif endpiece[0] == 'b' and self.whiteToMove:
                        moves.append(Move((r,c),(r + rDir,c + yDir),self.board))
                    elif endpiece[0] == 'w' and not self.whiteToMove:
                        moves.append(Move((r,c),(r + rDir,c + yDir),self.board))
                    else:
                        continue
                else:
                    continue


        pass


class Move():
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    fileToCols = {"a":0,"b":1,"c":2,"d":3,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k,v in fileToCols.items()}

    def __init__(self,startsq,endsq,board,isEnpassantMoves = False):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) \
            or (self.pieceMoved == 'bp' and self.endRow == 7)
        self.isEnpassantMoves = isEnpassantMoves
        if self.isEnpassantMoves:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):#https://www.pythontutorial.net/python-oop/python-__eq__/
        #用來使兩種不同instances of "Ｍove"卻有相同"moveID"視為相同
        if isinstance(other, Move): #https://www.runoob.com/python/python-func-isinstance.html
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


        


