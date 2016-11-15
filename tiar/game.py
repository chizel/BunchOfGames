#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import json


class game():
    # each item has its own picture and number
    items = [1, 2, 3, 4, 5]
    PATH = './data/'

    def __init__(self, size_r, size_c):
        # check field's sizes
        if size_r < 3 or size_c < 3:
            print('field\'s sizes can\'t be less than 3!')
            exit()
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
        '''Looking for chains in all rows starting from [row, columng].
        If check_left is True - function will look to the left cell
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
                    # chain's lenght is ok, save it
                    res.append([chain_length, (row, start)])
                start = c_id
                cell = self.field[row][c_id]
                chain_length = 1
        if chain_length >= min_length:
            res.append([chain_length, (row, start)])
        return res

    def check_column(self, row, column, min_length=3, check_up=False):
        '''Looking for chains in all columns starting from [row, columng].
        if check_up is True - function will look to the up cells of the
        field for equal cells'''
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
                    # chain's lenght is ok, save it
                    res.append([chain_length, (start, column)])
                start = r_id
                cell = self.field[r_id][column]
                chain_length = 1

        if chain_length >= min_length:
            res.append([chain_length, (start, column)])
        return res

    def check_field(self):
        '''Checking field for chains in rows and columns'''
        # if we need to check field something had happend to it
        # print it
        self.print_field()
        chains_r = []
        chains_c = []
        score = 0

        for i in range(self.size_r):
            chains_r.extend(self.check_row(i, 0))
        for i in range(self.size_c):
            chains_c.extend(self.check_column(0, i))

        if chains_r:
            # there are chains in some row(s)
            for chain in chains_r:
                for i in range(chain[0]):
                    self.field[chain[1][0]][chain[1][1] + i] = 0
                score += chain[0]

        if chains_c:
            # there are chains in some column(s)
            for chain in chains_c:
                for i in range(chain[0]):
                    self.field[chain[1][0] + i][chain[1][1]] = 0
                score += chain[0]

        # is there were any chains?
        if score:
            self.update_score(score)
            print('Your score is: ', self.score)
            self.move_down_cells()
            return True
        else:
            return False

    def fill_cells(self):
        '''Generate value for empty cells'''
        for r_id in range(self.size_r):
            for c_id in range(self.size_c):
                if not self.field[r_id][c_id]:
                    self.field[r_id][c_id] = random.choice(self.items)
        self.check_field()

    def move_down_cells(self):
        '''Move full cells down to empty cells'''
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

    def exchange_cells(self, from_coord, to_coord):
        '''Checking is exchange is possible
        exchanging cells values and checking is move made sense
        e.g. after moving there is at least one chain'''
        fr, fc = from_coord
        tr, tc = to_coord

        # is coordinates are in borders of the field
        if fr >= self.size_r and tr >= self.size_r:
            return
        elif fc >= self.size_c and tc >= self.size_c:
            return

        # is cells are neighbours
        if where_to_move:
            if abs(fc - tc) != 1:
                return
        else:
            if abs(fr - tr) != 1:
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

        # exchanging cells' values
        tmp = self.field[fr][fc]
        self.field[fr][fc] = self.field[tr][tc]
        self.field[tr][tc] = tmp

        if self.check_field():
            # move make sense nothing to do more
            return

        # move doesn't make sense, reverse changes
        tmp = self.field[fr][fc]
        self.field[fr][fc] = self.field[tr][tc]
        self.field[tr][tc] = tmp
        self.print_field()
        print('nothing to move')
        return

    def find_pairs(self):
        '''Search for pairs of similar cell in row and columns'''
        # checking rows
        pairs_r = []
        for i in range(self.size_r):
            cell = self.field[i][0]

            for j in range(1, self.size_c):
                if self.field[i][j] == cell:
                    # saving start of the pair
                    pairs_r.append((i, j - 1))
                else:
                    cell = self.field[i][j]

        # checking columns
        pairs_c = []
        for j in range(self.size_c):
            cell = self.field[0][j]

            for i in range(1, self.size_r):
                if self.field[i][j] == cell:
                    # saving start of the pair
                    pairs_c.append((i - 1, j))
                else:
                    cell = self.field[i][j]
        return pairs_r, pairs_c

    def check_field_for_moves(self):
        '''Checking is field has some possible moves. If has - returns True,
        if hasn't - returns False'''
        pairs_r, pairs_c = self.find_pairs()

        # checking row's pairs
        for r, c in pairs_r:
            cell = self.field[r][c]

            # check left side of the pair: up and down
            if c > 0:
                if r > 0 and self.field[r - 1][c - 1] == cell:
                    return True
                if (r + 1) < self.size_r and self.field[r + 1][c - 1] == cell:
                    return True
            # check left side of the pair: horizontal
            if c > 1:
                if self.field[r][c - 2] == cell:
                    return True

            # check right side of the pair: up and down
            if (c + 2) < self.size_c:
                if (r - 1) >= 0 and self.field[r - 1][c + 2] == cell:
                    return True
                if (r + 1) < self.size_r and self.field[r + 1][c + 2] == cell:
                    return True
            # check right side of the pair: horizontal
            if (c + 3) < self.size_c and self.field[r][c + 3] == cell:
                return True

        # checking column's pairs
        for r, c in pairs_c:
            cell = self.field[r][c]
            # check up of the pair: left and right
            if r > 0:
                if c > 0 and self.field[r - 1][c - 1] == cell:
                    return True
                if (c + 1) < self.size_c and self.field[r - 1][c + 1] == cell:
                    return True
            # check up of the pair: vertical
            if r > 1:
                if self.field[r - 2][c] == cell:
                    return True

            # check down side of the pair: left and right
            if (r + 2) < self.size_r:
                if (c - 1) >= 0 and self.field[r + 2][c - 1] == cell:
                    return True
                if (c + 1) < self.size_r and self.field[r + 2][c + 1] == cell:
                    return True
            # check right side of the pair: horizontal
            if (r + 3) < self.size_r and self.field[r + 3][c] == cell:
                return True

        # checking for neighbout pairs:
        #     *2*  1*3  *2  1*
        #     3*3  *4*  3*  *2
        #               *5  1*

        # checking rows
        for r in range(self.size_r):
            for c in range(self.size_c):
                cell = self.field[r][c]

                if (c + 2) < self.size_c and self.field[r][c + 2] == cell:
                    #check middle cell up and down
                    if r > 0 and self.field[r - 1][c + 1] == cell:
                        return True
                    if (r + 1) < self.size_r and\
                            self.field[r + 1][c + 1] == cell:
                        return True

        # checking columns
        for c in range(self.size_c):
            for r in range(self.size_r):
                cell = self.field[r][c]

                if (r + 2) < self.size_r and self.field[r + 2][c] == cell:
                    #check middle cell up and down
                    if c > 0 and self.field[r + 1][c - 1] == cell:
                        return True
                    if (c + 1) < self.size_r and\
                            self.field[r + 1][c + 1] == cell:
                        return True
        # TODO make this works
        print('we need to shuffle')
        return False

    def shuffle_field(self):
        '''If there is not a move - shuffle field'''
        return

    def update_score(self, score):
        '''update score'''
        # TODO develop better algorithm for updating score
        # more cells was destroyed - more points user get
        self.score += score

    def save_game(self):
        '''Saving game to a file'''
        with open(self.PATH + 'save.txt', 'w') as f:
            json.dump(self.field, f)

    def load(self):
        '''Loading saved game'''
        with open('save.txt', 'r') as f:
            tmp_field = []

            for line in f:
                tmp_row = []
                for ch in line:
                    try:
                        tmp_row.append(int(ch))
                    except:
                        pass
                tmp_field.append(tmp_row)
        # TODO we need check size of field
        self.field = tmp_field[:]


def main():
    #mg = game(4, 4)
    #mg.generate_field()
    #mg.field[0][0] = 1
    #mg.field[0][1] = 1
    #mg.field[0][2] = 4
    #mg.field[0][3] = 2
    #mg.field[1][0] = 1
    #mg.field[1][1] = 2
    #mg.field[1][2] = 3
    #mg.field[1][3] = 5
    #mg.field[2][0] = 5
    #mg.field[2][1] = 4
    #mg.field[2][2] = 2
    #mg.field[2][3] = 1
    #mg.field[3][0] = 3
    #mg.field[3][1] = 2
    #mg.field[3][2] = 4
    #mg.field[3][3] = 3
    #mg.print_field()
    #print(mg.check_field_for_moves())
    #exit()
    mg = game(5, 5)
    mg.generate_field()
    while True:
        s = input('x y from x y to\n')
        if s == 'l':
            mg.load()
            mg.print_field()
        elif len(s) == 4:
            fr = int(s[0])
            fc = int(s[1])
            tr = int(s[2])
            tc = int(s[3])
            mg.exchange_cells([fr, fc], [tr, tc])
            mg.check_field_for_moves()
        else:
            mg.print_field()
    return


if __name__ == "__main__":
    main()
