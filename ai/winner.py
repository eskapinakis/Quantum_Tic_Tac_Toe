from data_structures import Node
from boards import QuantumTicTacToe as Q, RegularTicTacToe as T
from math import inf
from ai import Algorithms as Alg


class Winner:

    def __init__(self, board, player, quantum=True, first=False, index=0):
        self.board = board
        self.player = player

        assert (not first)
        assert quantum

    def getMove(self):
        pass