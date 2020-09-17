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
    def __init__(self, token: str):
        super().__init__(token)

    def get_move(self):
        """
        Gets the user's move from the standard input and returns it as a string.
        """
        return input('Enter the coordinates: ').strip().split()


class AI(Player):
    """
    An AI (computer) player).
    """
    def __init__(self, token: str, difficulty: str):
        super().__init__(token)
        self.difficulty = difficulty

    def calculate_move(self, board: Board):
        """
        Calculates the AI move according to difficulty.

        :param board: (Board) The game board object.
        :return: (tuple of 2 int) The AI move in user-coordinate format.
        """
        # Note that the medium and hard difficulty move algorithms have their
        # own methods, but the easy move is simple enough to be included in this
        # method's body.
        if self.difficulty == 'easy':
            return self.easy_move(board)

        elif self.difficulty == 'medium':
            return self.medium_move(board)

        elif self.difficulty == 'hard':
            pass

    def easy_move(self, board: Board):
        """
        The algorithm for making an easy-level move. It's just a random move.

        :param board: The game board.
        :return: (tuple of 2 int) The AI move in user-coordinate format.
        """
        open_cells = self.get_token_cells(board, ' ')
        return rand_choice(open_cells)

    def medium_move(self, board: Board):
        """
        The algorithm for making a medium-level move.

        :param board: (Board) The game board object.
        :return: (tuple of 2 int) The coordinates of the AI's move.
        """

        # 1. can we win in one move?
        winning_move = self.one_move_win(board, self.token)
        if winning_move is not None:
            return winning_move  # go ahead and win

        # 2. is the opponent capable of winning in one move?
        if self.token == 'X':
            losing_move = self.one_move_win(board, 'O')
        else:
            losing_move = self.one_move_win(board, 'X')

        if losing_move is not None:
            return losing_move  # block them

        # 3. otherwise, move randomly
        return self.easy_move(board)

    @staticmethod
    def one_move_win(board: Board, token: str):
        """
        Determines whether the player with the given token can win in one move.
        If they can win in one move, returns the coordinates of that move.

        :param board: The game board.
        :param token: The token in question. ' ', 'X', or 'O'
        :return: (tuple of 2 int) Coordinates of the winning move. If an
            immediate winning move doesn't exits, returns None.
        """
        if token == 'X':
            winning_lines = ['XX ', 'X X', ' XX']
        else:
            winning_lines = ['OO ', 'O O', ' OO']

        for row in range(1, 4):
            row_tokens = ''.join(board.get_row(row))
            if row_tokens in winning_lines:
                return row_tokens.find(' ') + 1, row

        for column in range(1, 4):
            column_tokens = ''.join(board.get_column(column))
            if column_tokens in winning_lines:
                return column, 3 - column_tokens.find(' ')

        diagonal1 = ''.join(board.get_diagonal(1))
        if diagonal1 in winning_lines:
            column_index = diagonal1.find(' ') + 1
            return column_index, 4 - column_index

        diagonal2 = ''.join(board.get_diagonal(2))
        if diagonal2 in winning_lines:
            column_index = 4 - (diagonal2.find(' ') + 1)
            return column_index, column_index

        return None

    @staticmethod
    def get_token_cells(board: Board, token: str):
        """
        Determines which cells on the board are occupied by the specified token
        (' ', 'X', or 'O').

        :param board: The game board object.
        :param token: All cells in the returned list are occupied by this token.
        :return: (list) The list of open cells, each element of which is a tuple
            containing that cell's coordinates. Ordered by increasing row &
            column.
        """
        cells = []
        for x in range(1, 4):  # x-coord of board
            for y in range(1, 4):  # y-coord of board
                if board.check_cell((x, y)) == token:
                    cells.append((x, y))

        return cells


if __name__ == '__main__':
    my_board = Board()
    my_board.state = '____X__XO'
    print(my_board)

    my_AI = AI('O', 'medium')
    print(my_AI.medium_move(my_board))
