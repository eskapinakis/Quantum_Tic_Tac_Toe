from boards import Board


class RegularTicTacToe(Board.Board):

    def play(self, line, col, player):
        if not self.isOccupied(line, col):
            self.tiles[line][col] = player

    def getWinner(self):
        if self.checkVictory('O'):
            return "O has won"
        if self.checkVictory('X'):
            return "X has won"
        elif self.isFull():
            return "It's a Tie"
        return "banana"