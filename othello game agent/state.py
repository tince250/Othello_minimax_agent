from hashmap import LinearHashMap

colors = {
    "B": '\u26AA',
    "W": '\u26AB',
    "\x1b[94mA\x1b[0m": '\x1b[94m\u25CC\x1b[0m'
}

all_directions = {
            "N": (-1, 0),
            "NE": (-1, 1),
            "E": (0, 1),
            "SE": (1, 1),
            "S": (1, 0),
            "SW": (1, -1),
            "W": (0, -1),
            "NW": (-1, -1)
            }

class State(object):

    __slots__ = "_board", "num"

    def __init__(self):
        self._board = []
        for i in range(8):
            self._board.append(8*['-'])
        self._board[3][3] = self._board[4][4] = "W"
        self._board[3][4] = self._board[4][3] = "B"

        self.num = {"B": 2, "W": 2}

    @property
    def board(self):
        return self._board

    def get_value(self, i , j):
        return self._board[i][j]

    def set_value(self, i, j, value):
        self._board[i][j] = value
        self.num[value] += 1

        #Fliping the other player's peices in all 8 directions
        for direction in all_directions.keys():
            ni, nj = self.move(direction, i, j)
            if not self.is_outside_board(ni, nj):
                if self._board[ni][nj] == self.oposite_player(value):
                    possible_flips = [(ni, nj)]
                    while True:
                        ni, nj = self.move(direction, ni, nj)
                        if self.is_outside_board(ni, nj) or self._board[ni][nj] == '-':
                            break
                        if self._board[ni][nj] == value:
                            for piece in possible_flips:
                                self._board[piece[0]][piece[1]] = value
                            self.num[value] += len(possible_flips)
                            self.num[self.oposite_player(value)] -= len(possible_flips)
                            break
                        possible_flips.append((ni, nj))



    def move(self, direction, i, j):
        return i + all_directions[direction][0], j + all_directions[direction][1]

    def is_outside_board(self, i, j):
        if 0<=i<=7 and 0<=j<=7:
            return False
        return True

    def oposite_player(self, current_player):
        if current_player == "B":
            return "W"
        return "B"

    def copy_state(self):
        new_state = State()
        new_state._board = self.copy_board()
        new_state.num["B"] = self.num["B"]
        new_state.num["W"] = self.num["W"]
        return new_state

    def copy_board(self):
        new_board = []
        for i in range(8):
            new_board.append([])
            for j in range(8):
                new_board[i].append(self._board[i][j])

        return new_board



    def available_moves_board(self, available_moves):
        board_copy = self.copy_board()
        for move in available_moves:
            board_copy[move[0]][move[1]] = "\033[94mA\033[0m"
        return board_copy



    def available_moves(self, current_player):
        """
        Returns a list of possible positions the player can place the piece to
        :param current_player:
        :param i:
        :param j:
        :return:
        """
        available_moves = []

        for i in range(8):
            for j in range(8):
                if self._board[i][j] == current_player:
                    for direction in all_directions.keys():
                        ni, nj = self.move(direction, i, j)
                        if not self.is_outside_board(ni, nj) and self.board[ni][nj] == self.oposite_player(current_player):
                            while True:
                                ni, nj = self.move(direction, ni, nj)
                                if self.is_outside_board(ni, nj):
                                    break
                                else:
                                    if self._board[ni][nj] == '-':
                                        if (ni, nj) not in available_moves:
                                            available_moves.append((ni, nj))
                                        break
                                    if self._board[ni][nj] == current_player:
                                        break

        return available_moves

    def is_move_valid(self, i, j, value):
        value = value.upper()
        if value not in ("B", "W"):
            return False

        if not (0<=i<=7) or not (0<=j<=7):
            return False

        if self._board[i][j] != '-':
            print("ovde", self._board[i][j])
            return False

        if (i, j) not in self.available_moves(value):
            return False

        return True

    def has_legal_moves(self, player):
        return len(self.available_moves(player)) > 0

    def is_end(self):
        """
        The game end when the whole board is filled with pieces or neither player has legal moves left.
        :return:
        """

        if self.num["W"] + self.num["B"] == 64 or not (self.has_legal_moves("B") or self.has_legal_moves("W")):
            if self.num["W"] > self.num["B"]:
                winner = "W"
            elif self.num["W"] < self.num["B"]:
                winner = "B"
            else:
                winner = "tie"

            return True, winner

        return False, None

    def print_score(self):
        ret = "---------------------------------"
        ret += "\n\033[1mSCORE:   B:" + str(self.num["B"]) + "   W:" + str(self.num["W"]) + "\033[0m\n"
        ret += "---------------------------------"
        print(ret)

    def print_board(self, board):
        ret = "   %d   %d   %d   %d   %d   %d   %d   %d \n" % (0,1,2,3,4,5,6,7)
        self.print_score()
        for i in range(8):
            ret += str(i) + ""
            for j in range(8):
                if board[i][j] == '-':
                    ret += "   |"
                else:
                    ret += " %s |" % colors[board[i][j]]
            ret += "\n ---------------------------------\n"
        print(ret, end='')

    def __str__(self):
        ret =''
        self.print_score()
        for i in range(8):
            ret += str(i) + "|"
            for j in range(8):
                if self._board[i][j] == '-':
                    ret += "   |"
                else:
                    ret += " %s |" % colors[self._board[i][j]]
            ret += "\n---------------------------------\n"
        return ret

