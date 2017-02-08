#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import random


class Element():
    def __init__(self, position=-1):
        if position < 0:
            self.generate_position()
        else:
            self.position = position % 4
        self.on = False

    def rotate(self, clockwise=True):
        if clockwise:
            rotate = 1
        else:
            rotate = -1

        # must be ROTATE not CLOCKWISE!!!!!!!!!!!
        if self.position == 0:
            self.position = clockwise
        elif self.position == 1:
            self.position = 1 + clockwise
        elif self.position == 2:
            self.position = 2 + clockwise
        else:
            self.position = (3 + clockwise) % 4

    def generate_position(self):
        self.position = random.randint(0, 4)


class Line(Element):
    def rotate(self, clockwise=True):
        if self.position:
            self.position = 0
        else:
            self.position = 1

    def connections(self):
        if self.position == 0:
            return ['l', 'r']
        else:
            return ['u', 'd']

    def __str__(self):
        if self.position:
            return '|'
        else:
            return '-'


class T(Element):
    #0 T
    #1 -|
    #2 ^
    #3 |-
    def connections(self):
        if self.position == 0:
            return ['r', 'd', 'l']
        elif self.position == 1:
            return ['u', 'd', 'l']
        elif self.position == 2:
            return ['u', 'r', 'l']
        else:
            return ['u', 'r', 'd']

    def __str__(self):
        if self.position == 0:
            return 'T'
        elif self.position == 1:
            return '˨'
        elif self.position == 2:
            return '⊥'
        else:
            return 'Ͱ'


class L(Element):
    #0 L
    #1 Г
    #2 7
    #3 _|
    def connections(self):
        if self.position == 0:
            return ['u', 'r']
        elif self.position == 1:
            return ['r', 'd']
        elif self.position == 2:
            return ['d', 'l']
        else:
            return ['u', 'l']

    def __str__(self):
        if self.position == 0:
            return 'L'
        elif self.position == 1:
            return 'Г'
        elif self.position == 2:
            return 'ᄀ'
        else:
            return '˩'


class Source(Element):
    # 0 ⇧
    # 1 ⇨
    # 2 ⇩
    # 3 ⇦
    def __init__(self, position=0):
        super().__init__(position)
        self.on = True

    def connections(self):
        if self.position == 0:
            return ['u']
        elif self.position == 1:
            return ['r']
        elif self.position == 2:
            return ['d']
        else:
            return ['l']

    def __str__(self):
        if self.position == 0:
            return '⇧'
        elif self.position == 1:
            return '⇨'
        elif self.position == 2:
            return '⇩'
        else:
            return '⇦'


class Dest(Element):
    def connections(self):
        if self.position == 0:
            return ['u']
        elif self.position == 1:
            return ['r']
        elif self.position == 2:
            return ['d']
        else:
            return ['l']

    def __str__(self):
        if self.position == 0:
            return '⟟'
        elif self.position == 1:
            return '◐'
        elif self.position == 2:
            return '⫱'
        else:
            return '◑'


class Pipes():
    def __init__(self, size_r, size_c):
        # number of rows
        self.size_r = size_r
        # number of columns
        self.size_c = size_c
        # user's score
        self.score = 0
        # cell that was selected for move
        self.generate_field()
        self.connected = []

    def generate_field(self):
        '''Creating new field'''
        field = []

        for row in range(self.size_r):
            new_row = [0 for _ in range(self.size_c)]
            #new_row = []
            #for column in range(self.size_c):
                #cell = random.choice(self.colors)
            #    new_row.append(cell)
            field.append(new_row)
        self.field = field[:]

    def colorize(self, num, gui=False):
        '''colorizing cells'''
        res = ''
        if num == 1:
            res = '\033[95m'
            gcolor = 'grey'
        elif num == 2:
            res = '\033[94m'
            gcolor = 'blue'
        elif num == 3:
            res = '\033[93m'
            gcolor = 'yellow'
        elif num == 4:
            res = '\033[92m'
            gcolor = 'green'
        elif num == 5:
            res = '\033[91m'
            gcolor = 'red'

        if gui:
            return gcolor

        res += str(num)
        res += '\033[0m'
        return res

    def print_field(self):
        '''print field to console'''
        print('__________________________')
        print('\033[1m 0123456789\033[0m')
        i = 0
        for r_id in range(self.size_r):
            res_row = ''
            res_row = '\033[1m'
            res_row += str(i)
            res_row += '\033[0m'
            for c_id in range(self.size_c):
                #res_row += self.colorize(cell)
                if (r_id, c_id) in self.connected:
                    res_row += '\033[93m'
                    res_row += str(self.field[r_id][c_id])
                    res_row += '\033[0m'
                else:
                    res_row += str(self.field[r_id][c_id])
            print(res_row)
            i += 1
        print('__________________________')

    def create_source(self, row, column, position):
        self.field[row][column] = Source(position)
        self.source = (row, column)

    def connect_cell(self, conn_from, row, column):
        # from right --> <--from left
        # invert connection
        if not self.field[row][column]:
            return False

        if conn_from == 'u':
            check_conn = 'd'
        elif conn_from == 'r':
            check_conn = 'l'
        elif conn_from == 'd':
            check_conn = 'u'
        else:
            check_conn = 'r'

        connections = self.field[row][column].connections()

        if not check_conn in connections:
            # this cell has not connect with (row, column)
            return False

        if (row, column) in self.connected:
            # cell already connected
            return

        # add current cell to connected cells list
        self.connected.append((row, column))

        # removing connection from where source came (it's already connected)
        connections.remove(check_conn)

        if 'u' in connections and row > 0:
            self.connect_cell('u', row - 1, column)
        if 'r' in connections and (column + 1) < self.size_c:
            self.connect_cell('r', row, column + 1)
        if 'd' in connections and row + 1 < self.size_r:
            self.connect_cell('d', row + 1, column)
        if 'l' in connections and column > 0:
            self.connect_cell('l', row, column - 1)

    def check_connections(self):
        source = self.source
        start = self.field[source[0]][source[1]].connections()
        self.connected = [source]

        if 'u' in start:
            if source[0] > 0:
                self.connect_cell('u', source[0] - 1, source[1])
        elif 'l' in start:
            if source[1] + 1 < self.size_c:
                self.connect_cell('l', source[0], source[1] + 1)
        elif 'd' in start:
            if source[0] + 1 < self.size_r:
                self.connect_cell('d', source[0] + 1, source[1])
        else:
            if source[0] + 1 < self.size_r:
                self.connect_cell('r', source[0], source[1] + 1)

        #for cell in self.connected:
    def create_destinations(self, dest_coordinates):
        for r_id, c_id in dest_coordinates:
            self.field[r_id][c_id] = Dest()


def main():
    mg = Pipes(5, 5)
    mg.create_source(1, 1, 0)
    mg.field[0][0] = L()
    mg.field[0][1] = L()
    mg.field[0][2] = Line()
    mg.field[0][3] = Line()
    mg.field[0][3] = L()
    mg.field[1][3] = Line()
    mg.field[2][1] = T()
    mg.field[2][2] = T()
    mg.field[2][3] = T()
    mg.field[2][4] = T()
    dest_coordinates = [(2, 0), (4, 3), (3, 2)]
    mg.create_destinations(dest_coordinates)
    mg.check_connections()
    mg.print_field()
    return


if __name__ == "__main__":
    main()
