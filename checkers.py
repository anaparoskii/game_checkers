from math import inf
from time import time
from copy import deepcopy


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
                    self.matrix[i][j] = "w" + str(i) + str(j)

    @staticmethod
    def print_matrix(board, player_turn, mandatory_jump):
        available_moves = []
        if player_turn:
            available_moves = Checkers.find_available_moves(board, mandatory_jump, True)
        k = 0
        print()
        for i in range(8):
            if i == 0:
                print("     0", end="   ")
            else:
                print(i, end="   ")
        print()
        for row in board:
            print(k, end="  |")
            k += 1
            j = 0
            for elem in row:
                j += 1
                if player_turn and Checkers.is_movable(board, k - 1, j - 1, available_moves):
                    print(ANSI_BLUE + elem + ANSI_RESET, end=" ")
                else:
                    print(elem, end=" ")
            print("| ", k - 1)
        for i in range(8):
            if i == 0:
                print("     0", end="   ")
            else:
                print(i, end="   ")
        print("\n")

    @staticmethod
    def print_second_matrix(board, moves, pawn):
        k = 0
        print()
        for i in range(8):
            if i == 0:
                print("     0", end="   ")
            else:
                print(i, end="   ")
        print()
        for row in board:
            print(k, end="  |")
            k += 1
            j = 0
            for elem in row:
                j += 1
                if pawn in elem:
                    print(ANSI_BLUE + elem + ANSI_RESET, end=" ")
                else:
                    for move in moves:
                        if move[3] == k - 1 and move[4] == j - 1:
                            print(ANSI_BACK + str(k - 1) + str(j - 1) + ANSI_RESET, end="  ")
                            break
                    else:
                        print(elem, end=" ")
            print("| ", k - 1)
        for i in range(8):
            if i == 0:
                print("     0", end="   ")
            else:
                print(i, end="   ")
        print("\n")

    @staticmethod
    def is_movable(board, m, n, available_moves):
        for move in available_moves:
            if board[m][n] == move[0]:
                return True
        return False

    def computer_move(self):
        t1 = time()
        current_state = Node(self.matrix)
        available_moves = current_state.get_children(self.mandatory_jump, False)
        if len(available_moves) == 0:
            print(ANSI_GREEN + "Computer has no moves available! YOU WIN!" + ANSI_RESET)
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
        move_chart[self.matrix] = new_board
        self.matrix = new_board
        t2 = time()
        time_taken = t2 - t1
        move = dictionary[max(dictionary.keys())].get_move()
        print("Computer moved ", move[0], " from ", move[1], move[2], " to ", move[3], move[4])
        if abs(move[1] - move[3]) == 2:
            self.player_pieces -= 1
            print(ANSI_BOLD + "Computer took your pawn!" + ANSI_RESET)
        print("The move took %.6f seconds" % time_taken)

    def player_move(self):
        available_moves = Checkers.find_available_moves(self.matrix, self.mandatory_jump, self.player_turn)
        if len(available_moves) == 0:
            print(ANSI_RED + "No moves available! YOU LOSE!" + ANSI_RESET)
            exit()
        pawn = Checkers.choose_pawn(self.matrix, available_moves)
        move = Checkers.choose_move(self.matrix, available_moves, self.player_turn, self.mandatory_jump)
        for moves in available_moves:
            if pawn in moves[0] and move == str(moves[3]) + str(moves[4]):
                Checkers.make_a_move(self.matrix, moves)
                if Checkers.is_jump(available_moves, move, pawn):
                    self.computer_pieces -= 1
                    while True:
                        jump = Checkers.double_jump(self.matrix, moves, self.player_turn, self.mandatory_jump)
                        if jump:
                            Checkers.make_a_move(self.matrix, jump)
                            self.computer_pieces -= 1
                            continue
                        break
                break

    @staticmethod
    def double_jump(board, move, player_turn, mandatory_jump):
        available_jumps = []
        if Checkers.check_jumps(board, "w", move[3], move[4], move[3]-1, move[4]-1, move[3]-2, move[4]-2):
            available_jumps.append([board[move[3]][move[4]], move[3], move[4], move[3]-2, move[4]-2])
        if Checkers.check_jumps(board, "w", move[3], move[4], move[3]-1, move[4]+1, move[3]-2, move[4]+2):
            available_jumps.append([board[move[3]][move[4]], move[3], move[4], move[3]-2, move[4]+2])
        if board[move[3]][move[4]][0] == "W":
            if Checkers.check_jumps(board, "w", move[3], move[4], move[3]+1, move[4]-1, move[3]+2, move[4]-2):
                available_jumps.append([board[move[3]][move[4]], move[3], move[4], move[3]+2, move[4]-2])
            if Checkers.check_jumps(board, "w", move[3], move[4], move[3]+1, move[4]+1, move[3]+2, move[4]+2):
                available_jumps.append([board[move[3]][move[4]], move[3], move[4], move[3]+2, move[4]+2])
        if len(available_jumps) == 0:
            return False
        state = deepcopy(board)
        Checkers.print_second_matrix(state, available_jumps, str(move[3]) + str(move[4]))
        while True:
            choice = input("Do you want to make another jump? [Y/N]: ")
            if choice.lower() == "y":
                break
            elif choice.lower() == "n":
                return False
            elif choice == "":
                print(ANSI_YELLOW + "Game ended!" + ANSI_RESET)
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
                        print(ANSI_BOLD + "Invalid choice! Please try again." + ANSI_RESET)
            else:
                print(ANSI_BOLD + "Invalid choice! Please try again." + ANSI_RESET)
        pawn = str(move[3]) + str(move[4])
        jump = Checkers.choose_move(board, available_jumps, player_turn, mandatory_jump)
        for moves in available_jumps:
            if pawn == str(moves[1]) + str(moves[2]) and jump == str(moves[3]) + str(moves[4]):
                return moves

    @staticmethod
    def is_jump(available_moves, move, pawn):
        for moves in available_moves:
            if pawn in moves[0] and move == str(moves[3]) + str(moves[4]):
                if abs(moves[1] - moves[3]) == 2:
                    return True
                return False

    @staticmethod
    def choose_pawn(board, available_moves):
        while True:
            pawn = input("Choose a pawn you want to move [format [row column] no spaces]: ")
            if pawn == "":
                print(ANSI_YELLOW + "Game ended!" + ANSI_RESET)
                exit()
            elif pawn.lower() == "s":
                while True:
                    choice = input("Are you sure you want to surrender? [Y/N]: ")
                    if choice.lower() == "y":
                        print(ANSI_RED + "You surrendered! Coward move..." + ANSI_RESET)
                        exit()
                    elif choice.lower() == "n":
                        break
                    else:
                        print(ANSI_BOLD + "Invalid choice! Please try again." + ANSI_RESET)
            else:
                for moves in available_moves:
                    if pawn in moves[0]:
                        break
                else:
                    print(ANSI_BOLD + "Invalid choice! Please try again." + ANSI_RESET)
                break
        new_board = deepcopy(board)
        pawn_moves = []
        for moves in available_moves:
            if pawn in moves[0]:
                pawn_moves.append(moves)
        Checkers.print_second_matrix(new_board, pawn_moves, pawn)
        return pawn

    @staticmethod
    def choose_move(board, available_moves, player_turn, mandatory_jump):
        while True:
            while True:
                move = input("Choose a move [format [row column] no spaces] [x to choose another pawn]: ")
                if (move == "" or move.lower() == "s" or move.lower() == "x"
                        or (len(move) == 2 and move[0].isdigit() and move[1].isdigit())):
                    break
                print(ANSI_BOLD + "Invalid choice! Please try again." + ANSI_RESET)
            if move == "":
                print(ANSI_YELLOW + "Game ended!" + ANSI_RESET)
                exit()
            elif move.lower() == "s":
                while True:
                    choice = input("Are you sure you want to surrender? [Y/N]: ")
                    if choice.lower() == "y":
                        print(ANSI_RED + "You surrendered! Coward move..." + ANSI_RESET)
                        exit()
                    elif choice.lower() == "n":
                        break
                    else:
                        print(ANSI_BOLD + "Invalid choice! Please try again." + ANSI_RESET)
            elif move.lower() == "x":
                Checkers.print_matrix(board, player_turn, mandatory_jump)
                continue
            else:
                for moves in available_moves:
                    if move == str(moves[3]) + str(moves[4]):
                        break
                else:
                    print(ANSI_BOLD + "Invalid choice! Please try again." + ANSI_RESET)
                break
        return move

    @staticmethod
    def find_available_moves(board, mandatory_jump, player_turn):
        if player_turn:
            letter = "w"
        else:
            letter = "b"
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if (player_turn and board[m][n][0].lower() == "w") or (not player_turn and board[m][n][0] == "B"):
                    if Checkers.check_moves(board, letter, m, n, m-1, n+1):
                        available_moves.append([board[m][n], m, n, m-1, n+1])
                    if Checkers.check_moves(board, letter, m, n, m-1, n-1):
                        available_moves.append([board[m][n], m, n, m-1, n-1])
                    if Checkers.check_jumps(board, letter, m, n, m-1, n+1, m-2, n+2):
                        available_jumps.append([board[m][n], m, n, m-2, n+2])
                    if Checkers.check_jumps(board, letter, m, n, m-1, n-1, m-2, n-2):
                        available_jumps.append([board[m][n], m, n, m-2, n-2])
                if (player_turn and board[m][n][0] == "W") or (not player_turn and board[m][n][0].lower() == "b"):
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
        if letter.lower() == "w":
            opponent_letter = "b"
        else:
            opponent_letter = "w"
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
        if letter == "w" and move[3] == 0:
            letter = "W"
        elif letter == "b" and move[3] == 7:
            letter = "B"
        board[move[3]][move[4]] = letter + move[0][1] + move[0][2]
        if abs(move[1] - move[3]) == 2:
            board[(move[1] + move[3]) // 2][(move[2] + move[4]) // 2] = "---"
        board[move[1]][move[2]] = "---"

    def play(self):
        print(ANSI_PURPLE + "Welcome to Checkers!" + ANSI_RESET)
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
                print(ANSI_YELLOW + "Game ended!" + ANSI_RESET)
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
                        print(ANSI_BOLD + "Invalid choice! Please try again." + ANSI_RESET)
            else:
                print(ANSI_BOLD + "Invalid choice! Please try again." + ANSI_RESET)
        while True:
            Checkers.print_matrix(self.matrix, self.player_turn, self.mandatory_jump)
            print("MY PIECES: %d\tCOMPUTER'S PIECES: %d" % (self.player_pieces, self.computer_pieces))
            if self.player_turn:
                print(ANSI_PURPLE + "Player's turn!" + ANSI_RESET)
                self.player_move()
            else:
                print(ANSI_PURPLE + "Computer's turn!" + ANSI_RESET)
                print("Thinking...")
                self.computer_move()
            if self.player_pieces == 0:
                print(ANSI_RED + "You have no pieces left! YOU LOSE!" + ANSI_RESET)
                exit()
            elif self.computer_pieces == 0:
                print(ANSI_GREEN + "Computer has no pieces left! YOU WIN!" + ANSI_RESET)
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
                if board[i][j][0].lower() == "w":
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
                    if ((board[i][j][0] == "B" and board[i-1][j-1][0].lower() == "w" and board[i-2][j-2] == "---")
                            or (board[i-1][j+1][0].lower() == "w" and board[i-2][j+2] == "---")):
                        result += 5
                    if ((board[i+1][j-1][0].lower() == "w" and board[i-1][j+1] == "---")
                            or (board[i+1][j+1][0].lower() == "w" and board[i-1][j-1] == "---")):
                        result -= 3
                    if ((board[i-1][j-1][0] == "W" and board[i+1][j+1] == "---")
                            or (board[i-1][j+1][0] == "W" and board[i+1][j-1] == "---")):
                        result -= 3
                    if (board[i+1][j+1][0].lower() == "b" or board[i+1][j-1][0].lower() == "b"
                            or board[i-1][j+1][0].lower() == "b" or board[i-1][j-1][0].lower() == "b"):
                        result += 8
        return result + (computer - opponent) * 100


if __name__ == "__main__":
    ANSI_BLACK = "\u001b[30m"
    ANSI_RED = "\u001b[1;31m"
    ANSI_WHITE = "\u001b[37m"
    ANSI_RESET = "\u001b[0m"
    ANSI_GREEN = "\033[1;32m"
    ANSI_YELLOW = "\033[1;33m"
    ANSI_PURPLE = "\033[1;35m"
    ANSI_BOLD = "\033[1m"
    ANSI_BLUE = "\033[1;36m"
    ANSI_BACK = "\u001b[45;1m"

    move_chart = {}

    checkers = Checkers()
    checkers.play()
