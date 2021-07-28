from data_structures import Node
from boards import TicTacToe as SB
from math import inf
from ai import Algorithms as Alg


class Minimax(Alg.Algorithms):

    root = None

    def __init__(self, board, player):
        super().__init__(board, player)

        self.root = Node.Node()
        self.root.copyBoard(board.getBoard())

        # print('Root Board')
        # self.printBoard(self.root.getBoard())

    def getMove(self):
        print('')
        best = 0
        i = 0

        self.generateChildren(self.root, self.piece)
        bestChild = self.root.getChildren()[0]

        for child in self.root.getChildren():
            # eval = self.minimax(child, 4, self.piece)
            eval = self.evalTerminal(child)
            print('eval ', i, ' : ', eval, ' move: ', child.getMove())
            i += 1
            if eval > best:
                bestChild = child
                best = eval

        # print('final move:', move)
        # print('Child Board')
        # self.printBoard(bestChild.getBoard())

        return bestChild.getMove()

    def evalTerminal(self, node):

        # Immediate
        if node.isWinning(self.other):
            return -10
        if node.isWinning(self.piece):
            return 10

        # In next move
        if self.isThereWinningMove(node.getBoard(), self.other):
            return -7
        if self.isThereWinningMove(node.getBoard(), self.piece):
            return 7

        # In two next moves
        if self.enablesTwoOptions(node.getBoard(), self.other):
            return -5
        if self.enablesTwoOptions(node.getBoard(), self.piece):
            return 5

        # Some Heuristics
        if node.getBoard().getTile(1, 1) == self.other:
            return -2
        if node.getBoard().getTile(1, 1) == self.piece:
            return 2

        # Nhe
        else:
            return 0

    def generateChildren(self, node, player):

        # self.printBoard(node.getBoard())

        for i in range(9):
            line = self.getCoordinates(i)[0]
            col = self.getCoordinates(i)[1]

            board = SB.SmallBoard()  # create a new board
            board.copyTiles(node.getBoard().getBoard())

            # self.printBoard(board)

            if not board.isOccupied(line, col):
                board.play(line, col, player)
                # creates a child of node - [line, col] is the move that originated the node
                child = Node.Node(node, board, [line, col])
                node.addChildren(child)
                # self.printBoard(child.getBoard())
                # print('child move: ', child.getMove())

    def minimax(self, node, depth, maximizing):

        if depth == 0 or node.isWinning(self.piece) or node.isWinning(self.other) or \
                node.isFull():
            return self.evalTerminal(node)

        if maximizing:
            self.generateChildren(node, self.piece)
            maxEval = -inf
            for child in node.children:
                eval = self.minimax(child, depth - 1, False)
                maxEval = max(maxEval, eval)
            return maxEval

        else:
            self.generateChildren(node, self.other)
            minEval = inf
            for child in node.children:
                eval = self.minimax(child, depth - 1, True)
                minEval = min(minEval, eval)
            return minEval