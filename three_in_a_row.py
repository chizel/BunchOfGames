#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random


class game():
    # each item has its own picture and number
    items = [1, 2, 3, 4, 5]

    def __init__(self, size_r, size_c):
        # number of rows
        self.size_r = size_r
        # number of columns
        self.size_c = size_c
        self.score = 0

    def generate_field(self):
        field = []

        for row in range(self.size_r):
            new_row = []
            for column in range(self.size_r):
                cell = random.choice(self.items)
                new_row.append(cell)
            field.append(new_row)
        self.field = field[:]
        self.check_field()

    def colorize(self, num):
        res = ''
        if num == 1:
            res = '\033[95m'
        elif num == 2:
            res = '\033[94m'
        elif num == 3:
            res = '\033[93m'
        elif num == 4:
            res = '\033[92m'
        elif num == 5:
            res = '\033[91m'
        res += str(num)
        res += '\033[0m'
        return res

    def print_field(self):
        print('__________________________')
        print('\033[1m 01234\033[0m')
        i = 0
        for row in self.field:
            res_row = '\033[1m'
            res_row += str(i)
            res_row += '\033[0m'
            for cell in row:
                res_row += self.colorize(cell)
            print(res_row)
            i += 1
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

        for c_id in range(column + 1, self.size_c):
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

        for r_id in range(row + 1, self.size_r):
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

        for i in range(self.size_r):
            chains_r.extend(self.check_row(i, 0))
        for i in range(self.size_c):
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
            print('Your score is: ', self.score)
            self.move_down_cells()
            #self.fill_cells()

    def fill_cells(self):
        for r_id in range(self.size_r):
            for c_id in range(self.size_c):
                if not self.field[r_id][c_id]:
                    self.field[r_id][c_id] = random.choice(self.items)
        self.check_field()

    def move_down_cells(self):
        for c_id in range(self.size_c):
            for r_id in range(self.size_r - 1, -1, -1):
                if self.field[r_id][c_id]:
                    continue

                for i in range(r_id - 1, -1, -1):
                    if self.field[i][c_id]:
                        self.field[r_id][c_id] = self.field[i][c_id]
                        self.field[i][c_id] = 0
                        break
        self.fill_cells()

    def find_chain(self, coord, where_to_move):
        if where_to_move:
            ar, ac = 1, 0
        else:
            ar, ac = 0, 1

        r, c = coord
        chain_length = 1
        cell = self.field[r][c]

    # TODO check bounds
        if (r + ar) < self.size_r and (c + ac) < self.size_c and\
                self.field[r + ar][c + ac] == cell:
            chain_lenght = 2
            if (r + ar * 2) < self.size_r and (c + ac * 2) < self.size_c and\
                    self.field[r + ar * 2][c + ac * 2] == cell:
                # we have a chain, move make sense
                return True

        if (r - ar) > 0 and (c - ac) > 0 and\
                self.field[r - ar][c - ac] == cell:
            if chain_length == 2:
                # we have a chain, move make sense
                return True

            if (r - ar * 2) > 0 and (c - ac) > 0 and\
                    self.field[r - ar * 2][c - ac * 2] == cell:
                # we have a chain, move make sense
                self.check_field()
                return True
        return False

    def move_cell(self, from_coord, to_coord):
        '''check is moving is possible then moving cells'''
        fr, fc = from_coord
        tr, tc = to_coord

        # is coordinates are in borders of the field
        if fr >= self.size_r and tr >= self.size_r:
            return
        elif fc >= self.size_c and tc >= self.size_c:
            return

        # where to move - horizontal or vertical
        if fr == tr:
            # horizontal
            where_to_move = 1
        elif fc == tc:
            # vertical
            where_to_move = 0
        else:
            return

        # is cells are neighbours
        if where_to_move:
            if abs(fc - tc) != 1:
                return
        else:
            if abs(fr - tr) != 1:
                return

        # exchanging cells' values
        tmp = self.field[fr][fc]
        self.field[fr][fc] = self.field[tr][tc]
        self.field[tr][tc] = tmp

        # check is after moving we will have at least one chain
        # check upper and lower cells of the first cell
        if self.find_chain(from_coord, where_to_move):
            self.check_field()
            return
        # check upper and lower cells of the second cell
        if self.find_chain(to_coord, where_to_move):
            self.check_field()
            return

        # check front and back
        if where_to_move:
            cell = self.field[fr][fc]
            if (fc - 2) >= 0 and self.field[fr][fc - 1] == cell and\
                    self.field[fr][fc - 2] == cell:
                self.check_field()
                return
        else:
            if (fc + 2) < self.size_c and self.field[fr + 1][fc] == cell and\
                    self.field[fr + 2][fc] == cell:
                self.check_field()
                return

        # move doesn't make sense, reverse changes
        tmp = self.field[fr][fc]
        self.field[fr][fc] = self.field[tr][tc]
        self.field[tr][tc] = tmp
        print('nothing to move')
        return

    def update_score(self, score):
        '''update score'''
        # TODO develop better algorithm for updating score
        # more cells was destroyed - more points user get
        self.score += score


def main():
    mg = game(5, 5)
    mg.generate_field()
    while True:
        s = input('x y from x y to\n')
        fr, fc, tr, tc = s.split(' ')
        fr = int(fr)
        fc = int(fc)
        tr = int(tr)
        tc = int(tc)
        mg.move_cell([fr, fc], [tr, tc])
    return


if __name__ == "__main__":
    main()
