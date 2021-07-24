from boards import TicTacToe as SB


class AI:

    sb = None

    def __init__(self):
        self.sb = SB.SmallBoard()

    def generateTree(self, depth):
        return False
