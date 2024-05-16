from math import inf
from time import time
from copy import deepcopy

ANSI_BLACK = "\u001b[30m"
ANSI_RED = "\u001b[31m"
ANSI_MAGENTA = "\u001b[35m"
ANSI_CYAN = "\u001b[36m"
ANSI_WHITE = "\u001b[37m"
ANSI_RESET = "\u001b[0m"


class Node(object):
    def __init__(self, board, move=None, value=None, parent=None):
        self.board = board
        self.value = value
        self.parent = parent
        self.move = move

    def get_children(self, mandatory_jump, player_turn):
        current_state = deepcopy(self.board)
        children = []
        available_moves = Checkers.find_available_moves(current_state, mandatory_jump, player_turn)
        for i in range(len(available_moves)):
            state = deepcopy(current_state)
            Checkers.make_a_move(state, available_moves[i])
            # if len(children) != 0:
            #     if Checkers.heuristic(state) < Checkers.heuristic(children[i-1].get_board()):
            #         continue
            #     children.append(Node(state, available_moves[i]))
            # else:
            #     children.append(Node(state, available_moves[i]))
            children.append(Node(state, available_moves[i]))
        return children

    def get_board(self):
        return self.board

    def get_value(self):
        return self.value

    def get_parent(self):
        return self.parent

    def get_move(self):
        return self.move


class Checkers(object):
    def __init__(self):
        self.matrix = [[], [], [], [], [], [], [], []]
        self.player_pieces = 12
        self.computer_pieces = 12
        self.player_turn = True
        self.mandatory_jump = False

        for row in self.matrix:
            for i in range(8):
                row.append("---")
        self.position_computer()
        self.position_player()

    def position_computer(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.matrix[i][j] = "b" + str(i) + str(j)

    def position_player(self):
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.matrix[i][j] = "a" + str(i) + str(j)

    @staticmethod
    def print_matrix(board, player_turn):
        k = 0
        print()
        for row in board:
            print(k, end="  |")
            k += 1
            for elem in row:
                if elem != "---" and Checkers.is_movable(board, int(elem[1]), int(elem[2]), player_turn):
                    print(ANSI_CYAN + elem + ANSI_RESET, end=" ")
                else:
                    print(elem, end=" ")
            print()
        for i in range(8):
            if i == 0:
                print("     0", end="   ")
            else:
                print(i, end="   ")
        print("\n")

    @staticmethod
    def is_movable(board, m, n, player_turn):
        if player_turn:
            letter = "a"
            if board[m][n][0].lower() != letter:
                return False
            if m - 1 < 0 or n - 1 < 0:
                return False
            if board[m-1][n-1] == "---":
                return True
            if n + 1 > 7:
                return False
            if board[m-1][n+1] == "---":
                return True
            if m - 2 < 0 or n - 2 < 0:
                return False
            if board[m-2][n-2] == "---" and board[m-1][n-1][0].lower() == "b":
                return True
            if n + 2 > 7:
                return False
            if board[m-2][n+2] == "---" and board[m-1][n+1][0].lower() == "b":
                return True
            if board[m][n][0] == "A":
                if m + 1 < 0:
                    return False
                if board[m + 1][n - 1] == "---" or board[m + 1][n + 1] == "---":
                    return True
                if m + 2 < 0:
                    return False
                if (board[m + 2][n - 2] == "---" and board[m + 1][n - 1][0].lower() == "b"
                        or board[m + 2][n + 2] == "---" and board[m + 1][n + 1][0].lower() == "b"):
                    return True
                return False
            return False
        return False

    def computer_move(self):
        t1 = time()
        current_state = Node(self.matrix)
        available_moves = current_state.get_children(self.mandatory_jump, False)
        if len(available_moves) == 0:
            print(ANSI_CYAN + "Computer has no moves available! YOU WIN!" + ANSI_RESET)
            exit()
        elif len(available_moves) == 1:
            depth = 0
        elif len(available_moves) >= 7:
            depth = 3
        else:
            depth = 5
        dictionary = {}
        for i in range(len(available_moves)):
            child = available_moves[i]
            value = Checkers.minimax(child.get_board(), -inf, inf, depth, False, self.mandatory_jump)
            dictionary[value] = child
        new_board = dictionary[max(dictionary.keys())].get_board()
        self.matrix = new_board
        t2 = time()
        time_taken = t2 - t1
        move = dictionary[max(dictionary.keys())].get_move()
        print("Computer moved ", move[0], " from ", move[1], move[2], " to ", move[3], move[4])
        if abs(move[1] - move[3]) == 2:
            self.player_pieces -= 1
        print("The move took %.6f seconds" % time_taken)

    def player_move(self):
        available_moves = Checkers.find_available_moves(self.matrix, self.mandatory_jump, self.player_turn)
        if len(available_moves) == 0:
            print(ANSI_RED + "No moves available! YOU LOSE!" + ANSI_RESET)
            exit()
        for i in range(len(available_moves)):
            print(i, ": move ", available_moves[i][0], " from ", available_moves[i][1], available_moves[i][2],
                  " to ", available_moves[i][3], available_moves[i][4])
        while True:
            choice = input("Choose a move: ")
            if choice == "":
                print(ANSI_MAGENTA + "Game ended!" + ANSI_RESET)
                exit()
            elif choice.lower() == "s":
                while True:
                    choice = input("Are you sure you want to surrender? [Y/N]: ")
                    if choice.lower() == "y":
                        print(ANSI_RED + "You surrendered! Coward move..." + ANSI_RESET)
                        exit()
                    elif choice.lower() == "n":
                        break
                    else:
                        print("Invalid choice! Please try again.")
            elif choice.isdigit():
                choice = int(choice)
                if 0 <= choice < len(available_moves):
                    break
                else:
                    print("Invalid choice! Please try again.")
        move = available_moves[choice]
        Checkers.make_a_move(self.matrix, move)
        if abs(move[1] - move[3]) == 2:
            self.computer_pieces -= 1

    @staticmethod
    def find_available_moves(board, mandatory_jump, player_turn):
        if player_turn:
            letter = "a"
        else:
            letter = "b"
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if (player_turn and board[m][n][0].lower() == "a") or (not player_turn and board[m][n][0] == "B"):
                    if Checkers.check_moves(board, letter, m, n, m-1, n+1):
                        available_moves.append([board[m][n], m, n, m-1, n+1])
                    if Checkers.check_moves(board, letter, m, n, m-1, n-1):
                        available_moves.append([board[m][n], m, n, m-1, n-1])
                    if Checkers.check_jumps(board, letter, m, n, m-1, n+1, m-2, n+2):
                        available_jumps.append([board[m][n], m, n, m-2, n+2])
                    if Checkers.check_jumps(board, letter, m, n, m-1, n-1, m-2, n-2):
                        available_jumps.append([board[m][n], m, n, m-2, n-2])
                if (player_turn and board[m][n][0] == "A") or (not player_turn and board[m][n][0].lower() == "b"):
                    if Checkers.check_moves(board, letter, m, n, m+1, n-1):
                        available_moves.append([board[m][n], m, n, m+1, n-1])
                    if Checkers.check_moves(board, letter, m, n, m+1, n+1):
                        available_moves.append([board[m][n], m, n, m+1, n+1])
                    if Checkers.check_jumps(board, letter, m, n, m+1, n-1, m+2, n-2):
                        available_jumps.append([board[m][n], m, n, m+2, n-2])
                    if Checkers.check_jumps(board, letter, m, n, m+1, n+1, m+2, n+2):
                        available_jumps.append([board[m][n], m, n, m+2, n+2])
        if mandatory_jump is False:
            available_moves += available_jumps
            return available_moves
        else:
            if len(available_jumps) == 0:
                return available_moves
            return available_jumps

    @staticmethod
    def check_moves(board, letter, m, n, new_m, new_n):
        if new_m < 0 or new_m > 7 or new_n < 0 or new_n > 7:
            return False
        if board[m][n][0].lower() != letter:
            return False
        if board[new_m][new_n] != "---":
            return False
        return True

    @staticmethod
    def check_jumps(board, letter, m, n, by_m, by_n, new_m, new_n):
        if letter.lower() == "a":
            opponent_letter = "b"
        else:
            opponent_letter = "a"
        if new_m < 0 or new_m > 7 or new_n < 0 or new_n > 7:
            return False
        if board[m][n][0].lower() != letter:
            return False
        if board[by_m][by_n][0].lower() != opponent_letter:
            return False
        if board[new_m][new_n] != "---":
            return False
        return True

    @staticmethod
    def make_a_move(board, move):
        letter = board[move[1]][move[2]][0]
        if letter == "a" and move[3] == 0:
            letter = "A"
        elif letter == "b" and move[3] == 7:
            letter = "B"
        board[move[3]][move[4]] = letter + move[0][1] + move[0][2]
        if abs(move[1] - move[3]) == 2:
            board[(move[1] + move[3]) // 2][(move[2] + move[4]) // 2] = "---"
        board[move[1]][move[2]] = "---"

    def play(self):
        print(ANSI_MAGENTA + "Welcome to Checkers!" + ANSI_RESET)
        print("""
        First, a few rules:
        1. You can quit the game at any moment by pressing ENTER
        2. You can surrender the game at any moment by pressing 's'
        """)
        while True:
            choice = input("Is jumping mandatory? [Y/N]: ")
            if choice.lower() == "y":
                self.mandatory_jump = True
                break
            elif choice.lower() == "n":
                self.mandatory_jump = False
                break
            elif choice == "":
                print(ANSI_MAGENTA + "Game ended!" + ANSI_RESET)
                exit()
            elif choice.lower() == "s":
                while True:
                    choice = input("Are you sure you want to surrender? [Y/N]: ")
                    if choice.lower() == "y":
                        print(ANSI_RED + "You surrendered before the game even started!" + ANSI_RESET)
                        exit()
                    elif choice.lower() == "n":
                        break
                    else:
                        print("Invalid choice! Please try again.")
            else:
                print("Invalid choice! Please try again.")
        while True:
            Checkers.print_matrix(self.matrix, self.player_turn)
            if self.player_turn:
                print(ANSI_MAGENTA + "Player's turn!" + ANSI_RESET)
                self.player_move()
            else:
                print(ANSI_MAGENTA + "Computer's turn!" + ANSI_RESET)
                print("Thinking...")
                self.computer_move()
            if self.player_pieces == 0:
                print(ANSI_RED + "You have no pieces left! YOU LOSE!" + ANSI_RESET)
                exit()
            elif self.computer_pieces == 0:
                print(ANSI_CYAN + "Computer has no pieces left! YOU WIN!" + ANSI_RESET)
                exit()
            self.player_turn = not self.player_turn

    @staticmethod
    def minimax(board, alfa, beta, depth, maximizing_player, mandatory_jump):
        if depth == 0:
            return Checkers.heuristic(board)
        current_state = Node(board)
        if maximizing_player:
            max_eval = -inf
            for child in current_state.get_children(mandatory_jump, True):
                ev = Checkers.minimax(child.get_board(), alfa, beta, depth - 1, False, mandatory_jump)
                max_eval = max(max_eval, ev)
                alfa = max(alfa, ev)
                if beta <= alfa:
                    break
            return max_eval
        else:
            min_eval = inf
            for child in current_state.get_children(mandatory_jump, False):
                ev = Checkers.minimax(child.get_board(), alfa, beta, depth - 1, True, mandatory_jump)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alfa:
                    break
            return min_eval

    @staticmethod
    def heuristic(board):
        result = 0
        computer = 0
        opponent = 0
        for i in range(8):
            for j in range(8):
                if board[i][j][0].lower() == "a":
                    opponent += 1
                else:
                    computer += 1
                    if board[i][j][0] == "b":
                        result += 5
                    if board[i][j][0] == "B":
                        result += 10
                    if i == 0 or i == 7 or j == 0 or j == 7:
                        result += 10
                    if i + 1 > 7 or j + 1 > 7 or i - 1 < 0 or j - 1 < 0:
                        continue
                    if i + 2 > 7 or j + 2 > 7 or i - 2 < 0 or j - 2 < 0:
                        continue
                    if ((board[i][j][0] == "B" and board[i-1][j-1][0].lower() == "a" and board[i-2][j-2] == "---")
                            or (board[i-1][j+1][0].lower() == "a" and board[i-2][j+2] == "---")):
                        result += 5
                    if ((board[i+1][j-1][0].lower() == "a" and board[i-1][j+1] == "---")
                            or (board[i+1][j+1][0].lower() == "a" and board[i-1][j-1] == "---")):
                        result -= 3
                    if ((board[i-1][j-1][0] == "A" and board[i+1][j+1] == "---")
                            or (board[i-1][j+1][0] == "A" and board[i+1][j-1] == "---")):
                        result -= 3
                    if (board[i+1][j+1][0].lower() == "b" or board[i+1][j-1][0].lower() == "b"
                            or board[i-1][j+1][0].lower() == "b" or board[i-1][j-1][0].lower() == "b"):
                        result += 8
        return result + (computer - opponent) * 100


if __name__ == "__main__":
    checkers = Checkers()
    checkers.play()
