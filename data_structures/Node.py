from boards import TicTacToe as SB


class Node:

    father = None
    board = None
    move = None
    children = []

    def __init__(self, node=None, board=None, move=None):
        self.father = node
        self.board = SB.SmallBoard()
        if board:
            self.board.copyTiles(board.getBoard())
        self.move = move

    def getBoard(self):
        return self.board

    def addChildren(self, node):
        self.children.append(node)

    def getChildren(self):
        return self.children

    def getFather(self):
        return self.father

    def isWinning(self, player):
        return self.board.checkVictory(player)

    def copyBoard(self):
        self.board.copyTiles(self.getFather().getBoard().getBoard())

    def play(self, coord, player):
        line = coord[0]
        col = coord[1]
        self.board.play(line, col, player)

    def isFull(self):
        return self.board.isFull()