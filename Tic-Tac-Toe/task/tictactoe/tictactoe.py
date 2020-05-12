class TicTacToe:

    @staticmethod
    def checked_numbers(f_list, diapason_lower_limit, diapason_upper_limit):
        digits_as_str = [str(x) for x in range(diapason_lower_limit, diapason_upper_limit)]
        for item in f_list:
            if item not in digits_as_str:
                return False
        return True

    def __init__(self, i_dimension, i_players_list, i_placeholder):
        self.dimension = i_dimension
        self.players_list = i_players_list
        self.placeholder = i_placeholder
        self.init_string = self.placeholder * self.dimension ** 2
        self.game_matrix = self.get_init_matrix()
        self.state = 'init'
        self.another_player = False

    def change_state(self, state_string):
        self.state = state_string

    def change_player(self):
        self.another_player = not self.another_player

    def run(self):
        while True:
            if self.state == 'init':
                print(self.get_game_representation())
                self.change_state('game on')

            if self.state == 'game on':
                self.process_plays_move()
                print(self.get_game_representation())
                self.change_player()
                self.change_state('checking result')
            if self.state == 'checking result':
                if self.check_impossible():
                    break
                if self.check_any_winner():
                    print(f'{self.get_winner()} wins')
                    break
                if self.not_empty_cells():
                    print('Draw')
                    break
                self.change_state('game on')

        return None

    def get_init_matrix(self) -> list:
        return [[x for x in self.init_string[i:i + 3]] for i in
                range(0, self.dimension * self.dimension, self.dimension)]

    def get_game_representation(self) -> str:
        out_string = '-' * self.dimension * self.dimension + '\n'

        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                current = self.game_matrix[i][j]
                if (j + 1) % 3 == 1:
                    out_string += '|' + ' ' + current
                elif (j + 1) % 3 == 0:
                    out_string += ' ' + current + ' |' + '\n'
                else:
                    out_string += ' ' + current
        else:
            out_string += '-' * 9
        return out_string

    def check_horizontal(self, player) -> bool:
        for row in range(0, self.dimension):
            for column in range(0, self.dimension):
                current = self.game_matrix[row][column]
                if current != player:
                    break
            else:
                return True
        return False

    def check_vertical(self, player) -> bool:
        for row in range(0, self.dimension):
            for column in range(0, self.dimension):
                current = self.game_matrix[column][row]
                if current != player:
                    break
            else:
                return True
        return False

    def check_both_diagonals(self, player) -> bool:
        params_list = [[0, 1], [-1, -1]]
        conditions_list = []
        for params in params_list:
            offset, factor = params
            conditions_list.append(self.check_diagonal(player, offset, factor))

        return any(conditions_list)

    def check_diagonal(self, player, offset, factor) -> bool:
        for index in range(0, self.dimension):
            current = self.game_matrix[index][offset + factor * index]
            if current != player:
                break
        else:
            return True
        return False

    def check_any_winner(self):
        first, second = self.players_list
        return any([self.check_win(first), self.check_win(second)])

    def check_win(self, player) -> int:
        conditions_list = [self.check_horizontal(player), self.check_vertical(player),
                           self.check_both_diagonals(player)]
        return any(conditions_list)

    def get_winner(self) -> str:
        for player in self.players_list:
            if self.check_win(player):
                return player
        return '#'

    def check_all_winners(self):
        first, second = self.players_list
        conditions_list = [self.check_win(first), self.check_win(second)]
        return all(conditions_list)

    def not_empty_cells(self) -> bool:
        return self.placeholder not in [sym for row in self.game_matrix for sym in row]

    def count_symbol(self, player) -> int:
        result = 0
        for el in [player for row in self.game_matrix for player in row]:
            if el == player:
                result += 1
        return result

    def check_draw(self) -> bool:
        return self.not_empty_cells()

    def check_difference_moves(self):
        first, second = self.players_list
        return abs(self.count_symbol(first) - self.count_symbol(second)) > 1

    def check_impossible(self):
        conditions_list = [self.check_difference_moves(), self.check_all_winners()]
        return any(conditions_list)

    # check player moves block

    def checked_cell_occupation(self, f_list):
        x, y = [int(x) for x in f_list]
        return self.game_matrix[self.dimension - y][x - 1] == self.placeholder

    def add_new_cell(self, f_list):
        cell = 'O' if self.another_player else 'X'
        x, y = [int(x) for x in f_list]
        self.game_matrix[self.dimension - y][x - 1] = cell
        return self.game_matrix

    def checked_player_move(self, in_list):
        # 1) check for numbers
        if not self.checked_numbers(in_list, 0, 10):
            return 'not numbers'
        # 2) check for correct numbers
        if not self.checked_numbers(in_list, 1, self.dimension + 1):
            return 'incorrect number'
        # 3) check cell occupancy
        if not self.checked_cell_occupation(in_list):
            return 'cell occupation'

        return '#'

    def process_plays_move(self):
        while True:
            player_movie_str = input('Enter the coordinates: ')
            prepared_move_list = player_movie_str.strip().split()
            answer = self.checked_player_move(prepared_move_list)
            if answer == 'not numbers':
                print('You should enter numbers!')
            elif answer == 'incorrect number':
                print('Coordinates should be from 1 to 3!')
            elif answer == 'cell occupation':
                print('This cell is occupied! Choose another one!')
            else:
                return self.add_new_cell(prepared_move_list)


# end of class TicTacToe

tic_tac_toe = TicTacToe(3, ['X', 'O'], '_')
tic_tac_toe.run()
