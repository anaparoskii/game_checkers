from math import inf

ansi_black = "\u001b[30m"
ansi_red = "\u001b[31m"
ansi_magenta = "\u001b[35m"
ansi_cyan = "\u001b[36m"
ansi_white = "\u001b[37m"
ansi_reset = "\u001b[0m"


class Node(object):
    def __init__(self, board, move=None, value=None, parent=None):
        self.board = board
        self.value = value
        self.parent = parent
        self.move = move

    def get_children(self, mandatory_jump, player_turn):
        copy_board = self.board
        current_state = copy_board
        children = []
        available_moves = Checkers.find_available_moves(current_state, mandatory_jump, player_turn)
        for i in range(len(available_moves)):
            copy_state = current_state
            state = copy_state
            Checkers.make_a_move(state, available_moves[i])
            if len(children) != 0:
                if Checkers.heuristic(state) < Checkers.heuristic(children[i-1].get_board()):
                    continue
                children.append(Node(state, available_moves[i]))
            else:
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

    def print_matrix(self):
        k = 0
        print()
        for row in self.matrix:
            print(k, end="  |")
            k += 1
            for elem in row:
                print(elem, end=" ")
            print()
        for i in range(8):
            if i == 0:
                print("     0", end="   ")
            else:
                print(i, end="   ")
        print("\n")

    def computer_move(self):
        current_state = Node(self.matrix)
        available_moves = current_state.get_children(self.mandatory_jump, False)
        if len(available_moves) == 0:
            print(ansi_cyan + "Computer has no moves available! YOU WIN!" + ansi_reset)
            exit()
        dictionary = {}
        for i in range(len(available_moves)):
            child = available_moves[i]
            value = Checkers.minimax(child.get_board(), -inf, inf, 4, False, self.mandatory_jump)
            dictionary[value] = child
        new_board = dictionary[max(dictionary.keys())].get_board()
        self.matrix = new_board

    def player_move(self):
        available_moves = Checkers.find_available_moves(self.matrix, self.mandatory_jump, self.player_turn)
        if len(available_moves) == 0:
            print(ansi_red + "No moves available! YOU LOSE!" + ansi_reset)
            exit()
        for i in range(len(available_moves)):
            print(i, ": move ", available_moves[i][0], " from ", available_moves[i][1], available_moves[i][2],
                  " to ", available_moves[i][3], available_moves[i][4])
        while True:
            choice = input("Choose a move: ")
            if choice == "":
                print(ansi_magenta + "Game ended!" + ansi_reset)
                exit()
            elif choice.lower() == "s":
                print(ansi_red + "You surrendered! Coward..." + ansi_reset)
                exit()
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
                if (player_turn and board[m][n][0].lower() == "a") or board[m][n][0] == "B":
                    if Checkers.check_moves(board, letter, m, n, m-1, n+1):
                        available_moves.append([board[m][n], m, n, m-1, n+1])
                    if Checkers.check_moves(board, letter, m, n, m-1, n-1):
                        available_moves.append([board[m][n], m, n, m-1, n-1])
                    if Checkers.check_jumps(board, letter, m, n, m-1, n+1, m-2, n+2):
                        available_jumps.append([board[m][n], m, n, m-2, n+2])
                    if Checkers.check_jumps(board, letter, m, n, m-1, n-1, m-2, n-2):
                        available_jumps.append([board[m][n], m, n, m-2, n-2])
                if (player_turn and board[m][n][0] == "A") or board[m][n][0].lower() == "b":
                    if Checkers.check_moves(board, letter, m, n, m+1, n-1):
                        available_moves.append([board[m][n], m, n, m+1, n-1])
                    if Checkers.check_moves(board, letter, m, n, m+1, n+1):
                        available_moves.append([board[m][n], m, n, m+1, n+1])
                    if Checkers.check_jumps(board, letter, m, n, m+1, n-1, m+2, n-2):
                        available_jumps.append([board[m][n], m, n, m+2, n-2])
                    if Checkers.check_jumps(board, letter, m, n, m+1, n+1, m+2, n+2):
                        available_jumps.append([board[m][n], m, n, m+2, n+2])
        if mandatory_jump is False:
            available_moves.extend(available_jumps)
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
        if board[new_m][new_n][0] != "---":
            return False
        return True

    @staticmethod
    def make_a_move(board, move):
        letter = board[move[1]][move[2]][0]
        if letter == "a" and move[3] == 0:
            letter = "A"
        elif letter == "b" and move[3] == 7:
            letter = "B"
        board[move[3]][move[4]] = letter + str(move[1]) + str(move[2])
        if abs(move[1] - move[3]) == 2:
            board[(move[1] + move[3]) // 2][(move[2] + move[4]) // 2] = "---"
        else:
            board[move[1]][move[2]] = "---"

    def play(self):
        print(ansi_magenta + "Welcome to Checkers!" + ansi_reset)
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
                print(ansi_magenta + "Game ended!" + ansi_reset)
                exit()
            elif choice.lower() == "s":
                print(ansi_red + "You surrendered! Coward..." + ansi_reset)
                exit()
            else:
                print("Invalid choice! Please try again.")
        while True:
            self.print_matrix()
            if self.player_turn:
                print(ansi_magenta + "Player's turn!" + ansi_reset)
                self.player_move()
            else:
                print(ansi_magenta + "Computer's turn!" + ansi_reset)
                print("Thinking...")
                self.computer_move()
            if self.player_pieces == 0:
                print(ansi_red + "You have no pieces left! YOU LOSE!" + ansi_reset)
                exit()
            elif self.computer_pieces == 0:
                print(ansi_cyan + "Computer has no pieces left! YOU WIN!" + ansi_reset)
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
                ev = Checkers.minimax(child, alfa, beta, depth - 1, False, mandatory_jump)
                max_eval = max(max_eval, ev)
                alfa = max(alfa, ev)
                if beta <= alfa:
                    break
            return max_eval
        else:
            min_eval = inf
            for child in current_state.get_children(mandatory_jump, False):
                ev = Checkers.minimax(child, alfa, beta, depth - 1, True, mandatory_jump)
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
                        result += 8
                    if i+1 > 7 or j+1 > 7 or i - 1 < 0 or j - 1 < 0:
                        continue
                    if ((board[i+1][j-1][0].lower() == "a" and board[i-1][j+1] == "---")
                            or (board[i+1][j+1][0].lower() == "a" and board[i-1][j-1] == "---")):
                        result -= 3
                    if ((board[i-1][j-1][0] == "A" and board[i+1][j+1] == "---")
                            or (board[i-1][j+1][0] == "A" and board[i+1][j-1] == "---")):
                        result -= 3
                    if (board[i+1][j+1][0].lower() == "b" or board[i+1][j-1][0].lower() == "b"
                            or board[i-1][j+1][0].lower() == "b" or board[i-1][j-1][0].lower() == "b"):
                        result += 6
        return result + (computer - opponent) * 100


if __name__ == "__main__":
    checkers = Checkers()
    checkers.play()
