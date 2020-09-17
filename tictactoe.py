from Board import Board
from Player import Human, AI


class InvalidTokenError(Exception):
    """To be raised when a token other than 'X' or 'O' is passed/used."""
    def __init__(self, token):
        self.message = f"{token} is not a valid token. Valid tokens are 'X' " \
                       f"and 'O'."
        super().__init__(self.message)


class InvalidPlayerTypeError(Exception):
    """
    To be raised when an invalid player type is selected. (user/difficulty)
    """
    def __init__(self, player_type: str):
        self.message = f"{player_type} is not a valid player type. Please" \
                       f" choose 'user' or a valid difficulty."
        super().__init__(self.message)


class TicTacToe:
    """
    The main application for the Tic-Tac-Toe with AI game!
    """
    def __init__(self):
        self.board = Board()
        self.player1 = None  # X
        self.player2 = None  # O
        self.players = tuple()

    def run(self):
        """User-facing method for starting the application loop."""
        while True:
            exit_or_nah = self.menu()

            if exit_or_nah is None:
                self.board.state = '_________'
                self.play()
            else:
                break

    def menu(self):
        """
        Enters a menu loop. User can start a game or exit.

        :return: 'exit' (str) if the user wants to quit the application, None
            otherwise.
        """
        while True:
            action = input('Input command: ').strip()

            if action.startswith('start'):
                commands = action.split()
                if len(commands) != 3:  # start input must have 3 commands
                    print('Bad parameters!')
                else:
                    players = tuple(commands[1:])  # extract player types
                    try:
                        self.create_players(players[0], players[1])
                        return None
                    except InvalidPlayerTypeError as e:
                        print(e.message)

            elif action == 'exit':
                return action

            else:
                print('Bad parameters!')

    def create_players(self, player_type1: str, player_type2: str):
        """
        Instantiates the player objects and assigns them to the appropriate
        instance attributes.

        :param player_type1: Type of player1 - user, easy, medium
        :param player_type2: Type of player2
        """
        difficulties = ['easy', 'medium']

        if player_type1 == 'user':
            self.player1 = Human('X')
        elif player_type1 in difficulties:
            self.player1 = AI('X', player_type1)
        else:
            raise InvalidPlayerTypeError(player_type1)

        if player_type2 == 'user':
            self.player2 = Human('O')
        elif player_type2 in difficulties:
            self.player2 = AI('O', player_type2)
        else:
            raise InvalidPlayerTypeError(player_type2)

        self.players = (self.player1, self.player2)

    def play(self):
        """Call this to play the game."""
        print(self.board)

        player_toggle = 0  # controls who is the current player

        # MAIN GAME LOOP
        game_state = self.determine_game_state()
        while game_state == 'Game not finished':
            current_player = self.players[player_toggle]

            if type(current_player) is Human:
                self.do_user_move(current_player)
            elif type(current_player) is AI:
                self.do_computer_move(current_player)

            print(self.board)

            game_state = self.determine_game_state()
            player_toggle = (player_toggle + 1) % 2  # switch to the other player

        print(game_state + '\n')

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
        print(f'Making move level "{player.difficulty}"')

        move = player.calculate_move(self.board)
        if not self.is_open_cell(move):
            print(move)
            raise Exception()

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

    def determine_game_state(self):
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
