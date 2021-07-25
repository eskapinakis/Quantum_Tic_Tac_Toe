from boards import TicTacToe as SB
from data_structures import Node


class Tree:

    root = None
    board = None
    player = 'X'

    def __init__(self):
        self.root = Node.Node()
        self.makeChildren(self.root)

    def changePLayer(self):
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'

    @staticmethod
    def getCoordinates(i):
        line = i / 3
        col = i % 3
        return [line, col]

    def makeChildren(self, node):

        for i in range(9):

            child = Node.Node(node)
            child.copyBoard()
            child.play(self.getCoordinates(i), self.player)
            self.ChangePlayer()
            node.addChildren(child)
            if not node.isWinning():
                self.makeChildren(child)






