from boards import TicTacToe as SB


class Node:

    father = None
    board = None
    move = None
    move2 = None
    children = []

    def __init__(self, node=None, board=None, move=None, move2=None):
        self.children = []
        self.father = node
        self.board = SB.SmallBoard()
        if board:
            self.board.copyTiles(board.getBoard())
        self.move = move
        self.move2 = move2

    def getBoard(self):
        return self.board

    def addChildren(self, node):
        self.children.append(node)

    def deleteChildren(self):
        self.children = []

    def getChildren(self):
        return self.children

    def getFather(self):
        return self.father

    def getMove(self):
        return self.move

    def getMove2(self):
        return self.move2

    def isWinning(self, player):
        return self.board.checkVictory(player)

    def copyBoard(self, tiles):
        self.board.copyTiles(tiles)

    def copyFather(self):
        self.board.copyTiles(self.getFather().getBoard().getBoard())

    def play(self, coord, player):
        line = coord[0]
        col = coord[1]
        self.board.play(line, col, player)

    def isFull(self):
        return self.board.isFull()