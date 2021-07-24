from boards import TicTacToe as SB
from data_structures import Node


class Tree:

    root = None
    board = None

    def __init__(self):
        self.root = Node.Node()
        self.makeChildren(self.root)

    @staticmethod
    def getCoordinates(i):
        line = i / 3
        col = i % 3
        return [line, col]

    @staticmethod
    def makeChildren(node):

        for i in range(9):
            return 0






