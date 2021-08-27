from data_structures import Node
from boards import QuantumTicTacToe as Q, RegularTicTacToe as T
from math import inf
from ai import Algorithms as Alg


class Minimax(Alg.Algorithms):

    root = None
    quantum = False
    index = 0
    depth = 0  # the program searches in depth + 1
    first = False

    def __init__(self, board, player, quantum=False, first=False, index=0):

        super().__init__(board, player)

        self.root = Node.Node(board=board)
        self.quantum = quantum
        self.index = index

        if quantum:
            self.depth = 6
        else:
            self.depth = 6

        self.first = first  # to know if this is the first move of the computer

    def getMove(self):
        # Make the first generation
        self.generateChildren(self.root, self.piece, self.index)
        bestChild = self.root.getChildren()[0]
        # print(bestChild.getBoard().getCounters())  # TODO - printing
        best = - inf

        index = self.index
        if not self.first:  # in quantum you play twice
            index += 1

        for child in self.root.getChildren():
            eval = self.pruningMinimax(child, self.depth, -inf, inf, self.first, index, first=not self.first)
            # print(eval)  TODO - printing
            # child.getBoard().printBoard()
            if eval > best:
                bestChild = child
                best = eval
        # print(best, '\n')  # TODO - printing
        return bestChild.getMove()

    def evalTerminal(self, node):
        # node.getBoard().printBoard()  # TODO - Printing
        if node.isWinning(self.other):
            return -1
        elif node.isWinning(self.piece):
            return 1
        return 0

    # creates the next generation
    def generateChildren(self, node, player, index=0):
        if self.quantum:
            self.generateQuantumChildren(node, player, index)
        else:
            self.generateRegularChildren(node, player)

    # only the next generation
    def generateRegularChildren(self, node, player):
        for i in range(9):
            line = self.getCoordinates(i)[0]
            col = self.getCoordinates(i)[1]

            board = T.RegularTicTacToe()  # create a new board
            board.copyTiles(node.getBoard().getBoard())

            if not board.isOccupied(line, col):
                board.play(line, col, player)
                child = Node.Node(node, board, [line, col])  # [line, col] is the child's move
                node.addChildren(child)

    # only the next generation
    def generateQuantumChildren(self, node, player, index):

        counters = node.getBoard().getCounters()

        # """
        if node.isCollapsed():  # if there is a cycle in the node

            boards = self.makeCollapsedBoard(node)  # create the two possible boards
            board1 = boards[0]
            board2 = boards[1]
            # board1.printBoard()  # TODO - printing
            # board2.printBoard()

            for i in self.preference:  # range(9):
                coord = self.getCoordinates(i)
                line = coord[0]
                col = coord[1]

                # copy the first board to create a child
                newBoard1 = Q.QuantumTicTacToe()
                newBoard1.copyTiles(board1.getBoard())
                newBoard1.copyCounters(counters)

                # copy the second board to create another child
                newBoard2 = Q.QuantumTicTacToe()
                newBoard2.copyTiles(board2.getBoard())
                newBoard2.copyCounters(counters)

                if not newBoard1.isOccupied(line, col):
                    newBoard1.play(line, col, player + str(index))
                    children = self.makeBabies(node, newBoard1, line, col)  # to refine the babies
                    for child in children:
                        node.addChildren(child)

                if not newBoard2.isOccupied(line, col):
                    newBoard2.play(line, col, player + str(index))
                    children = self.makeBabies(node, newBoard2, line, col)  # to refine the babies
                    for child in children:
                        node.addChildren(child)

        else:
            for i in self.preference:  # range(9):
                coord = self.getCoordinates(i)
                line = coord[0]
                col = coord[1]

                board = Q.QuantumTicTacToe()  # create a new board
                board.copyTiles(node.getBoard().getBoard())
                board.copyCounters(counters)

                if not board.isOccupied(line, col):
                    board.play(line, col, player+str(index))
                    children = self.makeBabies(node, board, line, col)  # to refine the babies
                    for child in children:
                        node.addChildren(child)

    @staticmethod
    def makeCollapsedBoard(node):
        board = node.getBoard()  # get information from daddy
        coord = node.getMove()
        line = coord[0]
        col = coord[1]

        tile = board.getTile(line, col)  # get te tile where choices will be made
        choice1 = tile[0] + tile[1]
        choice2 = tile[3] + tile[4]

        # create the board for the first choice
        board1 = Q.QuantumTicTacToe()
        board1.copyTiles(board.getBoard())
        board1.copyCycle(board.getCycle())
        board1.collapseUncertainty(choice1)

        # create the board for the second choice
        board2 = Q.QuantumTicTacToe()
        board2.copyTiles(board.getBoard())
        board2.copyCycle(board.getCycle())
        board2.collapseUncertainty(choice2)

        return [board1, board2]

    @staticmethod
    def makeBabies(node, board, line, col):

        child = Node.Node(node, board, [line, col])  # basic stuff

        if board.sameSymbol(line, col):  # if the move was deterministic
            move = board.getTile(line, col)[0]
            board.eraseMove(line, col)
            board.play(line, col, move, replacing=True)
            child = Node.Node(node, board, [line, col])

        # """
        elif board.hasCycle(line, col):
            # the child will have two extra children
            child = Node.Node(node, board, [line, col], collapsed=True)
        # """

        # print(child.getBoard().getCounters())  # TODO - printing
        # child.getBoard().printBoard()

        return [child]

    def minimax(self, node, depth, maximizing):

        if depth == 0 or node.isWinning(self.piece) or node.isWinning(self.other) or \
                node.isFull():
            return self.evalTerminal(node)

        if maximizing:

            self.generateChildren(node, self.piece)  # it's my turn
            maxEval = -inf
            for child in node.children:
                eval = self.minimax(child, depth - 1, False)
                maxEval = max(maxEval, eval)
            return maxEval

        else:

            self.generateChildren(node, self.other)  # it's your turn
            minEval = inf
            for child in node.children:
                eval = self.minimax(child, depth - 1, True)
                minEval = min(minEval, eval)
            return minEval

    # minimax with alpha beta pruning
    def pruningMinimax(self, node, depth, alpha, beta, maximizing, index=0, first=False):

        # node.getBoard().printBoard()  PRINTING

        if depth == 0 or node.isWinning(self.piece) or node.isWinning(self.other) or \
                node.isFull():
            return self.evalTerminal(node)

        if maximizing:

            self.generateChildren(node, self.piece, index)  # it's my turn
            maxEval = -inf
            for child in node.children:
                if first and self.quantum:  # next move is still mine
                    eval = self.pruningMinimax(child, depth - 1, alpha, beta, True, index, False)
                else:  # next move is from opponent
                    eval = self.pruningMinimax(child, depth - 1, alpha, beta, False, index + 1, True)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval

        else:

            self.generateChildren(node, self.other, index)  # it's the opponent's turn
            minEval = inf
            for child in node.children:
                if first and self.quantum:  # next move is still the opponent's
                    eval = self.pruningMinimax(child, depth - 1, alpha, beta, False, index, False)
                else:  # next move is mine
                    eval = self.pruningMinimax(child, depth - 1, alpha, beta, True, index + 1, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return minEval