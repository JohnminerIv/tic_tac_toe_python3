"""
Tic Tac Toe - Modified from http://inventwithpython.com/chapter10.html
John Miner's interpretation of a tic tak toe codebase.
"""
import random


class Board:
    """
    Board keeps track of the state of the tic tak toe board. It returns
    imformation about open positions and whether or not someone has won.
    """
    LARGEST_BOARD_SIZE = 26
    LETTERS = ["a ", "b ", "c ", "d ", "e ", "f ", "g ", "h ", "i ", "j ", "k ", "l ",
               "m ", "n ", "o ", "p ", "q ", "r ", "s ", "t ", "u ", "v ", "w ", "x ", "y ", "z "]
    NUMBERS = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "10", "11", "12",
               "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]

    def __init__(self, size=3):
        if self.is_valid_board_size(size) is False:
            raise ValueError("Invalid board size")
        self.size = size
        self.positions = dict()
        self.letters = self.LETTERS[:self.size]
        self.numbers = self.NUMBERS[:self.size]
        for letter in self.letters:
            for number in self.numbers:
                self.positions[letter + number] = '  '

    @staticmethod
    def is_valid_board_size(board_size):
        """
        Returns true if board_size is valid.
        """
        if not isinstance(board_size, int):
            return False
        if board_size < 3 or board_size > Board.LARGEST_BOARD_SIZE:
            return False
        return True

    def draw(self):
        """
        Prints a representation of the board.
        """
        # 5 is the number of characters per box add one for the header column
        sepreator_line = "-" * (len(self.letters) + 1) * 5 + "-"
        print(sepreator_line)
        print(
            "|    " + "".join([f"| {letter} " for letter in self.letters]) + "|")
        print(sepreator_line)
        for number in self.numbers:
            print(f"| {number} " + "".join(
                [f"| {self.positions[letter + number]} " for letter in self.letters]) + "|")
            print(sepreator_line)

    def is_board_full(self):
        """
        Returns True if every space on the board has been taken.
        Otherwise return False.
        """
        for position in self.positions:
            if self.is_position_availible(position):
                return False
        return True

    def make_move(self, move, letter):
        """
        Updates the board with a new move
        """
        self.positions[move] = letter

    def is_position_availible(self, position):
        """
        Returns true if the given position is empty
        """
        return self.positions[position] == '  '

    def is_winner(self, given_letter):
        """
        Returns True if the give_letter has won.
        """
        if self.check_diagonal_1(given_letter)[0] == self.size or \
                self.check_diagonal_2(given_letter)[0] == self.size:
            return True
        for number in self.numbers:
            if self.check_row(number, given_letter)[0] == self.size:
                return True
        for letter in self.letters:
            if self.check_column(letter, given_letter)[0] == self.size:
                return True
        return False

    def check_row(self, number, given_letter):
        """
        Returns how many of a given letter there are in a given row as well as
        the availible spaces.
        """
        count = 0
        avalible_pos = []
        for letter in self.letters:
            if self.positions[letter + number] == given_letter:
                count += 1
            else:
                avalible_pos.append(letter + number)
        return count, avalible_pos

    def check_column(self, letter, given_letter):
        """
        Returns how many of a given letter there are in a given column as well
        as the availible spaces.
        """
        count = 0
        avalible_pos = []
        for number in self.numbers:
            if self.positions[letter + number] == given_letter:
                count += 1
            else:
                avalible_pos.append(letter + number)
        return count, avalible_pos

    def check_diagonal_1(self, given_letter):
        """
        Returns how many of a given letter there are in diagonal 1 row as well
        as the availible spaces.
        """
        count = 0
        avalible_pos = []
        for i in range(self.size):
            if self.positions[self.letters[i] + self.numbers[i]] == given_letter:
                count += 1
            else:
                avalible_pos.append(self.letters[i] + self.numbers[i])
        return count, avalible_pos

    def check_diagonal_2(self, given_letter):
        """
        Returns how many of a given letter there are in diagonal 2 as well as
        the availible spaces.
        """
        count = 0
        avalible_pos = []
        for i in range(self.size):
            if self.positions[self.letters[self.size - 1 - i] + self.numbers[i]] == given_letter:
                count += 1
            else:
                avalible_pos.append(
                    self.letters[self.size - 1 - i] + self.numbers[i])
        return count, avalible_pos


class NPC:
    """
    NPC keeps track of the npc's letter and decides the next moves for for the
    computer.
    """

    def __init__(self, letter, opponent):
        self.letter = letter
        self.opponent_letter = opponent

    def choose_random_move_from_list(self, board, moves_list):
        """
        Returns a valid move from the passed list on the passed board.
        Returns None if there is no valid move.
        """
        possible_moves = []
        for move in moves_list:
            if board.is_position_availible(move):
                possible_moves.append(move)
        if len(possible_moves) > 0:
            return random.choice(possible_moves)
        return None

    def get_move(self, board):
        """
        Determines where the computer should move and return that move.
        """
        # First, check if we can win in the next move
        winning_move = self.get_winning_move(board, self.letter)
        if winning_move is not None:
            return winning_move
        # Check if the player could win on their next move, and block them.
        blocking_move = self.get_winning_move(board, self.opponent_letter)
        if blocking_move is not None:
            return blocking_move
        # Try to take one of the corners, if they are free.
        corner_move = self.move_in_a_corner(board)
        if corner_move is not None:
            return corner_move
        # Try to take the center, if it is free.
        if board.size % 2 == 1:
            if board.is_position_availible(board.letters[board.size // 2]
                                           + board.numbers[board.size // 2]):
                return board.letters[board.size // 2] + board.numbers[board.size // 2]
        # Move on one of the sides.
        return self.choose_random_move_from_list(board, list(board.positions.keys()))

    def get_winning_move(self, board, given_letter):
        """
        Finds a winning move if it exists for a given a board and a letter
        """
        diagonal_1 = board.check_diagonal_1(given_letter)
        if diagonal_1[0] == board.size - 1:
            if board.is_position_availible(diagonal_1[1][0]):
                return diagonal_1[1][0]

        diagonal_2 = board.check_diagonal_2(given_letter)
        if diagonal_2[0] == board.size - 1:
            if board.is_position_availible(diagonal_2[1][0]):
                return diagonal_2[1][0]

        for number in board.numbers:
            row = board.check_row(number, given_letter)
            if row[0] == board.size - 1:
                if board.is_position_availible(row[1][0]):
                    return row[1][0]

        for letter in board.letters:
            column = board.check_column(letter, given_letter)
            if column[0] == board.size - 1:
                if board.is_position_availible(column[1][0]):
                    return column[1][0]
        return None

    def move_in_a_corner(self, board):
        """
        Chooses a corner position if possible
        """
        return self.choose_random_move_from_list(board, [
            board.letters[0] + board.numbers[0],
            board.letters[0] + board.numbers[board.size - 1],
            board.letters[board.size - 1] + board.numbers[0],
            board.letters[board.size - 1] + board.numbers[board.size - 1]])


class GameState:
    """
    Game state tracks the game state, the board, and the game loop.
    """

    def __init__(self):
        self.board = Board(request_board_size())
        self.player_letter = request_player_letter()
        if self.player_letter == "X ":
            self.npc = NPC("O ", self.player_letter)
        else:
            self.npc = NPC("X ", self.player_letter)
        self.is_active = True

    def who_goes_first(self):
        """
        Randomly choose the player who goes first.
        """
        if random.randint(0, 1) == 0:
            return 'computer'
        return 'player'

    def start_gameloop(self):
        """
        Runs the main loop for the program.
        """
        print("Game Loop starting...")
        while True:
            current_turn = self.who_goes_first()
            print('The ' + current_turn + ' will go first.')
            while self.is_active:
                if current_turn == "player":
                    self.board.draw()
                    move = get_player_move(
                        self.board.positions, self.board.is_position_availible)
                    self.board.make_move(move, self.player_letter)
                    current_turn = "computer"
                else:
                    move = self.npc.get_move(self.board)
                    self.board.make_move(move, self.npc.letter)
                    current_turn = "player"
                if self.board.is_winner(self.player_letter):
                    self.board.draw()
                    print("You won!")
                    self.is_active = False
                if self.board.is_winner(self.npc.letter):
                    self.board.draw()
                    print("You lost!")
                    self.is_active = False
                if self.board.is_board_full():
                    self.board.draw()
                    print("Tie")
                    self.is_active = False
            if request_play_again() is False:
                break
            self.is_active = True
            self.board = Board(request_board_size())


def request_player_letter():
    """
    Lets the player type which letter they want to be.
    Returns a list with the player’s letter as the first item, and the
    computer's letter as the second.
    """
    letter = ''
    while letter in ('X', 'O') == False:
        print('Do you want to be X or O?')
        letter = input().upper()
    if letter == 'X':
        return 'X '
    return 'O '


def request_board_size():
    """
    Requests the user to input the size of the board they would like to play on.
    """
    board_size = 0
    while Board.is_valid_board_size(board_size) is False:
        print("Enter a board size.")
        try:
            board_size = int(input())
        except ValueError:
            pass
    return board_size


def request_play_again():
    """
    Promts the user to play again.
    """
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def get_player_move(board_positions, is_position_availible):
    """
    Promts the player for a move.
    """
    player_input = None
    move = None
    while move not in board_positions.keys() or is_position_availible(move) is False:
        print("What is your next move? Input in the form letter + number Ex. a3")
        player_input = input().lower()
        letter = player_input[0] + " "
        number = player_input[1:]
        if len(number) < 2:
            number = number + " "
        move = letter + number
    return move


if __name__ == '__main__':
    print('Welcome to Tic Tac Toe!')
    game_state = GameState()
    game_state.start_gameloop()