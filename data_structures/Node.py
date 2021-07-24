from boards import TicTacToe as SB


class Node:

    father = None
    board = None
    children = []

    def __init__(self, node=None):
        self.father = node
        self.board = SB.SmallBoard()

    def addChildren(self, node):
        self.children.append(node)

    def getChildren(self):
        return self.children

    def getFather(self):
        return self.father

    def isWinning(self, player):
        return self.board.checkVictory(player)