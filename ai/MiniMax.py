from data_structures import Node
from boards import TicTacToe as SB
from math import inf
from ai import Algorithms as Alg


class Minimax(Alg.Algorithms):

    root = None

    def __init__(self, board):
        super().__init__(board)
        self.root = Node.Node(self.board)

    def evalTerminal(self, node):
        if node.isWinning(self.piece):
            return 10
        if node.isWinning(self.other):
            return -10
        else:
            return 0

    def generateChildren(self, node, player):
        board = SB.SmallBoard()
        board.copyTiles(node.getBoard().getBoard())

        for i in range(9):
            line = self.getCoordinates(i)[0]
            col = self.getCoordinates(i)[1]
            if not board.isOccupied(line, col):
                board.play(line, col, player)
                # creates a child of node - [line, col] is the move that originated the node
                child = Node.Node(node, board, [line, col])
                node.addChildren(child)
                board.eraseMove(line, col)

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