# Just checks if there is a move to win or block and, if not chooses an odd tile
from ai import Algorithms as Alg
import random


class SimpleAlgorithm(Alg.Algorithms):

    def getMove(self):

        if self.moveToWin():
            # print('win')
            return self.move
        if self.moveToBlock():
            # print('block')
            return self.move
        else:
            return self.randomMove()

    def randomMove(self):

        board = self.board

        if not board.isOccupied(1, 1):  # if the middle tile is free
            return [1, 1]

        options = self.blockTheFuture(board)  # options that aren't bad

        return self.goodOptions(options, board)

    def goodOptions(self, options, board):  # if it's possible to do a good move

        corners = []  # corners are usually nice
        goodOptions = []  # those that will make you win

        for coord in options:
            if coord in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                corners.append(coord)

        for coord in options:
            line = coord[0]
            col = coord[1]
            if not board.isOccupied(line, col):
                board.play(line, col, self.piece)
                if self.twoWinningOptions(board, self.piece):
                    goodOptions.append(coord)
                board.eraseMove(line, col)

        if len(goodOptions) > 0:
            return random.choice(goodOptions)
        if len(corners) > 0:
            return random.choice(corners)
        return random.choice(options)

    def blockTheFuture(self, board):  # Choose the options that will not lead to death by stupid

        options = []

        for i in range(9):
            line = self.getCoordinates(i)[0]
            col = self.getCoordinates(i)[1]
            if not board.isOccupied(line, col):  # if the tile is free
                board.play(line, col, self.piece)
                if not self.enablesTwoOptions(board, self.other):  # if it's not a bad move
                    options.append([line, col])
                board.eraseMove(line, col)

        return options
