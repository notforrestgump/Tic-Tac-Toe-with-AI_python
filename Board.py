class Board:
    """
    Represents the Tic-Tac-Toe game board.

    One of the major functions of this class is to abstract away the difference
    between user coordinates (origin (1, 1) at bottom left) and list coordinates
    (origin (0,0) at top left). All instance methods that take coordinates as
    arguments must accept user-format coordinates.
    """
    state_int_to_str = {0: ' ', 1: 'X', 2: 'O'}  # note discrepancy ' ' vs '_'
    state_str_to_int = {' ': 0, '_': 0, 'X': 1, 'O': 2}  # ^^

    def __init__(self):
        self._state = [  # 0 is blank, 1 is X, 2 is O
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

    def __str__(self):
        output = '-' * 9  # top border
        for row in self._state:
            output += '\n| '  # left border
            for num in row:
                token = self.state_int_to_str[num]
                output += token + ' '  # actual board spaces
            output += '|'  # right border
        output += '\n' + ('-' * 9)  # bottom border
        return output

    def update_cell(self, coords: tuple, token: str):
        """
        Updates the given space on the board with the provided token.

        :param coords: (tuple of 2 ints) Board space coordinates in user format.
        :param token: (str) The desired new token for the given space. Options
            are ' ', 'X', and 'O'.
        """
        if token == ' ':
            token = '_'  # so that state_str_to_int can read properly

        row, column = self.convert_coords(coords)
        self._state[row][column] = self.state_str_to_int[token]

    def check_cell(self, coords: tuple):
        """
        Checks whether a given space on the board is empty, X, or O.

        :param coords: (tuple of ints) Board space coordinates in user format.
        :return: (str) Token at that spot on the board (' ', 'X', or 'O').
        """
        row, column = self.convert_coords(coords)
        space_state = self._state[row][column]
        return self.state_int_to_str[space_state]

    def get_row(self, row_number: int):
        """Returns the tokens in the selected row as a list."""
        row_tokens = []
        for column in range(1, 4):
            row_tokens.append(self.check_cell((column, row_number)))

        return row_tokens

    def get_column(self, column_number: int):
        """Returns the tokens in the selected column as a list."""
        column_tokens = []
        for row in range(3, 0, -1):
            column_tokens.append(self.check_cell((column_number, row)))

        return column_tokens

    def get_diagonal(self, diagonal_number: int):
        """
        Returns the tokens in the selected diagonal as a list, ordered from
        topmost to bottommost.

        :param diagonal_number: 1 indicates the diagonal which includes (1, 3),
            and 2 indicates the diagonal which includes (1, 1).
        :return: (list of str) The elements of the chosen diagonal from top to
            bottom.
        """
        if diagonal_number == 1:
            diagonal_tokens = [self.check_cell((1, 3)),
                               self.check_cell((2, 2)),
                               self.check_cell((3, 1))]
        elif diagonal_number == 2:
            diagonal_tokens = [self.check_cell((3, 3)),
                               self.check_cell((2, 2)),
                               self.check_cell((1, 1))]
        else:
            diagonal_tokens = None

        return diagonal_tokens

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        """
        :param new_state: (str) The board state as a 9-character string.
            '_' is blank, 'X' is X, 'O' is O.
        """
        if len(new_state) == 9:
            for i, char in enumerate(new_state):
                self._state[i//3][i % 3] = self.state_str_to_int[char]
        else:
            print('Invalid board state.')

    @staticmethod
    def convert_coords(coords: tuple):
        """
        Converts user-format coordinates to list-format coordinates.

        :param coords: (tuple of 2 ints) (x, y) coordinates, origin (1, 1)
            at bottom left.
        :return: (tuple of 2 ints) (row, column) coordinates. Top row is 0,
            first column index is 0.
        """
        x, y = coords
        return (3-y), (x-1)


if __name__ == '__main__':
    board = Board()
    board.state = '____X__XO'
    print(board)
    print('|', ''.join(board.get_column(2)), '|')
