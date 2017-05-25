#!/usr/local/bin python3.6

from itertools import product
import random


class StrokeSelectionError(Exception):
    pass


class NoStrokeError(Exception):
    pass


class Field:
    '''
        self.matrix is n*n matrix, whitch store the fied
        (self.matrix[i][j] == 0) <=> (i, j) cell is free
        (self.matrix[i][j] == 1) <=> (i, j) cell contains black chip
        (self.matrix[i][j] == 2) <=> (i, j) cell contains white chip

        self.player is a player who moves this turn
        self.player = 1: black player
        self.player = 2: white player
    '''

    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __init__(self, n=8):
        self.matrix = [
            [0 for j in range(n)] for i in range(n)
        ]
        self.matrix[int(n / 2)][int(n / 2) - 1] = Field.BLACK
        self.matrix[int(n / 2) - 1][int(n / 2)] = Field.BLACK
        self.matrix[int(n / 2) - 1][int(n / 2) - 1] = Field.WHITE
        self.matrix[int(n / 2)][int(n / 2)] = Field.WHITE

        self.player = Field.BLACK

        self.random_games_number = 10

        self.angles = [
            (0, 0),
            (0, len(self.matrix) - 1),
            (len(self.matrix) - 1, 0),
            (len(self.matrix) - 1, len(self.matrix) - 1)
        ]

    def opposite_color(self, color):
        return Field.BLACK if color == Field.WHITE else Field.WHITE

    def is_inside(self, i, j):
        return (0 <= i < len(self.matrix)) and (0 <= j < len(self.matrix[i]))

    def is_direction_available(self, i, j, dx, dy):
        if dx == dy == 0:
            return False
        counter = 0
        while True:
            counter += 1
            new_x = i + dx * counter
            new_y = j + dy * counter
            if not self.is_inside(new_x, new_y):
                break
            elif self.matrix[new_x][new_y] == self.opposite_color(self.player):
                continue
            elif self.matrix[new_x][new_y] == self.player:
                if counter > 1:
                    return True
                else:
                    break
            else:
                break
        return False

    def is_stroke_available(self, i, j):
        if self.matrix[i][j] != Field.EMPTY:
            return False
        for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
            if self.is_direction_available(i, j, dx, dy):
                return True

    def get_fill_directions(self, i, j):
        if self.matrix[i][j] != Field.EMPTY:
            return []
        result = []
        for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
            if self.is_direction_available(i, j, dx, dy):
                result.append((dx, dy))
        return result

    def get_available_strokes(self):
        return [
            (i, j)
            for i in range(len(self.matrix))
            for j in range(len(self.matrix[i]))
            if self.is_stroke_available(i, j)
        ]

    def make_turn(self, i, j):
        if (i, j) not in self.get_available_strokes():
            raise StrokeSelectionError()

        for dx, dy in self.get_fill_directions(i, j):
            counter = 1
            new_x = i + dx * counter
            new_y = j + dy * counter
            while self.matrix[new_x][new_y] != self.player:
                self.matrix[new_x][new_y] = self.player
                counter += 1
                new_x = i + dx * counter
                new_y = j + dy * counter
        self.matrix[i][j] = self.player
        self.player = self.opposite_color(self.player)

    def skip_turn(self):
        self.player = self.opposite_color(self.player)

    def make_random_turn(self):
        if len(self.get_available_strokes()) == 0:
            raise NoStrokeError()
        self.make_turn(*random.choice(self.get_available_strokes()))

    def get_winner(self):
        black_counter = sum([
            1
            for i in range(len(self.matrix))
            for j in range(len(self.matrix[i]))
            if self.matrix[i][j] == Field.BLACK
        ])
        white_counter = sum([
            1
            for i in range(len(self.matrix))
            for j in range(len(self.matrix[i]))
            if self.matrix[i][j] == Field.WHITE
        ])
        if black_counter > white_counter:
            return Field.BLACK
        elif white_counter > black_counter:
            return Field.WHITE
        else:
            return Field.EMPTY

    def compete(self, black_turn, white_turn):
        has_stroke = {Field.BLACK: True, Field.WHITE: True}
        while True:
            try:
                has_stroke[self.player] = True
                if self.player == Field.BLACK:
                    black_turn(self)
                else:
                    white_turn(self)
            except NoStrokeError as exception:
                has_stroke[self.player] = False
                self.skip_turn()

            if (not has_stroke[Field.BLACK]) and (not has_stroke[Field.WHITE]):
                return self.get_winner()

    def compare(self, black_turn, white_turn, games_number=100):
        '''
            no score for angles:

            black score: 95 (95.0 %)
            white score: 4 (4.0 %)
            friendship: 1 (1.0 %)

            score for angles:

            black score: 97 (97.0 %)
            white score: 2 (2.0 %)
            friendship: 1 (1.0 %)
        '''
        counters = {Field.BLACK: 0, Field.WHITE: 0, Field.EMPTY: 0}
        for i in range(games_number):
            print('[' + '#' * (i + 1) + ' ' * (games_number - i - 1) + ']')
            tmp_field = self.copy()
            counters[tmp_field.compete(black_turn, white_turn)] += 1

        black_percentage = counters[Field.BLACK] / games_number * 100
        white_percentage = counters[Field.WHITE] / games_number * 100
        empty_percentage = counters[Field.EMPTY] / games_number * 100
        print('black score: {} ({} %)\nwhite score: {} ({} %)\nfriendship: {} ({} %)'.format(
            counters[Field.BLACK], black_percentage,
            counters[Field.WHITE], white_percentage,
            counters[Field.EMPTY], empty_percentage
        ))

    def get_random_winner(self):
        return self.compete(Field.make_random_turn, Field.make_random_turn)

    def copy(self):
        copy_field = Field(len(self.matrix))
        for i in range(len(self.matrix)):
            for j, color in enumerate(self.matrix[i]):
                copy_field.matrix[i][j] = color
        copy_field.player = self.player
        return copy_field

    def cell_score(self, i, j):
        if (i, j) in self.angles:
            return self.random_games_number / 2
        else:
            return 0

    def make_smart_turn(self):
        if len(self.get_available_strokes()) == 0:
            raise NoStrokeError()
        scores = {(i, j): self.cell_score(i, j) for (i, j) in self.get_available_strokes()}
        for game in range(self.random_games_number):
            for i, j in self.get_available_strokes():
                tmp_field = self.copy()
                tmp_field.make_turn(i, j)
                if tmp_field.get_random_winner() == self.player:
                    scores[(i, j)] += 1

        best_stroke = sorted([(key, scores[key]) for key in scores], key=lambda x: -x[1])[0][0]
        self.make_turn(*best_stroke)


def check_strokes(strokes):
    field = Field()
    for i, j in strokes:
        try:
            field.make_turn()
        except StrokeSelectionError:
            return False
    return True
