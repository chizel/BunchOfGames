#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random


class game():
    # each item has its own picture and number
    items = [1, 2, 3, 4, 5]

    def __init__(self, field_r, field_c):
        # number of rows
        self.field_r = field_r
        # number of columns
        self.field_c = field_c
        self.score = 0

    def generate_field(self):
        field = []

        for row in range(self.field_r):
            new_row = []
            for column in range(self.field_r):
                cell = random.choice(self.items)
                new_row.append(cell)
            field.append(new_row)
        self.field = field[:]
        self.check_field()

    def print_field(self):
        print('__________________________')
        for row in self.field:
            res_row = ''
            for cell in row:
                res_row += str(cell)
            print(res_row)
        print('__________________________')

    def check_row(self, row, column, min_length=3, check_left=False):
        ''' if check_left is True - function will look to the left cell
        for equal cells'''
        cell = self.field[row][column]
        chain_length = 1
        start = column
        # list with chains' data
        res = []

        if check_left:
            for c_id in range(column - 1, -1, -1):
                if self.field[row][c_id] == cell:
                    chain_length += 1
                    start = column - 1
                else:
                    break


        for c_id in range(column + 1, self.field_c):
            if self.field[row][c_id] == cell:
                chain_length += 1
            else:
                if chain_length >= min_length:
                    res.append([chain_length, (row, start)])
                start = c_id
                cell = self.field[row][c_id]
                chain_length = 1
        if chain_length >= min_length:
            res.append([chain_length, (row, start)])
        return res

    def check_column(self, row, column, min_length=3, check_up=False):
        ''' if check_up is True - function will look to the left cell
        for equal cells'''
        cell = self.field[row][column]
        chain_length = 1
        start = row
        # list with chains' data
        res = []

        if check_up:
            for r_id in range(row - 1, -1, -1):
                if self.field[r_id][column] == cell:
                    chain += 1
                    start -= 1
                else:
                    break

        for r_id in range(row + 1, self.field_r):
            if self.field[r_id][column] == cell:
                chain_length += 1
            else:
                if chain_length >= min_length:
                    res.append([chain_length, (start, column)])
                start = r_id
                cell = self.field[r_id][column]
                chain_length = 1
 
        if chain_length >= min_length:
            res.append([chain_length, (start, column)])
        return res

    def check_field(self):
        self.print_field()
        chains_r = []
        chains_c = []
        score = 0

        for i in range(self.field_r):
            chains_r.extend(self.check_row(i, 0))
        for i in range(self.field_c):
            chains_c.extend(self.check_column(0, i))

        if chains_r:
            for chain in chains_r:
                for i in range(chain[0]):
                    self.field[chain[1][0]][chain[1][1] + i] = 0
                score += chain[0]

        if chains_c:
            for chain in chains_c:
                for i in range(chain[0]):
                    self.field[chain[1][0] + i][chain[1][1]] = 0
                score += chain[0]

        if score:
            self.update_score(score)
            print(self.score)
            self.fill_cells()

    def fill_cells(self):
        for r_id in range(self.field_r):
            for c_id in range(self.field_c):
                self.field[r_id][c_id] = random.choice(self.items)
        self.check_field()

    def move_cells_down(self):
        for c_id in range(self.field_c):
            for r_id in range(self.field_r, -1, -1):
                if self.field[r_id][c_id]:
                    continue
                for row_id in range(r_id + 1, -1, -1):
                    if not cells_map[row_id][c_id]:
                        self.field[r_id][c_id] = self.field[row_id][c_id]
                        changed = True
                    if not changed:
                        self.field[r_id][c_id] = random.choice(self.items)
        self.fill_cells()

    def move_cell(from_coord, to_coord):
        '''check is moving is possible'''
        fr, fc = from_coord
        tr, tc = to_coord
        tmp = self.field[r][c]
        self.field[r][c] = self.field[tr][tc]
        self.field[tr][tc] tmp
        # check is moving make sense e.g.
        # after moving there is a chain (or more)

    def update_score(self, score):
        '''update score'''
        # TODO develop better algorithm for updating score
        # more cells was destroyed - more points user get 
        self.score += score


def main():
    mg = game(5, 5)
    mg.generate_field()
    mg.check_field()
    return


if __name__ == "__main__":
    main()
