#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random


class game():
    # each item has its own picture
    items = [0, 1, 2, 3, 4]
    score = 0

    def __init__(self, field_r, field_c):
        # number of rows
        self.field_r = field_r
        # number of columns
        self.field_c = field_c

    def generate_field(self):
        field = []
        #TODO REMOVE
        for row in range(self.field_r):
            field.append([0] * self.field_c)
        self.field = field[:]
        #TODO END REMOVE
        return
        for row in range(self.field_r):
            new_row = []
            for column in range(self.field_r):
                cell = random.choice(self.items)
                new_row.append(cell)
            field.append(new_row)
        self.field = field[:]

    def print_field(self):
        print('__________________________')
        for row in self.field:
            res_row = ''
            for cell in row:
                res_row += str(cell)
            print(res_row)
        print('__________________________')

    def check_row(self, row, column, check_left=False):
        ''' if check_left is True - function will look to the left cell
        for equal cells'''
        cell = self.field[row][column]
        chain = 1

        if check_left:
            for c in range(column - 1, -1, -1):
                if self.field[row][c] == cell:
                    chain += 1
                else:
                    break

        for c in range(column + 1, self.field_c):
            if self.field[row][c] == cell:
                chain += 1
            else:
                break

        if chain > 2:
            return chain
        return 0

    def check_column(self, row, column, check_up=False):
        ''' if check_up is True - function will look to the left cell
        for equal cells'''
        cell = self.field[row][column]
        chain = 1

        if check_up:
            for r in range(row - 1, -1, -1):
                if self.field[r][column] == cell:
                    chain += 1
                else:
                    break

        for r in range(row + 1, self.field_r):
            if self.field[r][column] == cell:
                chain += 1
            else:
                break

        if chain > 2:
            return chain
        return 0

    def check_field(self):
        '''
        2011020
        0201002
        2011110
        0211012
        2101010
        0101102
        '''
        print('check_field() in progress. I don\'t now how to solve it yet :(')
        return
        for row in range(self.field_r):
            for column in range(self.field_c):
                cell = self.field[row][column]
                # checking row
                # cell is first in the chain
                chain_length = 1

                for i in range(column + 1, self.field_c):
                    if cell == self.field[row][i]:
                        chain_length += 1
                    else:
                        if chain_length > 2:
                            # TODO update score
                            # TODO check if this chain has vertical subchain
                            self.move_cells_down(row, i, chain_length, 1)
                if chain_length > 2:
                    self.move_cells_down(row, i, chain_length, 1)
                #return
                # check column
        return

    def move_cells_down(self, cells_map, start_row):
        '''
        Cells_map is a map of steps to move cell down.
        For example: 0 1 3 0 mean first column we don't change,
        second we need to move down,
        third move down by 3 cells and
        the last column we do not change.
        '''
        for r_id in range(row_start, -1, -1):
            for c_id in range(self.field_c):
                # we need to remove this cell and place upper cell
                # to this
                if cells_map[r_id][c_id]:
                    changed = False
                    # check upper_cells
                    for row_id in range(r_id + 1, -1, -1):
                        if not cells_map[row_id][c_id]:
                            self.field[r_id][c_id] = self.field[row_id][c_id]
                            changed = True
                        if not changed:
                            self.field[r_id][c_id] = random.choice(self.items)
        #self.check_field()
        return

    def update_score(self, count_cells):
        '''update score'''
        # TODO develop better algorithm for updating score
        # more cells was destroyed - more points user get 
        self.score += count_cells
        return


def main():
    my_game = game(5, 5)
    my_game.generate_field()
    #my_game.field[0][0] = 4
    #my_game.field[0][1] = 1
    #my_game.field[0][2] = 5
    #my_game.field[1][1] = 1
    #my_game.field[1][0] = 2
    #my_game.field[2][1] = 1
    #my_game.field[2][2] = 3
    #my_game.field[3][0] = 1
    #my_game.field[3][1] = 1
    #my_game.field[3][2] = 1
    #my_game.field[3][3] = 1
    #my_game.print_field()
    #my_game.check_field()
    my_game.print_field()
    r=my_game.check_column(2, 1, True)
    #print(r)
    return


if __name__ == "__main__":
    main()
