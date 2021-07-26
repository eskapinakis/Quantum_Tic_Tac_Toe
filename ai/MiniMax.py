from data_structures import *


class Minimax:

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



