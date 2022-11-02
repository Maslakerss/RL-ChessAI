from data.chessIndexes import POSITIONINDEXES, NOTATIONINDEXES
import cv2
import numpy as np
import os

ROWS = 8
COLUMNS = 8


class Board:
    def __init__(self, boardPosition=""):
        super(Board, self).__init__()

        #normalPos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

        if not boardPosition:
            boardPosition = "rnbqr3/pppp1p1p/1b3n1k/3P2K1/8/2NB1N2/PPPB2pP/R2Q1R2"


        self.board = np.zeros((8, 8),  dtype=np.str_)
        self.futureBoard = self.board

        self.position = boardPosition
        self.currentMove = "W"
        self.legalMoves = list()


        self.board_setup(self.position)
        #self.begin()
        

    def board_setup(self, setup):
        setupBoard = self.board
        setupBoard = setupBoard.reshape(64)

        iteration = 0
        for piece in setup:
            if piece == "/":
                continue

            elif piece.isdigit():
                for i in range(int(piece)):
                    setupBoard[iteration] = '.'

                    iteration += 1

            
            else:
                setupBoard[iteration] = piece
                iteration += 1

        
        setupBoard = setupBoard.reshape((8, 8))
        self.board = setupBoard
        print(self.board)


    def begin(self):
        while not self.is_checkmate() and not self.is_stalemate():
            self.step()

    

    def step(self):
        move = input(f"make move {POSITIONINDEXES[self.currentMove]}: \n")
        
        self.make_move(move)
        print(self.board)




    def make_move(self, move):
        if len(move) != 4:
            print("that move is invalid")
            self.step()
        
        if not move[0] in POSITIONINDEXES or not move[2] in POSITIONINDEXES:
            print("that move is invalid")
            self.step()


        #originalPosition and targetPosition
        oPos = [8 - int(move[1]), POSITIONINDEXES[move[0].lower()]]
        tPos = [8 - int(move[3]), POSITIONINDEXES[move[2].lower()]]


        piece = self.board[oPos[0], oPos[1]]
        

        if (self.currentMove == "W" and piece.islower()) or (self.currentMove == "C" and not piece.islower()):
            print("that move is invalid")
            self.step()


        possibleMoves = self.get_moves(piece, oPos)

        print(possibleMoves)
        print(tPos)

        if tPos in possibleMoves:
            self.currentMove = NOTATIONINDEXES[self.currentMove]

            tempBoard = self.board
            tempBoard[oPos[0], oPos[1]], tempBoard[tPos[0], tPos[1]] = '.', tempBoard[oPos[0], oPos[1]]


            self.board = tempBoard
        


    
    def get_moves(self, piece, position):
        holdPiece = piece

        moves = {
            "p": self.pawn_moves,
            "r": self.rook_moves,
            "q": self.queen_moves,
            "b": self.bishop_moves,
            "n": self.knight_moves,
            "k": self.king_moves
        }
        
        return moves[holdPiece.lower()](piece, position)
        


    def get_all_moves(self):
        print("For now")



    def is_check(self):
        allPieces = ["n", "p", "k", "r", "b", "q"]
        enemyPieces = ["N", "P", "K", "R", "B", "Q"] 
        kingPos = self.get_king_pos()

        if self.currentMove == "W":
            for x in range(len(allPieces)):
                allPieces[x], enemyPieces[x] = enemyPieces[x], allPieces[x]


        knightMoves = self.knight_moves(allPieces[0], kingPos)
        pawnMoves = self.pawn_moves(allPieces[1], kingPos, king_check=True)
        kingMoves = self.king_moves(allPieces[2], kingPos)
        rookMoves = self.rook_moves(allPieces[3], kingPos)
        bishopMoves = self.bishop_moves(allPieces[4], kingPos)

        
        for move in knightMoves:
            piece = self.board[move[0], move[1]]

            if piece == enemyPieces[0]:
                return True


        for move in pawnMoves:
            piece = self.board[move[0], move[1]]

            if piece == enemyPieces[1]:
                return True


        for move in kingMoves:
            piece = self.board[move[0], move[1]]

            if piece == enemyPieces[2]:
                return True

        
        for move in rookMoves:
            piece = self.board[move[0], move[1]]

            if piece == enemyPieces[5] or piece == enemyPieces[3]:
                return True


        for move in bishopMoves:
            piece = self.board[move[0], move[1]]

            if piece == enemyPieces[5] or piece == enemyPieces[4]:
                return True

        
        return False



    def is_checkmate(self):
        return False


    def is_stalemate(self):
        return False




    def get_king_pos(self):
        tempBoard = self.board

        king = 'k'

        if self.currentMove == "W":
            king = king.upper()

        for y, row in enumerate(tempBoard):
            for x, tile in enumerate(row):
                if tile == king:
                    return [y, x]



    def pawn_moves(self, pawn, position, king_check=False):
        positionY = position[0]
        direction = 1
        pawnVectors = [[1, 1], [1, -1], [1,0], [2, 0]]
        moves = list()
        
        if pawn == "P":
            direction = -1

            if positionY != 6:
                pawnVectors.pop()

        elif positionY !=1:
            pawnVectors.pop()

        
        for i in range(len(pawnVectors)):
            pawnVectors[i] = [item * direction for item in pawnVectors[i]]



        for index, vector in enumerate(pawnVectors):
            pos = [vector[0] + position[0], vector[1] + position[1]]

            if not (pos[0] >=0 and pos[0] < 8) or not (pos[1] >=0 and pos[1] < 8):
                continue


            moves.append(pos)
            piece = piece = self.board[pos[0], pos[1]] 


            if index < 2:
                if not (piece == '.'):
                    if (piece.isupper() and pawn.isupper()) or (piece.islower() and pawn.islower()):
                        moves.pop()

                else:
                    moves.pop()

            else:
                if self.board[pos[0], pos[1]] != '.' or king_check:
                    moves.pop()
                    
                    break

        
        return moves


    def rook_moves(self, rook, position):
        positionY = position[0]
        positionX = position[1]

        moves = list()

        for Y in range(positionY, 8):
            if Y != positionY:
                moves.append([Y, positionX])
                piece = self.board[Y, positionX]

                if piece != '.':
                    if (piece.isupper() and rook.isupper()) or (piece.islower() and rook.islower()):
                        moves.pop()

                    break

        for Y in range(positionY, -1, -1):
            if Y != positionY:
                moves.append([Y, positionX])
                piece = self.board[Y, positionX]

                if piece != '.':
                    if (piece.isupper() and rook.isupper()) or (piece.islower() and rook.islower()):
                        moves.pop()

                    break

        

        for X in range(positionX, 8):
            if X != positionX:
                moves.append([positionY, X])
                piece = self.board[positionY, X]

                if piece != '.':
                    if (piece.isupper() and rook.isupper()) or (piece.islower() and rook.islower()):
                        moves.pop()

                    break
        
        for X in range(positionX, -1, -1):
            if X != positionX:
                moves.append([positionY, X])
                piece = self.board[positionY, X]

                if piece != '.':
                    if (piece.isupper() and rook.isupper()) or (piece.islower() and rook.islower()):
                        moves.pop()

                    break



        return moves


    def knight_moves(self, knight, position):
        moves = list()
        moveVectors = [[2, 1], [2, -1], [-2, 1], [-2, -1], [-1, -2], [1, -2], [-1, 2], [1, 2]]

        for vector in moveVectors:
            pos = [position[0] + vector[0], position[1] + vector[1]]

            if not (pos[0] >= 0 and pos[0] < 8) or not(pos[1] >=0 and pos[1] < 8):
                continue

            piece = self.board[pos[0], pos[1]]

            if piece != '.':
                if piece.isupper() and knight.isupper() or piece.islower() and knight.islower():
                    continue
            
            
            moves.append(pos)

        
        return moves


    
    def bishop_moves(self, bishop, position):
        moves = list()
        directions = [[1, 1], [-1, -1], [1, -1], [-1, 1]]


        for direction in directions:
            newPos = [position[0], position[1]]

            while newPos[0] <= 7 and newPos[0] >= 0 and newPos[1] <= 7 and newPos[1] >= 0:
                if newPos[0] == (3.5 + (3.5 * direction[0])) or newPos[1] == (3.5 + (3.5 * direction[1])):
                    break


                newPos[0] += direction[0]
                newPos[1] += direction[1]

                
                moves.append(newPos)
                piece = self.board[newPos[0], newPos[1]]

                if piece != '.':
                    if (piece.isupper() and bishop.isupper()) or (piece.islower() and bishop.islower()):
                        moves.pop()

                    break

        
        
        return moves


    def queen_moves(self, queen, position):
        rook = 'r'
        bishop = 'b'

        moves = list()

        if queen == 'Q':
            rook = rook.upper()
            bishop = bishop.upper()


        rookPositions = self.rook_moves(rook, position)
        bishopPosition = self.bishop_moves(bishop, position)

        moves = rookPositions

        for bPosition in bishopPosition:
            moves.append(bPosition)


        return moves


    def king_moves(self, king, position):
        positionY = position[0]
        positionX = position[1]

        moves = list()


        for y in range(1, 4):
            for x in range(1, 4):
                pos = [(y -2) + positionY, (x -2) + positionX]

                if not (pos[0] >= 0 and pos[0] < 8) or not (pos[1] >= 0 and pos[1] < 8):
                    continue
                
                if pos == position:
                    continue


                moves.append(pos)
                piece = self.board[pos[0], pos[1]]


                if piece != '.':
                    if piece.isupper() and king.isupper() or piece.islower() and king.islower():
                        moves.pop()


        return moves




board = Board()

#print(board.pawn_moves("P", [6, 0]))
#print(board.rook_moves("r", [5, 5]))
#print(board.bishop_moves("b", [5,5]))
#print(board.queen_moves("Q", [5,5]))
#print(board.king_moves("K", [4, 1]))

#print(board.get_king_pos())
print(board.is_check())

print("__________________________________")
newBoard = np.zeros((64), dtype=np.str_)
moves = board.knight_moves("N", [5,3])


for x in range(len(newBoard)):
    newBoard[x] = '.'

newBoard = newBoard.reshape((8, 8))

for move in moves:
    newBoard[move[0], move[1]] = '#' 


print(newBoard)