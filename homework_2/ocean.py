#!/usr/bin/python3
import random


class Cell(object):
    def __init__(self, ocean, x, y, reproduction_period):
        self.ocean = ocean
        self.x = x
        self.y = y
        self.reproduction_period = reproduction_period
        self.age = 0

    def die(self):
        self.ocean.field[self.y][self.x] = EmptyCell(self.ocean, self.x, self.y)

    def go(self, cell):
        self.ocean.field[cell.y][cell.x] = self
        self.ocean.field[self.y][self.x] = EmptyCell(self.ocean, self.x, self.y)
        self.x = cell.x
        self.y = cell.y

    def make_turn(self):
        self.age += 1
        if self.reproduction_period is not None:
            if self.age % self.reproduction_period == 0:
                try:
                    empty_neighbor = self.ocean.get_random_neighbor(self, EmptyCell)
                    self.born(empty_neighbor)
                except NeighborException:
                    pass

    def try_move(self):
        try:
            empty_neighbor = self.ocean.get_random_neighbor(self, EmptyCell)
            self.go(empty_neighbor)
        except NeighborException:
            pass

    def born(self, cell):
        pass


class Predator(Cell):
    def __init__(self, ocean, x, y, health=100, reproduction_period=150):
        super().__init__(ocean, x, y, reproduction_period)
        self.full_health = health
        self.health = health

    def make_turn(self):
        super().make_turn()
        self.health -= 1
        if self.health < 0:
            self.die()
            return

        try:
            victim_neighbor = self.ocean.get_random_neighbor(self, Victim)
            self.go(victim_neighbor)
            self.health = self.full_health
        except NeighborException:
            self.try_move()

    def born(self, cell):
        self.ocean.field[cell.y][cell.x] = Predator(self.ocean, cell.x, cell.y)


class Victim(Cell):
    def __init__(self, ocean, x, y, reproduction_period=50):
        super().__init__(ocean, x, y, reproduction_period)

    def make_turn(self):
        super().make_turn()
        self.try_move()

    def born(self, cell):
        self.ocean.field[cell.y][cell.x] = Victim(self.ocean, cell.x, cell.y)


class Obstacle(Cell):
    def __init__(self, ocean, x, y):
        super().__init__(ocean, x, y, None)


class EmptyCell(Cell):
    def __init__(self, ocean, x, y):
        super().__init__(ocean, x, y, None)


def generate_random_cell(ocean, x, y):
    random_number = random.random()
    if random_number < 0.99:
        return EmptyCell(ocean, x, y)
    else:
        random_number = random.random()
        if random_number < 1 / 3:
            return Predator(ocean, x, y)
        elif random_number > 2 / 3:
            return Victim(ocean, x, y)
        else:
            return Obstacle(ocean, x, y)


class NeighborException(Exception):
    pass


class Ocean(object):
    def __init__(self, width, height, map_file=None):
        self.width = width
        self.height = height
        self.turn = 0

        if map_file is None:
            self.generate_random_field()
        else:
            self.make_empty_filed()
            self.read_map(map_file)
            self.animate()

    def generate_random_field(self):
        self.field = [
            [generate_random_cell(self, x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def make_empty_filed(self):
        self.field = [
            [EmptyCell(self, x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def type_counter(self, cell_type):
        return sum([
            sum([1 for cell in line if type(cell) == cell_type])
            for line in self.field
        ])

    def animate(self):
        for y in range(self.height):
            for x in range(self.width):
                if type(self.field[y][x]) == EmptyCell:
                    random_number = random.random()
                    if random_number > 0.99:
                        random_number = random.random()
                        if random_number < 1 / 2:
                            self.field[y][x] = Predator(self, x, y)
                        else:
                            self.field[y][x] = Victim(self, x, y)

    def read_map(self, file_name):
        with open(file_name) as file:
            field = [[character for character in line[:-1]] for line in file]

        for y in range(self.height):
            for x in range(self.width):
                if field[y][x] == 'X':
                    self.field[y][x] = Obstacle(self, x, y)

    def get_neighbors(self, cell, cell_type):
        result = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == dy == 0:
                    continue
                y = (cell.y + dy) % self.height
                x = (cell.x + dx) % self.width
                if type(self.field[y][x]) == cell_type:
                    result.append(self.field[y][x])
        return result

    def get_random_neighbor(self, cell, cell_type):
        neighbors = self.get_neighbors(cell, cell_type)
        if len(neighbors) == 0:
            raise NeighborException()
        return neighbors[random.randint(0, len(neighbors) - 1)]

    def make_turn(self):
        for y in range(self.height):
            for x in range(self.width):
                self.field[y][x].make_turn()

        self.turn += 1
