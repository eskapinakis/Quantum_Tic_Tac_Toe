class Board:

    tiles = []

    def __init__(self):
        self.tiles = [['' for _ in range(3)] for _ in range(3)]

    def copyTiles(self, tiles):
        for i in range(3):
            for j in range(3):
                self.tiles[i][j] = tiles[i][j]

    def isEmpty(self, line, col):
        return self.tiles[line][col] == ''

    def isOccupied(self, line, col):
        return len(self.tiles[line][col]) == 1 or \
            len(self.tiles[line][col]) > 3  # also works for quantum

    def getLine(self, i):
        return self.tiles[i]

    def getColumn(self, i):
        return [self.tiles[0][i], self.tiles[1][i], self.tiles[2][i]]

    def getDiagonal(self, i):
        if i == 0:
            return [self.tiles[0][0], self.tiles[1][1], self.tiles[2][2]]
        else:
            return [self.tiles[0][2], self.tiles[1][1], self.tiles[2][0]]

    @staticmethod
    def allEqual(array, player):
        return all(elem == player for elem in array)

    def checkVictory(self, player):
        return self.colVictory(player) or self.lineVictory(player) or self.diagonalVictory(player)

    def lineVictory(self, player):
        for i in range(3):
            if self.allEqual(self.getLine(i), player):
                return True
        return False

    def colVictory(self, player):
        for i in range(3):
            if self.allEqual(self.getColumn(i), player):
                return True
        return False

    def diagonalVictory(self, player):
        for i in range(2):
            if self.allEqual(self.getDiagonal(i), player):
                return True
        return False

    def getTile(self, line, col):
        return self.tiles[line][col]

    def getBoard(self):
        return self.tiles

    def eraseMove(self, line, col):
        self.tiles[line][col] = ''

    def isFull(self):
        for i in range(3):
            for j in range(3):
                if len(self.tiles[i][j]) != 1:
                    return False
        return True

    def isKindaFull(self):
        for i in range(3):
            for j in range(3):
                if not self.isOccupied(i, j):
                    return False
        return True

    def printBoard(self):
        for l in self.tiles:
            print(l)