from data_structures import Node
from boards import QuantumTicTacToe as Q, RegularTicTacToe as T
from math import inf
from ai import Algorithms as Alg


# TODO - Falta ver quando ele fecha um ciclo e eu posso escolher

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
            self.depth = 5  # 7  # minimax goes until depth + 1
        else:
            self.depth = 6

        self.first = first  # to know if this is the first move of the computer

    def justReturnBestCollapse(self, line, col):
        self.root.move = [line, col]
        counters = self.root.getBoard().getCounters()
        self.root.getBoard().hasCycle(line, col)
        # print(self.root.getBoard().cycle)

        boards = self.makeCollapsedBoards(self.root)  # create the two possible boards
        board1 = boards[0]
        board2 = boards[2]

        # copy the first board to create a child
        newBoard1 = Q.QuantumTicTacToe()
        newBoard1.copyTiles(board1.getBoard())
        newBoard1.copyCounters(counters)

        # copy the second board to create another child
        newBoard2 = Q.QuantumTicTacToe()
        newBoard2.copyTiles(board2.getBoard())
        newBoard2.copyCounters(counters)

        child1 = Node.Node(self.root, newBoard1, [line, col])  # basic stuff
        self.root.addChildren(child1)

        child2 = Node.Node(self.root, newBoard2, [line, col])  # basic stuff
        self.root.addChildren(child2)

        if self.evalTerminal(child1) > self.evalTerminal(child2):
            return child1.getBoard()
        else:
            return child2.getBoard()

    # First time you use the algorithm it'll take forever
    def getFirstMove(self, line=None, col=None):

        # If it's the first time, you might have to collapse the board
        if self.first:
            self.root.move = [line, col]
            if self.root.getBoard().hasCycle(line, col):
                self.root.setCollapsed()

        # Make the first generation
        self.generateChildren(self.root, self.piece, self.index)
        children = self.root.getChildren()
        bestChild = children[0]
        best = - inf

        index = self.index
        if not self.first:  # so the next index is the player's (maybe)
            index += 1

        for child in children:
            # print('here: ', child.choice)  # PRINTING self.depth
            eval = self.pruningMinimax(child, self.depth, -inf, inf, self.first, index, first=not self.first)
            if eval > best:
                bestChild = child
                best = eval

        return [bestChild.getMove(), bestChild.getBoard()]

    # If we evaluated the nodes already we can check which one is the best
    @staticmethod
    def getBestBaby(node):
        best = -inf
        children = node.getChildren()
        bestChild = children[0]
        for child in children:
            if child.getEval() and child.getEval() > best:
                bestChild = child
                best = child.getEval()
        return bestChild

    def evalTerminal(self, node):
        if node.isWinning(self.other):
            node.setEval(-1)
            return -1
        elif node.isWinning(self.piece):
            node.setEval(1)
            return 1
        node.setEval(0)
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

        if node.isCollapsed():
            boards = self.makeCollapsedBoards(node)  # create the two possible boards
            board1 = boards[0]
            choice1 = boards[1]
            board2 = boards[2]
            choice2 = boards[3]

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
                    child = self.makeBabies(node, newBoard1, line, col)  # to refine the babies
                    child.setChoice(choice1)
                    node.addChildren(child)
                    # print(child.getChoice())

                if not newBoard2.isOccupied(line, col):
                    newBoard2.play(line, col, player + str(index))
                    child = self.makeBabies(node, newBoard2, line, col)  # to refine the babies
                    child.setChoice(choice2)
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
                    child = self.makeBabies(node, board, line, col)  # to refine the babies
                    node.addChildren(child)

    @staticmethod
    def makeCollapsedBoards(node):
        board = node.getBoard()  # get information from daddy
        coord = node.getMove()
        line = coord[0]
        col = coord[1]

        # get the tile where choices will be made
        tile = board.getTile(line, col)
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

        return [board1, choice1, board2, choice2]

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

        return child

    # minimax with alpha beta pruning
    def pruningMinimax(self, node, depth, alpha, beta, maximizing, index=0, first=False):

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
                node.setEval(eval)
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
                node.setEval(eval)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return minEval