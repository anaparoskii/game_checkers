class Checkers(object):
    def __init__(self):
        self.matrix = [[], [], [], [], [], [], [], []]
        self.my_pieces = 12
        self.opponent_pieces = 12
        self.my_turn = True
        self.mandatory_jump = False

        for row in self.matrix:
            for i in range(8):
                row.append("---")
        self.position_opponent()
        self.position_player()

    def position_opponent(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.matrix[i][j] = " O "

    def position_player(self):
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.matrix[i][j] = " X "

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

    def play(self):
        self.print_matrix()


if __name__ == "__main__":
    checkers = Checkers()
    checkers.play()
