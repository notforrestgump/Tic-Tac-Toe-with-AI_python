from random import choice as rand_choice
from Board import Board


class Player:
    """
    This class represents a Tic-Tac-Toe player, whether AI or human. Intended as
    a parent class for Human and AI.
    """
    def __init__(self, token: str):
        self._token = token

    @property
    def token(self):
        return self._token


class Human(Player):
    """
    A human (user) player.
    """
    def __init__(self):
        super().__init__('X')

    def get_move(self):
        """
        Gets the user's move from the standard input and returns it as a string.
        """
        return input('Enter the coordinates: ').strip().split()


class AI(Player):
    """
    An AI (computer) player).
    """
    def __init__(self, difficulty):
        super().__init__('O')
        self.difficulty = difficulty  # 0 (easy) 1 (medium) 2 (hard)

    def calculate_move(self, board: Board):
        """
        Calculates the AI move according to difficulty.

        :param board: (Board) The game board object.
        :return: (tuple of 2 int) The AI move in user-coordinate format.
        """
        open_cells = []
        for x in range(1, 4):  # x-coord of board
            for y in range(1, 4):  # y-coord of board
                if board.check_cell((x, y)) == ' ':
                    open_cells.append((x, y))

        if self.difficulty == 0:  # easy
            return rand_choice(open_cells)

        elif self.difficulty == 1:  # medium
            pass
        elif self.difficulty == 2:  # hard
            pass
