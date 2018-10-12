#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import random

class Pipes_field():
    objects = (
        # empty cell
        (,)
        # obstacle
        (,),
        # cross
        # has 2 connections - left-right, up-down
        (('l', 'r'), ('u', 'd')),
        # horizontal line
        ('l', 'r'),
        # vertical line 
        ('u', 'd'),
        # up-right
        ('u', 'r'),
        # right-down
        ('r', 'd'),
        # down-left
        ('d', 'l'),
        # left-up'
        ('l', 'u')),
        )

    def __init__(self, size_r, size_c):
        # number of rows
        self.size_r = size_r
        # number of columns
        self.size_c = size_c
        # user's score
        self.score = 0
        # cell that was selected for move
        self.generate_field()

    def generate_field(self):
        '''Creating new field'''
        field = []

        for row in range(self.size_r):
            new_row = [0 for _ in range(self.size_c)]
            field.append(new_row)
        self.field = field[:]

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

    def get_next_cell(self, r, c, dest):
        if dest == 'u':
            if r > 0:
                return (r - 1, c)
        elif dest == 'r':
            if c < self.size_c - 1:
                return (r, c + 1)
        elif dest == 'd':
            if r < self.size_r - 1:
                return (r + 1, c)
        else:
            if c > 0:
                return (r, c - 1)
        return None

    def check_connections(self, r, c, dest, next_cell):
        if dest == 'u' and 'd' in next_cell['dest']

    def check_field(self):
        self.sourse['r'] = '5'
        self.sourse['c'] = '2'
        self.sourse['dest'] = 'u'

        r = self.sourse['r']
        c = self.sourse['c']
        dest = self.sourse['dest']

        while True:
            coord = self.get_next_cell(r, c, dest)

            if not coord:
                break

            nr, nc = coord

            # empty cell
            if not self.field[nr][nc]:
                break

            next_cell 

            self.check_connections(r, c, dest, next_cell)


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
