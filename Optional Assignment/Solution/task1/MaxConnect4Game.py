# !/usr/bin/env python

import copy
import random
import sys

utility_value = {}
score_list = []
infinity = float('inf')
class MaxConnect4game:
    def __init__(self):
        self.gameboard = [[0 for i in range(7)] for j in range(6)]
        self.current_move = 0
        self.piece_count = 0
        self.player1Score = 0
        self.player2Score = 0
        self.gameFile = None
        self.computer_column = None
        self.depth = 1

    def checkPieceCount(self):
        self.piece_count = sum(1 for row in self.gameboard for piece in row if piece)

    def getPieceCount(self):
        return sum(1 for row in self.gameboard for piece in row if piece)

    def print_gameboard(self):
        print(' -------------------')
        for i in range(6):
            print(),
            for j in range(7):
                print('%d' % int(self.gameboard[i][j]), end=' ')
            print()
        print(' -------------------')

    def PrintingGameBoardToFile(self):
        for row in self.gameboard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r')
        self.gameFile.write('%s\r' % str(self.current_move))


    def alpha_beta(self, current_node, alpha, beta, depth):
        value = -infinity
        child_nodes = self.maximum_value(current_node)
        if child_nodes == [] or depth == 0:
            get_score(self, self.gameboard)
            return self.evaluation_calculation(self.gameboard)
        else:
            for node in child_nodes:
                self.gameBoard = copy.deepcopy(node)
                value = max(value, self.beta_alpha(node, alpha, beta, depth - 1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

    def beta_alpha(self, current_node, alpha, beta, depth):
        value = infinity
        child_nodes = self.minimum_value(current_node)
        if child_nodes == [] or depth == 0:
            get_score(self, self.gameboard)
            return self.evaluation_calculation(self.gameboard)
        else:
            for node in child_nodes:
                self.gameboard = copy.deepcopy(node)
                value = min(value, self.alpha_beta(node, alpha, beta, depth - 1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
        return value


    def minmax(self, depth):
        current_state = copy.deepcopy(self.gameboard)
        for i in range(7):
            if self.playPiece(i) != None:
                if self.piece_count == 42 or self.depth == 0:
                    self.gameboard = copy.deepcopy(current_state)
                    return i
                else:
                    val = self.beta_alpha(self.gameboard, -infinity, infinity, depth - 1)

                    utility_value[i] = val
                    self.gameboard = copy.deepcopy(current_state)

        max_uvalue = max([i for i in utility_value.values()])
        for i in range(7):
            if i in utility_value:
                if utility_value[i] == max_uvalue:
                    utility_value.clear()
                    return i

    def minimum_value(self, current_node):
        main_node = copy.deepcopy(current_node)
        if self.current_move == 1:
            opponent = 2
        elif self.current_move == 2:
            opponent = 1
        child_nodes = []
        for i in range(7):
            current_state = self.check_piece(i, opponent)
            if current_state != None:
                child_nodes.append(self.gameboard)
                self.gameboard = copy.deepcopy(main_node)
        return child_nodes

    def maximum_value(self, current_node):
        main_node = copy.deepcopy(current_node)
        child_nodes = []
        for i in range(7):
            current_state = self.playPiece(i)
            if current_state != None:
                child_nodes.append(self.gameboard)
                self.gameboard = copy.deepcopy(main_node)
        return child_nodes


    def evaluation_function(self):
        if self.current_move == 1:
            color = 2

        elif self.current_move == 2:
            color = 1
        return color

    def count_playerevaluation(self, state):
        player_fours = self.Calc_Streak(state, self.current_move, 4)
        player_threes = self.Calc_Streak(state, self.current_move, 3)
        player_twos = self.Calc_Streak(state, self.current_move, 2)

        return (player_fours * 37044 + player_threes * 882 + player_twos * 21)

    def calc_compeval(self, state):
        color = self.evaluation_function()
        comp_fours = self.Calc_Streak(state, color, 4)
        comp_threes = self.Calc_Streak(state, color, 3)
        comp_twos = self.Calc_Streak(state, color, 2)
        return (comp_fours * 37044 + comp_threes * 882 + comp_twos * 21)

    def evaluation_calculation(self, state):
        self.count_playerevaluation(state)
        self.calc_compeval(state)
        return self.count_playerevaluation(state) - self.calc_compeval(state)

    # Choose where to keep current player's choice
    def playPiece(self, column):
        if not self.gameboard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameboard[i][column]:
                    self.gameboard[i][column] = self.current_move
                    self.piece_count += 1
                    return 1

    def aiPlay(self):
        random_column = self.minmax(int(self.depth))
        result = self.playPiece(random_column)
        if not result:
            print('No Result')
        else:
            print('Player: %d, Column: %d\n' % (self.current_move, random_column + 1))
            self.change_move()

    def change_move(self):
        if self.current_move == 1:
            self.current_move = 2
        elif self.current_move == 2:
            self.current_move = 1

    def Calc_Streak(self, state, color, streak):
        count = 0
        for i in range(6):
            for j in range(7):
                if state[i][j] == color:
                    count += self.verticalCheck(i, j, state, streak)
                    count += self.horizontalCheck(i, j, state, streak)
                    count += self.diagonalCheck(i, j, state, streak)
        return count

    def verticalCheck(self, row, column, state, streak):
        consecutiveCount = 0
        for i in range(row, 6):
            if state[i][column] == state[row][column]:
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def horizontalCheck(self, row, column, state, streak):
        count = 0
        for j in range(column, 7):
            if state[row][j] == state[row][column]:
                count += 1
            else:
                break
        if count >= streak:
            return 1
        else:
            return 0

    def diagonalCheck(self, row, column, state, streak):
        total = 0
        count = 0
        j = column
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        count = 0
        j = column
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        return total

    def check_piece(self, column, opponent):
        if not self.gameboard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameboard[i][column]:
                    self.gameboard[i][column] = opponent
                    self.piece_count += 1
                    return 1

    def count_score(self):
        self.player1Score = 0;
        self.player2Score = 0;
        # Check horizontally
        for row in self.gameboard:
            # Check player 1
            if row[0:4] == [1] * 4:
                self.player1Score += 1
            if row[1:5] == [1] * 4:
                self.player1Score += 1
            if row[2:6] == [1] * 4:
                self.player1Score += 1
            if row[3:7] == [1] * 4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2] * 4:
                self.player2Score += 1
            if row[1:5] == [2] * 4:
                self.player2Score += 1
            if row[2:6] == [2] * 4:
                self.player2Score += 1
            if row[3:7] == [2] * 4:
                self.player2Score += 1

        # validate vertically
        for j in range(7):
            # for the player 1
            if (self.gameboard[0][j] == 1 and self.gameboard[1][j] == 1 and
                    self.gameboard[2][j] == 1 and self.gameboard[3][j] == 1):
                self.player1Score += 1
            if (self.gameboard[1][j] == 1 and self.gameboard[2][j] == 1 and
                    self.gameboard[3][j] == 1 and self.gameboard[4][j] == 1):
                self.player1Score += 1
            if (self.gameboard[2][j] == 1 and self.gameboard[3][j] == 1 and
                    self.gameboard[4][j] == 1 and self.gameboard[5][j] == 1):
                self.player1Score += 1
            # for the player 2
            if (self.gameboard[0][j] == 2 and self.gameboard[1][j] == 2 and
                    self.gameboard[2][j] == 2 and self.gameboard[3][j] == 2):
                self.player2Score += 1
            if (self.gameboard[1][j] == 2 and self.gameboard[2][j] == 2 and
                    self.gameboard[3][j] == 2 and self.gameboard[4][j] == 2):
                self.player2Score += 1
            if (self.gameboard[2][j] == 2 and self.gameboard[3][j] == 2 and
                    self.gameboard[4][j] == 2 and self.gameboard[5][j] == 2):
                self.player2Score += 1
        # Check diagonally

        # player's 1
        if (self.gameboard[2][0] == 1 and self.gameboard[3][1] == 1 and
                self.gameboard[4][2] == 1 and self.gameboard[5][3] == 1):
            self.player1Score += 1
        if (self.gameboard[1][0] == 1 and self.gameboard[2][1] == 1 and
                self.gameboard[3][2] == 1 and self.gameboard[4][3] == 1):
            self.player1Score += 1
        if (self.gameboard[2][1] == 1 and self.gameboard[3][2] == 1 and
                self.gameboard[4][3] == 1 and self.gameboard[5][4] == 1):
            self.player1Score += 1
        if (self.gameboard[0][0] == 1 and self.gameboard[1][1] == 1 and
                self.gameboard[2][2] == 1 and self.gameboard[3][3] == 1):
            self.player1Score += 1
        if (self.gameboard[1][1] == 1 and self.gameboard[2][2] == 1 and
                self.gameboard[3][3] == 1 and self.gameboard[4][4] == 1):
            self.player1Score += 1
        if (self.gameboard[2][2] == 1 and self.gameboard[3][3] == 1 and
                self.gameboard[4][4] == 1 and self.gameboard[5][5] == 1):
            self.player1Score += 1
        if (self.gameboard[0][1] == 1 and self.gameboard[1][2] == 1 and
                self.gameboard[2][3] == 1 and self.gameboard[3][4] == 1):
            self.player1Score += 1
        if (self.gameboard[1][2] == 1 and self.gameboard[2][3] == 1 and
                self.gameboard[3][4] == 1 and self.gameboard[4][5] == 1):
            self.player1Score += 1
        if (self.gameboard[2][3] == 1 and self.gameboard[3][4] == 1 and
                self.gameboard[4][5] == 1 and self.gameboard[5][6] == 1):
            self.player1Score += 1
        if (self.gameboard[0][2] == 1 and self.gameboard[1][3] == 1 and
                self.gameboard[2][4] == 1 and self.gameboard[3][5] == 1):
            self.player1Score += 1
        if (self.gameboard[1][3] == 1 and self.gameboard[2][4] == 1 and
                self.gameboard[3][5] == 1 and self.gameboard[4][6] == 1):
            self.player1Score += 1
        if (self.gameboard[0][3] == 1 and self.gameboard[1][4] == 1 and
                self.gameboard[2][5] == 1 and self.gameboard[3][6] == 1):
            self.player1Score += 1

        if (self.gameboard[0][3] == 1 and self.gameboard[1][2] == 1 and
                self.gameboard[2][1] == 1 and self.gameboard[3][0] == 1):
            self.player1Score += 1
        if (self.gameboard[0][4] == 1 and self.gameboard[1][3] == 1 and
                self.gameboard[2][2] == 1 and self.gameboard[3][1] == 1):
            self.player1Score += 1
        if (self.gameboard[1][3] == 1 and self.gameboard[2][2] == 1 and
                self.gameboard[3][1] == 1 and self.gameboard[4][0] == 1):
            self.player1Score += 1
        if (self.gameboard[0][5] == 1 and self.gameboard[1][4] == 1 and
                self.gameboard[2][3] == 1 and self.gameboard[3][2] == 1):
            self.player1Score += 1
        if (self.gameboard[1][4] == 1 and self.gameboard[2][3] == 1 and
                self.gameboard[3][2] == 1 and self.gameboard[4][1] == 1):
            self.player1Score += 1
        if (self.gameboard[2][3] == 1 and self.gameboard[3][2] == 1 and
                self.gameboard[4][1] == 1 and self.gameboard[5][0] == 1):
            self.player1Score += 1
        if (self.gameboard[0][6] == 1 and self.gameboard[1][5] == 1 and
                self.gameboard[2][4] == 1 and self.gameboard[3][3] == 1):
            self.player1Score += 1
        if (self.gameboard[1][5] == 1 and self.gameboard[2][4] == 1 and
                self.gameboard[3][3] == 1 and self.gameboard[4][2] == 1):
            self.player1Score += 1
        if (self.gameboard[2][4] == 1 and self.gameboard[3][3] == 1 and
                self.gameboard[4][2] == 1 and self.gameboard[5][1] == 1):
            self.player1Score += 1
        if (self.gameboard[1][6] == 1 and self.gameboard[2][5] == 1 and
                self.gameboard[3][4] == 1 and self.gameboard[4][3] == 1):
            self.player1Score += 1
        if (self.gameboard[2][5] == 1 and self.gameboard[3][4] == 1 and
                self.gameboard[4][3] == 1 and self.gameboard[5][2] == 1):
            self.player1Score += 1
        if (self.gameboard[2][6] == 1 and self.gameboard[3][5] == 1 and
                self.gameboard[4][4] == 1 and self.gameboard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameboard[2][0] == 2 and self.gameboard[3][1] == 2 and
                self.gameboard[4][2] == 2 and self.gameboard[5][3] == 2):
            self.player2Score += 1
        if (self.gameboard[1][0] == 2 and self.gameboard[2][1] == 2 and
                self.gameboard[3][2] == 2 and self.gameboard[4][3] == 2):
            self.player2Score += 1
        if (self.gameboard[2][1] == 2 and self.gameboard[3][2] == 2 and
                self.gameboard[4][3] == 2 and self.gameboard[5][4] == 2):
            self.player2Score += 1
        if (self.gameboard[0][0] == 2 and self.gameboard[1][1] == 2 and
                self.gameboard[2][2] == 2 and self.gameboard[3][3] == 2):
            self.player2Score += 1
        if (self.gameboard[1][1] == 2 and self.gameboard[2][2] == 2 and
                self.gameboard[3][3] == 2 and self.gameboard[4][4] == 2):
            self.player2Score += 1
        if (self.gameboard[2][2] == 2 and self.gameboard[3][3] == 2 and
                self.gameboard[4][4] == 2 and self.gameboard[5][5] == 2):
            self.player2Score += 1
        if (self.gameboard[0][1] == 2 and self.gameboard[1][2] == 2 and
                self.gameboard[2][3] == 2 and self.gameboard[3][4] == 2):
            self.player2Score += 1
        if (self.gameboard[1][2] == 2 and self.gameboard[2][3] == 2 and
                self.gameboard[3][4] == 2 and self.gameboard[4][5] == 2):
            self.player2Score += 1
        if (self.gameboard[2][3] == 2 and self.gameboard[3][4] == 2 and
                self.gameboard[4][5] == 2 and self.gameboard[5][6] == 2):
            self.player2Score += 1
        if (self.gameboard[0][2] == 2 and self.gameboard[1][3] == 2 and
                self.gameboard[2][4] == 2 and self.gameboard[3][5] == 2):
            self.player2Score += 1
        if (self.gameboard[1][3] == 2 and self.gameboard[2][4] == 2 and
                self.gameboard[3][5] == 2 and self.gameboard[4][6] == 2):
            self.player2Score += 1
        if (self.gameboard[0][3] == 2 and self.gameboard[1][4] == 2 and
                self.gameboard[2][5] == 2 and self.gameboard[3][6] == 2):
            self.player2Score += 1

        if (self.gameboard[0][3] == 2 and self.gameboard[1][2] == 2 and
                self.gameboard[2][1] == 2 and self.gameboard[3][0] == 2):
            self.player2Score += 1
        if (self.gameboard[0][4] == 2 and self.gameboard[1][3] == 2 and
                self.gameboard[2][2] == 2 and self.gameboard[3][1] == 2):
            self.player2Score += 1
        if (self.gameboard[1][3] == 2 and self.gameboard[2][2] == 2 and
                self.gameboard[3][1] == 2 and self.gameboard[4][0] == 2):
            self.player2Score += 1
        if (self.gameboard[0][5] == 2 and self.gameboard[1][4] == 2 and
                self.gameboard[2][3] == 2 and self.gameboard[3][2] == 2):
            self.player2Score += 1
        if (self.gameboard[1][4] == 2 and self.gameboard[2][3] == 2 and
                self.gameboard[3][2] == 2 and self.gameboard[4][1] == 2):
            self.player2Score += 1
        if (self.gameboard[2][3] == 2 and self.gameboard[3][2] == 2 and
                self.gameboard[4][1] == 2 and self.gameboard[5][0] == 2):
            self.player2Score += 1
        if (self.gameboard[0][6] == 2 and self.gameboard[1][5] == 2 and
                self.gameboard[2][4] == 2 and self.gameboard[3][3] == 2):
            self.player2Score += 1
        if (self.gameboard[1][5] == 2 and self.gameboard[2][4] == 2 and
                self.gameboard[3][3] == 2 and self.gameboard[4][2] == 2):
            self.player2Score += 1
        if (self.gameboard[2][4] == 2 and self.gameboard[3][3] == 2 and
                self.gameboard[4][2] == 2 and self.gameboard[5][1] == 2):
            self.player2Score += 1
        if (self.gameboard[1][6] == 2 and self.gameboard[2][5] == 2 and
                self.gameboard[3][4] == 2 and self.gameboard[4][3] == 2):
            self.player2Score += 1
        if (self.gameboard[2][5] == 2 and self.gameboard[3][4] == 2 and
                self.gameboard[4][3] == 2 and self.gameboard[5][2] == 2):
            self.player2Score += 1
        if (self.gameboard[2][6] == 2 and self.gameboard[3][5] == 2 and
                self.gameboard[4][4] == 2 and self.gameboard[5][3] == 2):
            self.player2Score += 1


def get_score(self, state):
    self.player1Score = 0;
    self.player2Score = 0;

    # checking row wise
    for row in state:
        # Check player 1
        if row[0:4] == [1] * 4:
            self.player1Score += 1
        if row[1:5] == [1] * 4:
            self.player1Score += 1
        if row[2:6] == [1] * 4:
            self.player1Score += 1
        if row[3:7] == [1] * 4:
            self.player1Score += 1
        # Check player 2
        if row[0:4] == [2] * 4:
            self.player2Score += 1
        if row[1:5] == [2] * 4:
            self.player2Score += 1
        if row[2:6] == [2] * 4:
            self.player2Score += 1
        if row[3:7] == [2] * 4:
            self.player2Score += 1

    # Checking columns
    for j in range(7):
        # Check player 1
        if (self.gameboard[0][j] == 1 and self.gameboard[1][j] == 1 and
                self.gameboard[2][j] == 1 and self.gameboard[3][j] == 1):
            self.player1Score += 1
        if (self.gameboard[1][j] == 1 and self.gameboard[2][j] == 1 and
                self.gameboard[3][j] == 1 and self.gameboard[4][j] == 1):
            self.player1Score += 1
        if (self.gameboard[2][j] == 1 and self.gameboard[3][j] == 1 and
                self.gameboard[4][j] == 1 and self.gameboard[5][j] == 1):
            self.player1Score += 1
        # Check player 2
        if (self.gameboard[0][j] == 2 and self.gameboard[1][j] == 2 and
                self.gameboard[2][j] == 2 and self.gameboard[3][j] == 2):
            self.player2Score += 1
        if (self.gameboard[1][j] == 2 and self.gameboard[2][j] == 2 and
                self.gameboard[3][j] == 2 and self.gameboard[4][j] == 2):
            self.player2Score += 1
        if (self.gameboard[2][j] == 2 and self.gameboard[3][j] == 2 and
                self.gameboard[4][j] == 2 and self.gameboard[5][j] == 2):
            self.player2Score += 1

    # Check diagonally

    # Check player 1
    if (self.gameboard[2][0] == 1 and self.gameboard[3][1] == 1 and
            self.gameboard[4][2] == 1 and self.gameboard[5][3] == 1):
        self.player1Score += 1
    if (self.gameboard[1][0] == 1 and self.gameboard[2][1] == 1 and
            self.gameboard[3][2] == 1 and self.gameboard[4][3] == 1):
        self.player1Score += 1
    if (self.gameboard[2][1] == 1 and self.gameboard[3][2] == 1 and
            self.gameboard[4][3] == 1 and self.gameboard[5][4] == 1):
        self.player1Score += 1
    if (self.gameboard[0][0] == 1 and self.gameboard[1][1] == 1 and
            self.gameboard[2][2] == 1 and self.gameboard[3][3] == 1):
        self.player1Score += 1
    if (self.gameboard[1][1] == 1 and self.gameboard[2][2] == 1 and
            self.gameboard[3][3] == 1 and self.gameboard[4][4] == 1):
        self.player1Score += 1
    if (self.gameboard[2][2] == 1 and self.gameboard[3][3] == 1 and
            self.gameboard[4][4] == 1 and self.gameboard[5][5] == 1):
        self.player1Score += 1
    if (self.gameboard[0][1] == 1 and self.gameboard[1][2] == 1 and
            self.gameboard[2][3] == 1 and self.gameboard[3][4] == 1):
        self.player1Score += 1
    if (self.gameboard[1][2] == 1 and self.gameboard[2][3] == 1 and
            self.gameboard[3][4] == 1 and self.gameboard[4][5] == 1):
        self.player1Score += 1
    if (self.gameboard[2][3] == 1 and self.gameboard[3][4] == 1 and
            self.gameboard[4][5] == 1 and self.gameboard[5][6] == 1):
        self.player1Score += 1
    if (self.gameboard[0][2] == 1 and self.gameboard[1][3] == 1 and
            self.gameboard[2][4] == 1 and self.gameboard[3][5] == 1):
        self.player1Score += 1
    if (self.gameboard[1][3] == 1 and self.gameboard[2][4] == 1 and
            self.gameboard[3][5] == 1 and self.gameboard[4][6] == 1):
        self.player1Score += 1
    if (self.gameboard[0][3] == 1 and self.gameboard[1][4] == 1 and
            self.gameboard[2][5] == 1 and self.gameboard[3][6] == 1):
        self.player1Score += 1

    if (self.gameboard[0][3] == 1 and self.gameboard[1][2] == 1 and
            self.gameboard[2][1] == 1 and self.gameboard[3][0] == 1):
        self.player1Score += 1
    if (self.gameboard[0][4] == 1 and self.gameboard[1][3] == 1 and
            self.gameboard[2][2] == 1 and self.gameboard[3][1] == 1):
        self.player1Score += 1
    if (self.gameboard[1][3] == 1 and self.gameboard[2][2] == 1 and
            self.gameboard[3][1] == 1 and self.gameboard[4][0] == 1):
        self.player1Score += 1
    if (self.gameboard[0][5] == 1 and self.gameboard[1][4] == 1 and
            self.gameboard[2][3] == 1 and self.gameboard[3][2] == 1):
        self.player1Score += 1
    if (self.gameboard[1][4] == 1 and self.gameboard[2][3] == 1 and
            self.gameboard[3][2] == 1 and self.gameboard[4][1] == 1):
        self.player1Score += 1
    if (self.gameboard[2][3] == 1 and self.gameboard[3][2] == 1 and
            self.gameboard[4][1] == 1 and self.gameboard[5][0] == 1):
        self.player1Score += 1
    if (self.gameboard[0][6] == 1 and self.gameboard[1][5] == 1 and
            self.gameboard[2][4] == 1 and self.gameboard[3][3] == 1):
        self.player1Score += 1
    if (self.gameboard[1][5] == 1 and self.gameboard[2][4] == 1 and
            self.gameboard[3][3] == 1 and self.gameboard[4][2] == 1):
        self.player1Score += 1
    if (self.gameboard[2][4] == 1 and self.gameboard[3][3] == 1 and
            self.gameboard[4][2] == 1 and self.gameboard[5][1] == 1):
        self.player1Score += 1
    if (self.gameboard[1][6] == 1 and self.gameboard[2][5] == 1 and
            self.gameboard[3][4] == 1 and self.gameboard[4][3] == 1):
        self.player1Score += 1
    if (self.gameboard[2][5] == 1 and self.gameboard[3][4] == 1 and
            self.gameboard[4][3] == 1 and self.gameboard[5][2] == 1):
        self.player1Score += 1
    if (self.gameboard[2][6] == 1 and self.gameboard[3][5] == 1 and
            self.gameboard[4][4] == 1 and self.gameboard[5][3] == 1):
        self.player1Score += 1

    # Check player 2
    if (self.gameboard[2][0] == 2 and self.gameboard[3][1] == 2 and
            self.gameboard[4][2] == 2 and self.gameboard[5][3] == 2):
        self.player2Score += 1
    if (self.gameboard[1][0] == 2 and self.gameboard[2][1] == 2 and
            self.gameboard[3][2] == 2 and self.gameboard[4][3] == 2):
        self.player2Score += 1
    if (self.gameboard[2][1] == 2 and self.gameboard[3][2] == 2 and
            self.gameboard[4][3] == 2 and self.gameboard[5][4] == 2):
        self.player2Score += 1
    if (self.gameboard[0][0] == 2 and self.gameboard[1][1] == 2 and
            self.gameboard[2][2] == 2 and self.gameboard[3][3] == 2):
        self.player2Score += 1
    if (self.gameboard[1][1] == 2 and self.gameboard[2][2] == 2 and
            self.gameboard[3][3] == 2 and self.gameboard[4][4] == 2):
        self.player2Score += 1
    if (self.gameboard[2][2] == 2 and self.gameboard[3][3] == 2 and
            self.gameboard[4][4] == 2 and self.gameboard[5][5] == 2):
        self.player2Score += 1
    if (self.gameboard[0][1] == 2 and self.gameboard[1][2] == 2 and
            self.gameboard[2][3] == 2 and self.gameboard[3][4] == 2):
        self.player2Score += 1
    if (self.gameboard[1][2] == 2 and self.gameboard[2][3] == 2 and
            self.gameboard[3][4] == 2 and self.gameboard[4][5] == 2):
        self.player2Score += 1
    if (self.gameboard[2][3] == 2 and self.gameboard[3][4] == 2 and
            self.gameboard[4][5] == 2 and self.gameboard[5][6] == 2):
        self.player2Score += 1
    if (self.gameboard[0][2] == 2 and self.gameboard[1][3] == 2 and
            self.gameboard[2][4] == 2 and self.gameboard[3][5] == 2):
        self.player2Score += 1
    if (self.gameboard[1][3] == 2 and self.gameboard[2][4] == 2 and
            self.gameboard[3][5] == 2 and self.gameboard[4][6] == 2):
        self.player2Score += 1
    if (self.gameboard[0][3] == 2 and self.gameboard[1][4] == 2 and
            self.gameboard[2][5] == 2 and self.gameboard[3][6] == 2):
        self.player2Score += 1

    if (self.gameboard[0][3] == 2 and self.gameboard[1][2] == 2 and
            self.gameboard[2][1] == 2 and self.gameboard[3][0] == 2):
        self.player2Score += 1
    if (self.gameboard[0][4] == 2 and self.gameboard[1][3] == 2 and
            self.gameboard[2][2] == 2 and self.gameboard[3][1] == 2):
        self.player2Score += 1
    if (self.gameboard[1][3] == 2 and self.gameboard[2][2] == 2 and
            self.gameboard[3][1] == 2 and self.gameboard[4][0] == 2):
        self.player2Score += 1
    if (self.gameboard[0][5] == 2 and self.gameboard[1][4] == 2 and
            self.gameboard[2][3] == 2 and self.gameboard[3][2] == 2):
        self.player2Score += 1
    if (self.gameboard[1][4] == 2 and self.gameboard[2][3] == 2 and
            self.gameboard[3][2] == 2 and self.gameboard[4][1] == 2):
        self.player2Score += 1
    if (self.gameboard[2][3] == 2 and self.gameboard[3][2] == 2 and
            self.gameboard[4][1] == 2 and self.gameboard[5][0] == 2):
        self.player2Score += 1
    if (self.gameboard[0][6] == 2 and self.gameboard[1][5] == 2 and
            self.gameboard[2][4] == 2 and self.gameboard[3][3] == 2):
        self.player2Score += 1
    if (self.gameboard[1][5] == 2 and self.gameboard[2][4] == 2 and
            self.gameboard[3][3] == 2 and self.gameboard[4][2] == 2):
        self.player2Score += 1
    if (self.gameboard[2][4] == 2 and self.gameboard[3][3] == 2 and
            self.gameboard[4][2] == 2 and self.gameboard[5][1] == 2):
        self.player2Score += 1
    if (self.gameboard[1][6] == 2 and self.gameboard[2][5] == 2 and
            self.gameboard[3][4] == 2 and self.gameboard[4][3] == 2):
        self.player2Score += 1
    if (self.gameboard[2][5] == 2 and self.gameboard[3][4] == 2 and
            self.gameboard[4][3] == 2 and self.gameboard[5][2] == 2):
        self.player2Score += 1
    if (self.gameboard[2][6] == 2 and self.gameboard[3][5] == 2 and
            self.gameboard[4][4] == 2 and self.gameboard[5][3] == 2):
        self.player2Score += 1


