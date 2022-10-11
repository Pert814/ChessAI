from inspect import BoundArguments
from shutil import move
from tkinter.tix import Tree
from xml.dom.pulldom import START_ELEMENT
from matplotlib.cbook import delete_masked_points
from numpy import true_divide
#from symbol import pass_stmt


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
        self.enpassantPossible = ()
        self.curentCastleRight = CastleRights(True,True,True,True)
        self.CastleRightsLog = [CastleRights(self.curentCastleRight.wKs,self.curentCastleRight.bKs,
                                self.curentCastleRight.wQs,self.curentCastleRight.bQs)]

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow,move.endCol)
        #PawnPromotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        #PawnEnpassant
        if move.isEnpassantMoves:
            self.board[move.startRow][move.endCol] = '--'
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2 , move.startCol)
        else:
            self.enpassantPossible = ()
        #castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'
        #CastlingRight Update and log
        self.updateCastleRights(move)
        self.CastleRightsLog.append(CastleRights(self.curentCastleRight.wKs,self.curentCastleRight.bKs,
                                    self.curentCastleRight.wQs,self.curentCastleRight.bQs))

    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
        #update King's pos. if needed
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.startRow,move.startCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.startRow,move.startCol)
        # undo enpassant
        if move.isEnpassantMoves:
            self.board[move.endRow][move.endCol] = '--'
            self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantPossible = (move.endRow, move.endCol)
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ()
        #undo castling rights
        self.CastleRightsLog.pop()
        self.curentCastleRight.bKs = self.CastleRightsLog[-1].bKs
        self.curentCastleRight.wKs = self.CastleRightsLog[-1].wKs
        self.curentCastleRight.bQs = self.CastleRightsLog[-1].bQs
        self.curentCastleRight.wQs = self.CastleRightsLog[-1].wQs
        
        #undo castling move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                self.board[move.endRow][move.endCol - 1] = '--'
            else:
                self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'

    def updateCastleRights(self,move):
        if move.pieceMoved == 'wK':
            self.curentCastleRight.wKs = False
            self.curentCastleRight.wQs = False
        elif move.pieceMoved == 'bK':
            self.curentCastleRight.bKs = False
            self.curentCastleRight.bQs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.curentCastleRight.wQs = False
                elif move.startCol == 7:
                    self.curentCastleRight.wKs = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.curentCastleRight.bQs = False
                elif move.startCol == 7:
                    self.curentCastleRight.bKs = False

    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRight = CastleRights(self.curentCastleRight.wKs , self.curentCastleRight.bKs ,
                                        self.curentCastleRight.wQs , self.curentCastleRight.bQs)
        moves = self.getAllPossibleMove()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0] , self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0] , self.blackKingLocation[1], moves)
        for i in range(len(moves)-1 , -1 , -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        self.enpassantPossible = tempEnpassantPossible
        self.curentCastleRight = tempCastleRight
        return moves

    def inCheck(self):
        if self.whiteToMove:
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
                elif (r-1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c-1),self.board, isEnpassantMoves = True))
            if c < 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c+1),self.board, isEnpassantMoves = True))
        else:
            if self.board[r+1][c] == '--':
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c > 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c-1),self.board, isEnpassantMoves = True))
            if c < 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif (r+1,c+1) == self.enpassantPossible:
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
    
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r , c):
            return
        if (self.whiteToMove and self.curentCastleRight.wKs) or (not self.whiteToMove and self.curentCastleRight.bKs ):
            if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
                if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                    moves.append(Move((r, c) , (r, c+2) , self.board , isCastleMove = True))
        elif (self.whiteToMove and self.curentCastleRight.wQs) or (not self.whiteToMove and self.curentCastleRight.bQs ):
            if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
                if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                    moves.append(Move((r, c) , (r, c-2) , self.board , isCastleMove = True))


class CastleRights():
    def __init__(self, wKs ,bKs ,wQs , bQs):
        self.wKs = wKs
        self.bKs = bKs
        self.wQs = wQs
        self.bQs = bQs

class Move():
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    fileToCols = {"a":0,"b":1,"c":2,"d":3,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k,v in fileToCols.items()}

    def __init__(self , startsq , endsq , board , isEnpassantMoves = False , isCastleMove = False):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) \
            or (self.pieceMoved == 'bp' and self.endRow == 7)
        #enpassant
        self.isEnpassantMoves = isEnpassantMoves
        if self.isEnpassantMoves:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        #castle 
        self.isCastleMove = isCastleMove

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


        


