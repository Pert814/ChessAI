from inspect import BoundArguments


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

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMove()

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
            if c < 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        else:
            if self.board[r+1][c] == '--':
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c > 0 and self.board[r+1][c-1][0] == 'w':
                moves.append(Move((r,c),(r+1,c-1),self.board))

            if c < 7 and self.board[r+1][c+1][0] == 'w':
                moves.append(Move((r,c),(r+1,c+1),self.board))

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
        queenDirections = ((1,1),(-1,1),(1,-1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1))
        for d in queenDirections:
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

    def __init__(self,startsq,endsq,board):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
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


        


