from data.chessIndexes import POSITIONINDEXES, NOTATIONINDEXES
import cv2
import numpy as np
import os

ROWS = 8
COLUMNS = 8


class Board:
    def __init__(self, boardPosition=""):
        super(Board, self).__init__()

        if not boardPosition:
            boardPosition = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


        self.board = np.zeros((8, 8),  dtype=np.str_)
        self.position = boardPosition
        self.currentMove = "W"
        self.legalMoves = list()


        self.board_setup(boardPosition)
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



    def make_move(self, move):
        if len(move) != 4:
            print("that move is invalid")
            self.step()
        
        if not move[0] in POSITIONINDEXES or not move[2] in POSITIONINDEXES:
            print("that move is invalid")
            self.step()



        originalPosition = [8 - int(move[1]), POSITIONINDEXES[move[0].lower()]]
        targetPosition = [8 - int(move[3]), POSITIONINDEXES[move[2].lower()]]


        piece = self.board[originalPosition[0], originalPosition[1]]
        

        if (self.currentMove == "W" and piece.islower()) or (self.currentMove == "C" and not piece.islower()):
            print("that move is invalid")
            self.step()


        possibleMoves = self.get_moves(piece, originalPosition)

        print(possibleMoves)
        print(targetPosition)

        if targetPosition in possibleMoves:
            self.currentMove = NOTATIONINDEXES[self.currentMove]
        

    
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
        


    def is_checkmate(self):
        return False
    
    def is_stalemate(self):
        return False




    def pawn_moves(self, pawn, position):
        positionY = position[0]
        positionX = position[1]
        direction = 1
        pawnRange = 2
        moves = list()
        
        if pawn == "P":
            direction = -1

            if positionY != 6:
                pawnRange = 1

        elif positionY !=1:
            pawnRange = 1

        
        for y in range(1, pawnRange + 1):
            moves.append([positionY + y * direction, positionX])

            if self.board[moves[y][0] , moves[y][1]] != '.':
                break

        
        return moves


    def rook_moves(self, rook, position):
        positionY = position[0]
        positionX = position[1]

        moves = list()

        for Y in range(positionY, 8):
            if Y != positionY:
                moves.append([Y, positionX])

                if self.board[Y, positionX] != '.':
                    break

        for Y in range(positionY, -1, -1):
            if Y != positionY:
                moves.append([Y, positionX])

                if self.board[Y, positionX] != '.':
                    break

        

        for X in range(positionX, 8):
            if X != positionX:
                moves.append([positionY, X])

                if self.board[positionY, X] != '.':
                    break
        
        for X in range(positionX, -1, -1):
            if X != positionX:
                moves.append([positionY, X])

                if self.board[positionY, X] != '.':
                    break



        return moves


    def knight_moves(self, knight, position):
        print("no")

    
    def bishop_moves(self, bishop, position):
        positionY = position[0]
        positionX = position[1]

        moves = list()
        directions = [[1, 1], [-1, -1], [1, -1], [-1, 1]]

        for direction in directions:
            newPos = [position[0], position[1]]

            while newPos[0] <= 7 and newPos[0] >= 0 and newPos[1] <= 7 and newPos[1] >= 0:
                if newPos[0] == (3.5 + (3.5 * direction[0])) or newPos[1] == (3.5 + (3.5 * direction[1])):
                    break


                newPos[0] += direction[0]
                newPos[1] += direction[1]

                
                moves.append([newPos[0], newPos[1]])

                if self.board[newPos[0], newPos[1]] != '.':
                    break

        
        
        return moves


    def queen_moves(self, queen, position):
        rook = 'r'
        bishop = 'b'

        moves = list()

        if queen == 'Q':
            rook.capitalize()
            bishop.capitalize()

        rookPositions = self.rook_moves(rook, position)
        bishopPosition = self.bishop_moves(bishop, position)

        moves = rookPositions

        for bPosition in bishopPosition:
            moves.append(bPosition)


        return moves


    def king_moves(self, king, position):
        print("nope")



board = Board()

#print(board.pawn_moves("P", [1, 3]))
print(board.rook_moves("r", [5, 5]))
print(board.bishop_moves("b", [5,5]))
#print(board.queen_moves("q", [5,5]))