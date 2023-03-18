from state import State
from hashmap import LinearHashMap
import time

from heuristic import heuritistic

INF = 99999999999999
MINF = -99999999999999

class Game(object):

    __slots__ = ['_current_state', '_player_turn', '_game_tree', '_states_map']

    def __init__(self):
        self._current_state = None
        self._player_turn = "B"
        self._game_tree = None
        self._states_map = None
        self.initialize_game()

    def initialize_game(self):
        self._current_state = State()
        #self._game_tree = Tree(self._current_state)
        self._states_map = LinearHashMap()
        self._player_turn = "B"

    def heuristic(self, player, state, end):
        #implementirana heuristic from internet research
        my_tiles = opp_tiles = my_front_tiles = opp_front_tiles = 0
        p = c = l1 = m = f = d = 0
        my_color = "W"
        opp_color = "B"
        board = state.board

        if end:
            if self._current_state.num[my_color] > self._current_state.num[opp_color]:
                return INF
            elif self._current_state.num[my_color] < self._current_state.num[opp_color]:
                return MINF
            else:
                return 0

        X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
        Y1 = [0, 1, 1, 1, 0, -1, -1, -1]
        V = [[20, -3, 11, 8, 8, 11, -3, 20], [-3, -7, -4, 1, 1, -4, -7, -3], [11, -4, 2, 2, 2, 2, -4, 11], [8, 1, 2, -3, -3, 2, 1, 8], [8, 1, 2, -3, -3, 2, 1, 8], [11, -4, 2, 2, 2, 2, -4, 11], [-3, -7, -4, 1, 1, -4, -7, -3], [20, -3, 11, 8, 8, 11, -3, 20]]

        #Piece difference, frontier disks and disk squares
        for i in range(8):
            for j in range(8):
                if board[i][j] == my_color:
                    d += V[i][j]
                    my_tiles += 1
                elif board[i][j] == opp_color:
                    d -= V[i][j]
                    opp_tiles += 1

                if board[i][j] != '-':
                    for k in range(8):
                        x = i + X1[k]
                        y = j + Y1[k]
                        if not self._current_state.is_outside_board(x, y) and board[x][y] == '-':
                            if board[i][j] == my_color:
                                my_front_tiles += 1
                            else:
                                opp_front_tiles += 1
                            break
        if my_tiles > opp_tiles:
            p = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            p = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            p = 0

        if my_front_tiles > opp_front_tiles:
            f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles)
        elif my_front_tiles < opp_front_tiles:
            f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles)
        else:
            f = 0

        #Corner occupancy
        my_tiles = opp_tiles = 0
        if (board[0][0] == my_color):
            my_tiles += 1
        elif (board[0][0] == opp_color):
            opp_tiles += 1
        if (board[0][7] == my_color):
            my_tiles += 1
        elif (board[0][7] == opp_color):
            opp_tiles += 1
        if (board[7][0] == my_color):
            my_tiles += 1
        elif (board[7][0] == opp_color):
            opp_tiles += 1
        elif (board[7][7] == my_color):
            my_tiles += 1
        if (board[7][7] == opp_color):
            opp_tiles += 1
        c = 25 * (my_tiles - opp_tiles)

        #Corner closeness
        my_tiles = opp_tiles = 0
        if board[0][0] == '-':
            if (board[0][1] == my_color):
                my_tiles += 1
            if (board[0][1] == opp_color):
                opp_tiles += 1
            if (board[1][0] == my_color):
                my_tiles += 1
            if (board[1][0] == opp_color):
                opp_tiles += 1
            if (board[1][1] == my_color):
                my_tiles += 1
            if (board[1][1] == opp_color):
                opp_tiles += 1
        if board[0][7] == '-':
            if (board[0][6] == my_color):
                my_tiles += 1
            if (board[0][6] == opp_color):
                opp_tiles += 1
            if (board[1][7] == my_color):
                my_tiles += 1
            if (board[1][7] == opp_color):
                opp_tiles += 1
            if (board[1][6] == my_color):
                my_tiles += 1
            if (board[1][6] == opp_color):
                opp_tiles += 1
        if board[7][0] == '-':
            if (board[7][1] == my_color):
                my_tiles += 1
            if (board[7][1] == opp_color):
                opp_tiles += 1
            if (board[6][0] == my_color):
                my_tiles += 1
            if (board[6][0] == opp_color):
                opp_tiles += 1
            if (board[6][1] == my_color):
                my_tiles += 1
            if (board[6][1] == opp_color):
                opp_tiles += 1
        if board[7][7] == '-':
            if (board[6][7] == my_color):
                my_tiles += 1
            if (board[6][7] == opp_color):
                opp_tiles += 1
            if (board[6][6] == my_color):
                my_tiles += 1
            if (board[6][6] == opp_color):
                opp_tiles += 1
            if (board[7][6] == my_color):
                my_tiles += 1
            if (board[7][6] == opp_color):
                opp_tiles += 1
            l1 = -12.5 * (my_tiles - opp_tiles)

        #Mobility
        my_tiles = len(self._current_state.available_moves(my_color))
        opp_tiles = len(self._current_state.available_moves(opp_color))
        if my_tiles > opp_tiles:
            m = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            m = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            m = 0

        #final weighted score
        score = (10 * p) + (801.724 * c) + (382.026 * l1) + (78.922 * m) + (74.396 * f) + (10 * d)
        return score


    def max(self, depth, start_time, alpha, beta):

        maxv = MINF-1

        px = None
        py = None

        end, winner = self._current_state.is_end()

        if end or depth == 1:
            score = self.heuristic("W", self._current_state, end)
            return score, 0, 0

        legal_moves = self._current_state.available_moves("W")
        if len(legal_moves) > 0:
            for move in legal_moves:
                state_copy = self._current_state.copy_state()
                self._current_state.set_value(move[0], move[1], "W")
                if self._current_state.has_legal_moves("B"):
                    (opp_value, opp_x, opp_py) = self.min(depth - 1, start_time, alpha, beta)
                else:
                    (opp_value, opp_x, opp_py) = self.max(depth - 1, start_time, alpha, beta)
                if opp_value > maxv:

                    px = move[0]
                    py = move[1]
                    maxv = opp_value
                self._current_state = state_copy

                if maxv >= beta:
                    return maxv, px, py

                if maxv > alpha:
                    alpha = maxv

            # self._states_map[self._current_state] = maxv
            return maxv, px, py

        return False, 0, 0



    def min(self, depth, start_time, alpha, beta):

        minv = INF+1

        qx = None
        qy = None

        end, winner = self._current_state.is_end()

        if end or depth == 1:
            score = self.heuristic("W", self._current_state, end)
            print(score)
            return score, 0, 0

        legal_moves = self._current_state.available_moves("B")
        if len(legal_moves) > 0:
            for move in legal_moves:
                state_copy = self._current_state.copy_state()
                self._current_state.set_value(move[0], move[1], "B")
                if self._current_state.has_legal_moves("W"):
                    (opp_value, opp_x, opp_py) = self.max(depth - 1, start_time, alpha, beta)
                else:
                    (opp_value, opp_x, opp_py) = self.min(depth - 1, start_time, alpha, beta)
                if opp_value < minv:
                    qx = move[0]
                    qy = move[1]
                    minv = opp_value
                self._current_state = state_copy

                if minv <= alpha:
                    return minv, qx, qy

                if minv < beta:
                    beta = minv

            # self._states_map[self._current_state] = minv
            return minv, qx, qy
        return False, 0, 0

    def play(self):
        while True:
            result, winner = self._current_state.is_end()

            if result:
                print()
                if winner == "B":
                    print("Black wins!")
                elif winner == "W":
                    print("White wins!")
                else:
                    print("It's a tie!")
                self._current_state.print_score()
                print("\n")
                print(len(self._states_map))
                break

            else:

                if self._player_turn == "B":
                # AI plays
                    print("Black plays")
                    start_time = time.time()
                    (score, px, py) = self.min(3, start_time, -99999999999999, 99999999999999)
                    end_time = time.time()
                    print(self._current_state.available_moves("B"))
                    print('Evaluation time: {}s'.format(round(end_time - start_time, 7)))
                    print('Recommended move B: X = {}, Y = {}'.format(px, py))

                    if score is not False:
                        self._current_state.set_value(px, py, "B")

                    self._player_turn = "W"

                    # while True:
                    #
                    #     print("Black plays")
                    #     available_moves = self._current_state.available_moves("B")
                    #     if len(available_moves) != 0:
                    #         self._current_state.print_board(self._current_state.available_moves_board(available_moves))
                    #         print("\033[94mSuggested legal moves (blue on board): \033[0m", end="")
                    #         print(available_moves)
                    #
                    #         px = int(input("Enter the x coordinate: "))   #sredi da ti ne puca kad pritisnes enter
                    #         py = int(input("Enter the y coordinate: "))
                    #
                    #         if self._current_state.is_move_valid(px, py, "B"):
                    #             self._current_state.set_value(px, py, "B")
                    #             self._player_turn = "W"
                    #             break
                    #         else:
                    #             print("Move not valid, try again.")
                    #     else:
                    #         print("You have no legal moves left, it's other player's turn.")
                    #         self._player_turn = "W"
                    #         break

                else:
                    #AI plays
                    print("White plays")
                    start_time = time.time()
                    (score, qx, qy) = self.max(3, start_time, -99999999999999, 99999999999999)
                    end_time = time.time()
                    print('Evaluation time: {}s'.format(round(end_time - start_time, 7)))
                    available_moves = self._current_state.available_moves("W")
                    print("Available moves W:", available_moves)
                    print('Recommended move W: X = {}, Y = {}'.format(qx, qy))

                    if score is not False:
                        self._current_state.set_value(qx, qy, "W")
                        print(self._current_state)
                    self._player_turn = "B"

                    #Human plays
                    # while True:
                    #
                    #     available_moves = self._current_state.available_moves("W")
                    #     if len(available_moves) != 0:
                    #         self._current_state.print_board(self._current_state.available_moves_board(available_moves))
                    #         print("\033[94mSuggested legal moves (blue on board): \033[0m", end="")
                    #         print(available_moves)
                    #
                    #         px = int(input("Enter the x coordinate: "))
                    #         py = int(input("Enter the y coordinate: "))
                    #
                    #         if self._current_state.is_move_valid(px, py, "W"):
                    #             self._current_state.set_value(px, py, "W")
                    #             self._player_turn = "B"
                    #             break
                    #         else:
                    #             print("Move not valid, try again.")
                    #     else:
                    #         print("You have no legal moves left, it's other player's turn.")



