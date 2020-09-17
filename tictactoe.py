from Board import Board
from Player import Human, AI


class InvalidTokenError(Exception):
    def __init__(self, token):
        self.message = f"{token} is not a valid token. Valid tokens are 'X' " \
                       f"and 'O'."
        super().__init__(self.message)


class TicTacToe:
    """
    The main application for the Tic-Tac-Toe with AI game!
    """
    def __init__(self):
        self.board = Board()
        self.player1 = Human()
        self.player2 = AI(0)
        self.players = (self.player1, self.player2)

    def run(self):
        """
        Call this to begin the game.
        """
        self.board.state = '_________'
        print(self.board)

        player_toggle = 0  # controls who is the current player

        # MAIN GAME LOOP
        game_state = self.get_game_state()
        while game_state == 'Game not finished':
            current_player = self.players[player_toggle]

            if type(current_player) is Human:
                self.do_user_move(current_player)
            elif type(current_player) is AI:
                self.do_computer_move(current_player)

            print(self.board)

            game_state = self.get_game_state()
            player_toggle = (player_toggle + 1) % 2  # switch to the other player

        print(game_state)

    def do_user_move(self, player: Human):
        """
        Takes the user's move from the standard input and updates the board.
        Checks to be sure that the move is valid and requests input until a
        valid move is given.

        :param player: (Human) The human user object making the move.
        """
        while True:
            move = player.get_move()

            try:
                move = [int(s) for s in move]
            except ValueError:
                print('You should enter numbers!')
            else:

                move = tuple(move)
                if len(move) != 2:
                    print('You should enter 2 coordinates!')
                elif not self.move_is_on_board(move):
                    print('Coordinates should be from 1 to 3!')
                elif not self.is_open_cell(move):
                    print('This cell is occupied! Choose another one!')

                else:
                    self.board.update_cell(move, player.token)
                    break

    def do_computer_move(self, player: AI):
        """
        Performs a move for an AI player.

        :param player: (AI) The AI player making the move
        """
        print('Making move level "easy"')

        move = player.calculate_move(self.board)
        self.board.update_cell(move, player.token)

    def is_open_cell(self, coords: tuple):
        """
        Accepts a pair of coordinates, then checks the board to see whether the
        cell in question is occupied or not.

        :param coords: (tuple of 2 ints) Board cell coordinates
        :return: (bool) True if space is unoccupied, False otherwise
        """
        token = self.board.check_cell(coords)
        return token == ' '

    def is_x_turn(self):
        """
        Determines whose turn it is, X or O. Since X always goes first, we know
        it is O's turn when there are more X on the board than O.

        :return: (bool) True if X should go next, False if O should go next.
        """
        x_count = 0
        o_count = 0
        for column in range(1, 4):
            for row in range(1, 4):
                if self.board.check_cell((column, row)) == 'X':
                    x_count += 1
                elif self.board.check_cell((column, row)) == 'O':
                    o_count += 1

        return o_count >= x_count

    def get_game_state(self):
        """
        Determines whether the game has concluded or remains unfinished. If the
        game is over, determines whether the outcome is an X victory, O victory,
        or a draw.

        :return: (str) 'Game not finished' if the game isn't over, 'Draw',
        'X wins', or 'O' wins otherwise.
            otherwise.
        """
        # did anyone win?
        if self.is_token_victory('X'):
            return 'X wins'
        elif self.is_token_victory('O'):
            return 'O wins'

        # is the game unfinished?
        for row in range(1, 4):
            for column in range(1, 4):
                if self.board.check_cell((row, column)) == ' ':
                    return 'Game not finished'

        # must've been a draw
        return 'Draw'

    def is_token_victory(self, token: str):
        """
        Checks the board to see if the given token has won by claiming three
        cells in a row vertically, horizontally, or diagonally.

        :param token: (str) 'X' or 'O'
        :return: (bool) True if token has claimed victory, False otherwise.
        """
        if token != 'X' and token != 'O':
            raise InvalidTokenError(token)

        # horizontal
        for row in range(1, 4):
            tokens_in_row = 0
            for column in range(1, 4):
                if self.board.check_cell((row, column)) == token:
                    tokens_in_row += 1
            if tokens_in_row == 3:
                return True

        # vertical
        for column in range(1, 4):
            tokens_in_column = 0
            for row in range(1, 4):
                if self.board.check_cell((row, column)) == token:
                    tokens_in_column += 1
            if tokens_in_column == 3:
                return True

        # diagonals
        diagonal1 = [
            self.board.check_cell((1, 1)),
            self.board.check_cell((2, 2)),
            self.board.check_cell((3, 3))
        ]
        diagonal2 = [
            self.board.check_cell((1, 3)),
            self.board.check_cell((2, 2)),
            self.board.check_cell((3, 1))
        ]
        if all([t == token for t in diagonal1]):
            return True
        elif all([t == token for t in diagonal2]):
            return True

        return False

    @staticmethod
    def get_start_state():
        """
        Takes the board start state from the standard input. Input must be 9
        characters long consisting of no characters other than '_', 'X',
        and 'O'.

        :return: (str) The start state, 9 characters long.
        """
        while True:
            start_state = input('Enter cells: ').strip()

            if len(start_state) != 9:
                print('Invalid start state: 9 characters required.')
            elif any([c not in ['_', 'X', 'O'] for c in start_state]):
                print("Invalid start state: restrict input to '_', 'X', 'O'")
            else:
                break

        return start_state

    @staticmethod
    def move_is_on_board(coords: tuple):
        """
        Checks to see that the given coordinates are on the board (i.e. between
        1 and 3).

        :param coords: (tuple of 2 ints) Cell coordinates
        :return: (bool) True if the coordinates are both between 1 and 3,
            False otherwise
        """
        x, y = coords
        return (0 < x < 4) and (0 < y < 4)


if __name__ == '__main__':
    game = TicTacToe()
    game.run()
