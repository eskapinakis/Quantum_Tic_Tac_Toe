class Algorithms:

    board = None
    piece = ''
    other = ''
    move = None

    def __init__(self, board, piece='O'):
        self.move = []

        self.assignBoard(board)

        self.piece = piece
        if piece == 'X':
            self.other = 'O'
        else:
            self.other = 'X'

    def assignBoard(self, board):
        self.board = board

    def printBoard(self, board=None):
        if not board:
            board = self.board
        for l in board.getBoard():
            print(l)

    @staticmethod
    def getCoordinates(index):

        line = int(index / 3)
        col = int(index % 3)
        return [line, col]

    # move to wint the game
    def moveToWin(self):

        board = self.board
        for i in range(3):
            for j in range(3):
                if not board.isOccupied(i, j):
                    board.play(i, j, self.piece)
                    if board.checkVictory(self.piece):
                        self.move = [i, j]
                        board.eraseMove(i, j)
                        return True
                    else:
                        board.eraseMove(i, j)

        return False

    # move to block a victory from the opponent
    def moveToBlock(self):

        board = self.board
        for i in range(3):
            for j in range(3):
                if not board.isOccupied(i, j):
                    board.play(i, j, self.other)
                    if board.checkVictory(self.other):
                        self.move = [i, j]
                        board.eraseMove(i, j)
                        return True
                    else:
                        board.eraseMove(i, j)
        return False

    def enablesTwoOptions(self, board, piece):  # to see if a move will enable two options

        if piece == 'X':
            other = 'O'
        else:
            other = 'X'

        for i in range(3):
            for j in range(3):
                if not board.isOccupied(i, j):
                    board.play(i, j, piece)
                    if self.twoWinningOptions(board, piece) and \
                            not self.isThereWinningMove(board, other):
                        board.eraseMove(i, j)
                        return True
                    board.eraseMove(i, j)

        return False

    @staticmethod
    def twoWinningOptions(board, piece):  # to see if there are two winning moves for a player

        winningMoves = 0

        for i in range(3):  # counts the number of winning moves
            for j in range(3):
                if not board.isOccupied(i, j):
                    board.play(i, j, piece)
                    if board.checkVictory(piece):
                        winningMoves += 1
                    board.eraseMove(i, j)

        if winningMoves > 1:
            return True

        return False

    @staticmethod
    def isThereWinningMove(board, piece):

        for i in range(3):
            for j in range(3):
                if not board.isOccupied(i, j):
                    board.play(i, j, piece)
                    if board.checkVictory(piece):
                        board.eraseMove(i, j)
                        return True
                    board.eraseMove(i, j)

        return False