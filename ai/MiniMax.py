from data_structures import Node
from boards import QuantumTicTacToe as Q, RegularTicTacToe as T
from math import inf
from ai import Algorithms as Alg


class Minimax(Alg.Algorithms):

    root = None
    quantum = False

    def __init__(self, board, player, quantum=False):

        super().__init__(board, player)

        self.root = Node.Node(board=board)
        self.quantum = quantum

    def getMove(self):

        best = - inf

        # Make the first generation
        self.generateChildren(self.root, self.piece)
        bestChild = self.root.getChildren()[0]

        for child in self.root.getChildren():
            # eval = self.minimax(child, 5, False)  # It's now the other guy's move
            eval = self.pruningMinimax(child, 5, -inf, inf, False)
            # print('eval: ', eval, child.getMove())
            # eval = 0
            if eval > best:
                bestChild = child
                best = eval
        if not self.quantum:
            return bestChild.getMove()
        else:
            return [bestChild.getMove(), bestChild.getMove2()]

    def evalTerminal(self, node):

        if node.isWinning(self.other):
            return -1
        elif node.isWinning(self.piece):
            return 1

        '''
        # In next move
        elif self.isThereWinningMove(node.getBoard(), self.other):
            return -10
        elif self.isThereWinningMove(node.getBoard(), self.piece):
            return 10

        # In two next moves
        elif self.enablesTwoOptions(node.getBoard(), self.other):
            return -5
        elif self.enablesTwoOptions(node.getBoard(), self.piece):
            return 5

        # Some Heuristics
        elif node.getBoard().getTile(1, 1) == self.other:
            return -2
        elif node.getBoard().getTile(1, 1) == self.piece:
            return 2
        
        # Nhe
        '''
        return 0

    def generateChildren(self, node, player):

        if not self.quantum:
            self.generateRegularChildren(node, player)
        if self.quantum:
            self.generateQuantumChildren(node, player)

    def generateRegularChildren(self, node, player):
        for i in self.preference:  # range(9):
            line = self.getCoordinates(i)[0]
            col = self.getCoordinates(i)[1]

            board = T.RegularTicTacToe()  # create a new board
            board.copyTiles(node.getBoard().getBoard())

            if not board.isOccupied(line, col):
                board.play(line, col, player)
                child = Node.Node(node, board, [line, col])  # [line, col] is the child's move
                node.addChildren(child)

    def generateQuantumChildren(self, node, player):
        for i in range(9):
            for j in range(9):
                line1 = self.getCoordinates(i)[0]
                col1 = self.getCoordinates(i)[1]

                line2 = self.getCoordinates(j)[0]
                col2 = self.getCoordinates(j)[1]

                board = Q.QuantumTicTacToe()  # create a new board
                board.copyTiles(node.getBoard().getBoard())

                if not board.isOccupied(line1, col1) and \
                        not board.isOccupied(line2, col2):
                    board.play(line1, col1, player)
                    board.play(line2, col2, player)
                    child = Node.Node(node, board, [line1, col1], [line2, col2])
                    node.addChildren(child)

    def minimax(self, node, depth, maximizing):

        if depth == 0 or node.isWinning(self.piece) or node.isWinning(self.other) or \
                node.isFull():
            return self.evalTerminal(node)

        if maximizing:

            self.generateChildren(node, self.piece)  # it's my turn
            maxEval = -inf
            for child in node.children:
                eval = self.minimax(child, depth - 1, False)
                # print('maxi eval: ', eval, ' move: ', child.getMove())
                maxEval = max(maxEval, eval)
            return maxEval

        else:

            self.generateChildren(node, self.other)  # it's your turn
            minEval = inf
            for child in node.children:
                eval = self.minimax(child, depth - 1, True)
                # print('mini eval: ', eval, ' move: ', child.getMove())
                minEval = min(minEval, eval)
            return minEval

    # minima with alpha beta pruning
    def pruningMinimax(self, node, depth, alpha, beta, maximizing):

        if depth == 0 or node.isWinning(self.piece) or node.isWinning(self.other) or \
                node.isFull():
            return self.evalTerminal(node)

        if maximizing:

            self.generateChildren(node, self.piece)  # it's my turn
            maxEval = -inf
            for child in node.children:
                eval = self.pruningMinimax(child, depth - 1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval

        else:

            self.generateChildren(node, self.other)  # it's your turn
            minEval = inf
            for child in node.children:
                eval = self.pruningMinimax(child, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return minEval