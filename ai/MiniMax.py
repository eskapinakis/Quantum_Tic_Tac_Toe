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
        best = - inf
        i = 0

        # Make the first generation
        self.generateChildren(self.root, self.piece)
        bestChild = self.root.getChildren()[0]

        print('')
        for child in self.root.getChildren():  # It's now the other guy's move
            # print('')
            # print('best eval: ', best)
            eval = self.minimax(child, 2, False)  # eval = self.evalTerminal(child)

            print('eval ', i, ': ', eval, ' move: ', child.getMove())
            i += 1
            if eval > best:
                bestChild = child
                best = eval

        # print('final move:', bestChild.getMove(), ' eval: ', eval)
        # print('Child Board')
        # self.printBoard(bestChild.getBoard())

        return bestChild.getMove()

    def evalTerminal(self, node):
        # Immediate
        if node.isWinning(self.other):
            return -10
        elif node.isWinning(self.piece):
            return 10

        '''
        # In next move
        elif self.isThereWinningMove(node.getBoard(), self.other):
            return -7
        elif self.isThereWinningMove(node.getBoard(), self.piece):
            return 7

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
        else:
        '''
        return 0

    def generateChildren(self, node, player):

        # self.printBoard(node.getBoard())

        for i in range(9):
            line = self.getCoordinates(i)[0]
            col = self.getCoordinates(i)[1]

            board = SB.SmallBoard()  # create a new board
            board.copyTiles(node.getBoard().getBoard())

            # self.printBoard(board)
            # print('Child Boards')

            if not board.isOccupied(line, col):
                board.play(line, col, player)
                # creates a child of node - [line, col] is the move that originated the node
                child = Node.Node(node, board, [line, col])
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
