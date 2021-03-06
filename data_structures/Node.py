class Node:

    father = None
    board = None
    move = None
    move2 = None
    collapsed = False
    children = []
    eval = None
    choice = None

    def __init__(self, node=None, board=None, move=None, move2=None, collapsed=False, choice=None):
        self.children = []
        self.father = node
        self.board = board
        self.move = move
        self.move2 = move2
        self.collapsed = collapsed
        self.eval = None
        self.choice = choice

    def setChoice(self, choice):
        self.choice = choice

    def getChoice(self):
        return self.choice

    def setEval(self, eval):
        self.eval = eval

    def getEval(self):
        return self.eval

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
        return self.board.getWinner() == player + " has won"

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

    def isCollapsed(self):
        return self.collapsed

    def setCollapsed(self):
        self.collapsed = True