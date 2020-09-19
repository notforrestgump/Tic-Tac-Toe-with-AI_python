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
    An AI (computer) player.
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
            return self.hard_move(board)

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

    def hard_move(self, board: Board):
        """
        Implements the Minimax algorithm to find a good move. Automatically
        moves in a corner space if it is the first player to move.
        """
        open_cells = self.get_token_cells(board, ' ')
        if len(open_cells) == 9:
            return rand_choice([(1, 1), (3, 1), (3, 3), (1, 3)])
        else:
            return self.minimax(board)

    def minimax(self, board: Board):
        """Minimax algorithm"""
        m, col, row = self.max(board, -2, 2)
        return col, row

    def max(self, board: Board, alpha, beta):
        """Used to maximize the AI score for the minimax algorithm."""
        max_value = -2

        move_col = None
        move_row = None

        result = self.determine_game_state(board)

        ai_token = self.token
        other_token = 'X' if ai_token == 'O' else 'O'

        # base case
        if result == f'{other_token} wins':
            return -1, 0, 0
        elif result == f'{ai_token} wins':
            return 1, 0, 0
        elif result == 'Draw':
            return 0, 0, 0

        # if not a terminal case, make a move and call min
        open_cells = self.get_token_cells(board, ' ')

        for cell in open_cells:
            board.update_cell(cell, ai_token)
            (m, min_col, min_row) = self.min(board, alpha, beta)

            # update the max value if needed
            if m > max_value:
                max_value, move_col, move_row = m, cell[0], cell[1]

            board.update_cell(cell, ' ')  # set the board back to normal

            # alpha/beta trimming
            if max_value >= beta:
                return max_value, move_col, move_row

            if max_value > alpha:
                alpha = max_value

        return max_value, move_col, move_row

    def min(self, board: Board, alpha, beta):
        """Used to minimize the opponent score for the minimax algorithm."""
        min_value = 2

        move_col = None
        move_row = None

        result = self.determine_game_state(board)

        ai_token = self.token
        other_token = 'X' if ai_token == 'O' else 'O'

        # base case
        if result == f'{other_token} wins':
            return -1, 0, 0
        elif result == f'{ai_token} wins':
            return 1, 0, 0
        elif result == 'Draw':
            return 0, 0, 0

        # if not a terminal case, make a move and call min
        open_cells = self.get_token_cells(board, ' ')

        for cell in open_cells:
            board.update_cell(cell, other_token)
            (m, max_col, max_row) = self.max(board, alpha, beta)

            # update the max value if needed
            if m < min_value:
                min_value, move_col, move_row = m, cell[0], cell[1]

            board.update_cell(cell, ' ')  # set the board back to normal

            # alpha/beta trimming
            if min_value <= alpha:
                return min_value, move_col, move_row

            if min_value < beta:
                beta = min_value

        return min_value, move_col, move_row

    def determine_game_state(self, board: Board):
        """
        Determines whether the game has concluded or remains unfinished. If the
        game is over, determines whether the outcome is an X victory, O victory,
        or a draw.

        :param board: The game board.
        :return: (str) 'Game not finished' if the game isn't over, 'Draw',
        'X wins', or 'O' wins otherwise.
            otherwise.
        """
        # did anyone win?
        if self.is_token_victory(board, 'X'):
            return 'X wins'
        elif self.is_token_victory(board, 'O'):
            return 'O wins'

        # is the game unfinished?
        for row in range(1, 4):
            for column in range(1, 4):
                if board.check_cell((row, column)) == ' ':
                    return 'Game not finished'

        # must've been a draw
        return 'Draw'

    @staticmethod
    def is_token_victory(board: Board, token: str):
        """
        Checks the board to see if the given token has won by claiming three
        cells in a row vertically, horizontally, or diagonally.

        :param board: The game board.
        :param token: (str) 'X' or 'O'
        :return: (bool) True if token has claimed victory, False otherwise.
        """
        # horizontal
        for row in range(1, 4):
            tokens_in_row = 0
            for column in range(1, 4):
                if board.check_cell((row, column)) == token:
                    tokens_in_row += 1
            if tokens_in_row == 3:
                return True

        # vertical
        for column in range(1, 4):
            tokens_in_column = 0
            for row in range(1, 4):
                if board.check_cell((row, column)) == token:
                    tokens_in_column += 1
            if tokens_in_column == 3:
                return True

        # diagonals
        diagonal1 = [
            board.check_cell((1, 1)),
            board.check_cell((2, 2)),
            board.check_cell((3, 3))
        ]
        diagonal2 = [
            board.check_cell((1, 3)),
            board.check_cell((2, 2)),
            board.check_cell((3, 1))
        ]
        if all([t == token for t in diagonal1]):
            return True
        elif all([t == token for t in diagonal2]):
            return True

        return False

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
    my_board.state = '_OOXX____'
    print(my_board)
