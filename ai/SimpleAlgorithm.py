# Just checks if there is a move to win or block and, if not chooses an odd tile
import random


class SimpleAlgorithm:

    board = None
    piece = ''
    other = ''
    move = None

    def __init__(self, board, piece='O'):
        self.move = []

        self.assignBoard(board)

        self.piece = piece
        if piece == 'X':
            self.other = 'O'
        else:
            self.other = 'X'

    def assignBoard(self, board):
        self.board = board

    def printBoard(self):
        for l in self.board.getBoard():
            print(l)

    @staticmethod
    def getCoordinates(index):

        line = int(index / 3)
        col = int(index % 3)
        return [line, col]

    def getMove(self):

        if self.moveToWin():
            # print('win')
            return self.move
        if self.moveToBlock():
            # print('block')
            return self.move
        else:
            return self.randomMove()

    def moveToWin(self):

        board = self.board
        for i in range(3):
            for j in range(3):
                if not board.isOccupied(i, j):
                    board.play(i, j, self.piece)
                    if board.checkVictory(self.piece):
                        self.move = [i, j]
                        board.eraseMove(i, j)
                        return True
                    else:
                        board.eraseMove(i, j)

        return False

    def moveToBlock(self):

        board = self.board
        for i in range(3):
            for j in range(3):
                if not board.isOccupied(i, j):
                    board.play(i, j, self.other)
                    if board.checkVictory(self.other):
                        self.move = [i, j]
                        board.eraseMove(i, j)
                        return True
                    else:
                        board.eraseMove(i, j)

        return False

    def randomMove(self):

        board = self.board

        if not board.isOccupied(1, 1):  # if the middle tile is free
            return [1, 1]

        options = []
        goodOptions = []

        for i in range(9):
            line = self.getCoordinates(i)[0]
            col = self.getCoordinates(i)[1]
            if not board.isOccupied(line, col):  # if the tile is free
                board.play(line, col, self.piece)
                if not self.enablesTwoOptions(board, self.other):  # if it's not a bad move
                    options.append([line, col])
                board.eraseMove(line, col)

        for coord in options:
            line = coord[0]
            col = coord[1]
            board.play(line, col, self.piece)
            if self.enablesTwoOptions(board, self.piece):  # if it's a good move
                goodOptions.append([line, col])
            board.eraseMove(line, col)

        if len(goodOptions) > 0:
            return random.choice(goodOptions)

        return random.choice(options)




    def enablesTwoOptions(self, board, piece):  # to see if a move will enable two options

        if piece == 'X':
            other = 'O'
        else:
            other = 'X'

        for i in range(3):
            for j in range(3):
                if not board.isOccupied(i, j):
                    board.play(i, j, piece)
                    if self.twoWinningOptions(board, piece) and \
                            not self.isThereWinningMove(board, other):
                        board.eraseMove(i, j)
                        return True
                    board.eraseMove(i, j)

        return False

    @staticmethod
    def twoWinningOptions(board, piece):  # to see if there are two winning moves for a player

        winningMoves = 0

        for i in range(3):  # counts the number of winning moves
            for j in range(3):
                if not board.isOccupied(i, j):
                    board.play(i, j, piece)
                    if board.checkVictory(piece):
                        winningMoves += 1
                    board.eraseMove(i, j)

        if winningMoves > 1:
            return True

        return False

    @staticmethod
    def isThereWinningMove(board, piece):

        for i in range(3):
            for j in range(3):
                if not board.isOccupied(i, j):
                    board.play(i, j, piece)
                    if board.checkVictory(piece):
                        board.eraseMove(i, j)
                        return True
                    board.eraseMove(i, j)

        return False
