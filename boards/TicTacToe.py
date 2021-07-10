class SmallBoard:

    tiles = []

    initialTile = []
    cycle = []

    def __init__(self):
        self.tiles = [['' for _ in range(3)] for _ in range(3)]
        self.cycle = []
        self.initialTile = []

    def isOccupied(self, line, col):
        return self.tiles[line][col] != ''

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

    def play(self, line, col, player):
        if self.tiles[line][col] == '':
            self.tiles[line][col] = player
        else:
            self.tiles[line][col] += ' ' + player

    def findIndex(self, index, current_tile):  # finds the other tile where the index is
        for i in range(3):
            for j in range(3):
                if str(index) in self.tiles[i][j] and [i, j] != current_tile:
                    return [i, j]

    def getMessage(self):
        tileCoordinates = self.cycle[len(self.cycle)-1]
        tile = self.tiles[tileCoordinates[0]][tileCoordinates[1]]
        return [str(tile[0]) + str(tile[1]), str(tile[3]) + str(tile[4])]

    def getCycle(self):
        return self.cycle

    def hasCycle(self, line, col):  # checks if there is a cycle starting in this tile

        self.cycle = []
        self.initialTile = [line, col]  # to know where you pass through
        tile = self.tiles[line][col]
        if len(tile) <= 2 or tile[1] == tile[4]:
            return False

        nextTile = self.findIndex(tile[1], [line, col])
        if self.recursiveHasCycle(nextTile[0], nextTile[1], tile[1]):
            return True
        return False

    def isFull(self):

        # if it's a regular draw
        k = 0
        for i in range(3):
            for j in range(3):
                if self.tiles[i][j] in ['X', 'O']:
                    k += 1
        if k == 9:
            return True

        for i in range(3):
            for j in range(3):
                if len(self.tiles[i][j]) < 5:
                    return False
        return True

    # the previous index is to make him walk the cycle in one direction
    def recursiveHasCycle(self, line, col, previous_index):

        if self.initialTile in self.cycle:  # then there is a cycle
            return True

        tile = self.tiles[line][col]  # check if current tile can be in a net
        if len(tile) <= 2:
            return False
        self.cycle.append([line, col])

        index1 = tile[1]  # find the two pointers from this house
        index2 = tile[4]
        if index2 == previous_index:
            NextTile = self.findIndex(index1, [line, col])
            index = index1
        else:
            NextTile = self.findIndex(index2, [line, col])
            index = index2

        if self.recursiveHasCycle(NextTile[0], NextTile[1], index):
            return True

    def collapseUncertainty(self, choice):

        i = len(self.cycle)-1
        tileCoordinate = self.cycle[i]

        self.tiles[tileCoordinate[0]][tileCoordinate[1]] = choice[0]  # put the choice

        nextTile = self.findIndex(choice[1], tileCoordinate)
        if nextTile == self.cycle[i-1]:
            # print("minus")
            self.collapseUncertaintyRecursiveMinus(choice, i - 1)
        else:
            # print("plus")
            self.collapseUncertaintyRecursivePlus(choice, 0)

    def collapseUncertaintyRecursiveMinus(self, choice, i):

        if i < 0:
            return

        tileCoordinate = self.cycle[i]
        data = self.tiles[tileCoordinate[0]][tileCoordinate[1]]
        index = choice[1]  # see the index sent - says which will be removed

        if index == data[1]:  # if you will remove the first
            self.tiles[tileCoordinate[0]][tileCoordinate[1]] = data[3]
            data = data[3]+data[4]
        elif index == data[4]:  # if you will remove the second
            self.tiles[tileCoordinate[0]][tileCoordinate[1]] = data[0]
            data = data[0] + data[1]

        self.collapseUncertaintyRecursiveMinus(data, i - 1)

    def collapseUncertaintyRecursivePlus(self, choice, i):

        if i == len(self.cycle)-1:
            return

        tileCoordinate = self.cycle[i]
        data = self.tiles[tileCoordinate[0]][tileCoordinate[1]]
        index = choice[1]  # see the index sent - says which will be removed

        if index == data[1]:  # if you will remove the first
            self.tiles[tileCoordinate[0]][tileCoordinate[1]] = data[3]
            data = data[3]+data[4]
        elif index == data[4]:  # if you will remove the second
            self.tiles[tileCoordinate[0]][tileCoordinate[1]] = data[0]
            data = data[0] + data[1]

        self.collapseUncertaintyRecursivePlus(data, i + 1)