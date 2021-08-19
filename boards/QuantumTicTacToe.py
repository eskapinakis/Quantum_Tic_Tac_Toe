from boards import Board


class QuantumTicTacToe(Board.Board):

    counters = []  # this keeps tabs on the index of each move

    winingCol = []  # these are the lines/cols that yield a victory
    winingLine = []
    line = False  # was the sort of tie given by lines

    initialTile = []
    cycle = []

    def __init__(self):

        super().__init__()

        self.counters = [['' for _ in range(3)] for _ in range(3)]

        self.winingCol = []
        self.winingLine = []
        self.line = False

        self.initialTile = []
        self.cycle = []

    def copyCycle(self, cycle):
        self.cycle = cycle

    def getCycle(self):
        return self.cycle

    def getWinCol(self):
        return self.winingCol

    def getWinLine(self):
        return self.winingLine

    def getWinner(self):
        oVictory = False
        xVictory = False

        if self.checkVictory('O'):
            oVictory = True
        if self.checkVictory('X'):
            xVictory = True

        if oVictory and xVictory:
            return self.getBestWinner() + " has Won"
        elif oVictory:
            return "O has won"
        elif xVictory:
            return "X has won"
        elif self.isFull():
            return "It's a Tie"
        return "banana"

    def getCounterColumn(self, i):
        return [self.counters[0][i], self.counters[1][i], self.counters[2][i]]

    def lineVictory(self, player):
        for i in range(3):
            if self.allEqual(self.getLine(i), player):
                if [i, player] not in self.winingLine:
                    self.winingLine.append([i, player])
                self.line = True
                return True
        return False

    def colVictory(self, player):
        for i in range(3):
            if self.allEqual(self.getColumn(i), player):
                if [i, player] not in self.winingCol:
                    self.winingCol.append([i, player])
                self.line = False
                return True
        return False

    @staticmethod
    def removeOtherPlayer(line, player):
        if player == 'X':  # to have the other player
            other = 'O'
        else:
            other = 'X'

        for i in range(len(line)):  # remove the other player from this line
            tile = line[i]
            for j in range(len(tile)):
                if tile[j] == other:
                    tile = tile.replace(tile[j+1], '0')
                    tile = tile.replace(other, player)
            line[i] = tile
        return line

    @staticmethod
    def getSmallestBiggest(line1, line2):

        max1 = 0  # get the biggest index in the first line
        for tile in line1:
            if int(tile[1]) > max1:
                max1 = int(tile[1])
            if int(tile[4]) > max1:
                max1 = int(tile[4])

        max2 = 0  # get the biggest index in the second line
        for tile in line2:
            if int(tile[1]) > max2:
                max2 = int(tile[1])
            if int(tile[4]) > max2:
                max2 = int(tile[4])

        if max1 < max2:  # return the player with the smallest biggest index
            return line1[0][0]
        else:
            return line2[0][0]

    # if both players won
    def getBestWinner(self):
        if self.line:  # if it was a line victory
            line1 = self.counters[int(self.winingLine[0][0])]
            line1 = self.removeOtherPlayer(line1, self.winingLine[0][1])
            line2 = self.counters[int(self.winingLine[1][0])]
            line2 = self.removeOtherPlayer(line2, self.winingLine[1][1])
            return self.getSmallestBiggest(line1, line2)
        else:  # if it was a column victory
            col1 = self.getCounterColumn(int(self.winingCol[0][0]))
            col1 = self.removeOtherPlayer(col1, self.winingCol[0][1])
            col2 = self.getCounterColumn(int(self.winingCol[1][0]))
            col2 = self.removeOtherPlayer(col2, self.winingCol[1][1])
            return self.getSmallestBiggest(col1, col2)

    def getCounters(self):
        return self.counters

    def play(self, line, col, player):
        if self.tiles[line][col] == '':
            self.counters[line][col] = player
            self.tiles[line][col] = player
        else:
            self.counters[line][col] += ' ' + player
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

    def hasCycle(self, line, col):  # checks if there is a cycle starting in this tile
        if self.sameSymbol(line, col):
            return False

        self.cycle = []
        self.initialTile = [line, col]  # to know where you pass through
        tile = self.tiles[line][col]

        if len(tile) < 5 or tile[1] == tile[4]:
            return False

        nextTile = self.findIndex(tile[1], [line, col])
        if self.recursiveHasCycle(nextTile[0], nextTile[1], tile[1]):
            return True
        return False

    # if both particles are in the same tile we collapse it
    def sameSymbol(self, line, col):
        tile = self.tiles[line][col]

        if len(tile) < 5:
            return False

        if tile[0]+tile[1] == tile[3]+tile[4]:
            self.tiles[line][col] = tile[0]
            return True
        return False

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