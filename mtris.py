#! /usr/bin/env python3
# -*- coding: utf-8 -*-


class Figure():
    '''
       0 **
         **

       1 *****

       2  **
         **

       3 **
          **

       4  *
         ***

       5 ****
         *

       6 *
         ****
       '''
    figures = [0, 1, 2, 3, 4, 5]

    def __init__(self, figure_id, tf):
        self.figure_id = figure_id
        self.init_figure()
        # tetris field object
        self.tf = tf

    def init_figure(self):
        # r, c - bottom left corner
        self.data = {'r': 0, 'c': 0}
        if self.figure_id == 0:
            self.data['coordinates'] = [[0, 0], [0, 1],
                                        [1, 0], [1, 1]]
        elif self.figure_id == 1:
            self.data['coordinates'] = [[0, 0], [0, 1], [0, 2], [0, 3]]
        elif self.figure_id == 2:
            self.data['coordinates'] = [[0, 0], [0, 1],
                                        [1, 1], [1, 2]]
        elif self.figure_id == 3:
            self.data['coordinates'] = [[0, 1], [0, 2],
                                        [1, 0], [1, 1]]
        elif self.figure_id == 4:
            self.data['coordinates'] = [[0, 1],
                                        [1, 0], [1, 1], [1, 2]]
            #self.data['coordinates'] = [[[0,1]],
                                        #[[1,0], [1,1], [1,2]]]
        #elif self.figure_id == 5:
            #self.data['coordinates'] = [[[0,0], [0,1], [0,2], [0,3]]
                                        #[[1,0]]]
        return

    def print_figure(self):
        print('-------------------------------')
        for coord in self.data['coordinates']:
            print(coord)
        print('-------------------------------')

    def rotate(self, field):
        # square
        if self.figure_id == 0:
            return

        coord = self.data['coordinates']
        new_coord = []
        base = coord[0]

        if self.figure_id == 1:
            # figure is horizontal
            if coord[0][1] < coord[1][1]:
                for i in range(len(coord)):
                    new_coord.append([base[0] - i, base[1]])
            else:
            # figure is vertical
            # coordinates: [[0,1], [1,1], [2,1], [3,1]]
                for i in range(len(coord)):
                    new_coord.append([base[0], base[1] + i])
        elif self.figure_id == 2:
            if coord[0][0] == coord[1][0]:
            # horizontal
            # **
            #  **
            # [[1,0], [1,1],
            # [2,1], [2,2]]
                new_coord = [base[:], [base[0] - 1, base[1] + 1],
                             [base[0] + 1, base[1]], [base[0], base[1] + 1]]
            else:
            # vertical
            #  *
            # **
            # *
            # [1,0], [0,1],
            # [2,0], [1,1]
                new_coord = [
                    base[:], [base[0], base[1] + 1],
                    [base[0] + 1, base[1] + 1], [base[0] + 1, base[1] + 2]]
            # checking if rotation is possible
        elif self.figure_id == 3:
            if coord[0][0] == coord[1][0]:
            # horizontal
            #  **
            # **
            # [0,1], [0,2],
            # [1,0], [1,1]
                new_coord = [
                    base[:], [base[0] + 1, base[1]],
                    [base[0] + 1, base[1] + 1], [base[0] + 2, base[1] + 1]]
            else:
            # vertical
            # *
            # **
            #  *
            # [0,1], [1,1],
            # [1,2], [2,2]
                new_coord = [
                    base[:], [base[0], base[1] + 1],
                    [base[0] + 1, base[1] - 1], [base[0] + 1, base[1]]]
        elif self.figure_id == 4:
            if coord[1][0] == coord[2][0]:
                # horizontal
                if coord[0][0] < coord[1][0]:
                    # up
                    pass
                else:
                    # down
                    pass
            else:
                # vertical
                if coord[0][1] > coord[1][1]:
                    # right
                    pass
                else:
                    # left
                    pass
        elif self.figure_id == 5:
            print(5)
        elif self.figure_id == 6:
            print(6)
        else:
            raise TypeError('self.figure_id is ' + str(self.figure_id) +
                            '. Must be from 0 to 6!')

        # check if rotating is possible
        for c in new_coord:
            if self.tf.field[c[0]][c[1]]:
                return
        self.data['coordinates'] = new_coord
        return

    def move_left(self):
        '''moves figure to the left if possible'''
        for coord in self.data['coordinates']:
            if coord[1] - 1 < 0:
                # we are near the left border
                # can't move figure through the border
                return
            if self.tf.field[coord[0]][coord[1] - 1]:
                # can't move to the left - cells has smth in it
                return

        # updating coordinates
        for i in range(len(self.data['coordinates'])):
            self.data['coordinates'][i][1] -= 1
        return

    def move_right(self):
        '''moves figure to the right if possible'''
        for coord in self.data['coordinates']:
            if coord[1] + 1 >= self.tf.c:
                # we are near the right border
                # can't move figure through the border
                return
            if self.tf.field[coord[0]][coord[1] + 1]:
                # can't move to the left - cells has smth in it
                return

        # updating coordinates
        for i in range(len(self.data['coordinates'])):
            self.data['coordinates'][i][1] += 1

    def move_down(self):
        '''
        check last row in coordinates
        check next row in the field
        '''
        # figure reached the last row of the field
        if self.data['r'] + 1 == self.tf.r:
            self.write_to_field()
            return

        # checking is moving possible
        for coord in self.data['coordinates']:
            if self.tf.field[coord[0] + 1][coord[1]]:
                self.write_to_field()
                return

        # updating coordinates
        for i in range(len(self.data['coordinates'])):
            self.data['coordinates'][i][0] += 1

        return

    def write_to_field(self):
        '''if unable to move figure down - write it to the field
        to the current position
        '''
        for coord in self.data['coordinates']:
            self.tf.field[coord[0]][coord[1]] = 1
        return


class Tetris():
    def __init__(self, r, c):
        # number of rows
        self.r = r
        # number of columns
        self.c = c
        # creating an empty field
        self.init_field()
        # empty row - first row from down which all cells are empty
        self.empty_row = self.r - 1

    def init_field(self):
        field = []
        for r in range(self.r):
            field.append([0] * self.c)
        self.field = field

    def print_field(self, field=False):
        if not field:
            field = self.field
        print('====================================')
        for line in field:
            res = ''
            for cell in line:
                res += str(cell)
            print(res)
        print('====================================')

    def check_field(self):
        remove_rows = []

        # looking for full rows
        for i in range(self.r - 1, self.empty_row, -1):
            full_row = True
            for cell in self.field[i]:
                if not cell:
                    full_row = False
                    break
            if full_row:
                remove_rows.append(i)

        # removing full rows
        for i in range(self.r - 1, self.empty_row, -1):
            moved = False
            if i in remove_rows:
                for j in range(i - 1, self.empty_row, -1):
                    if j not in remove_rows:
                        # move cells from row j to row i
                        self.move_row_down(j, i)
                        moved = True
                        # this row was moved down
                        # need to put there something from higher row
                        remove_rows.append(j)
                        break
                # there are not any rows with full cells
                # so fill this row with empty cells
                if not moved:
                    for k in range(self.c):
                        self.field[i][k] = 0

        self.empty_row += len(remove_rows)
        # is it even possible?
        if self.empty_row > self.r:
            self.empty_row = self.r
        return

    def move_row_down(self, from_r, to_r):
        for i in range(self.c):
            self.field[to_r][i] = self.field[from_r][i]
            self.field[from_r][i] = 0


#TODO remove this
from copy import deepcopy


def ptf(tf, obj):
    f = deepcopy(tf)
    print('++++++++++++++++++++++++++++++')
    for coord in obj.data['coordinates']:
        f[coord[0]][coord[1]] = 'x'
    for line in f:
        res = ''
        for cell in line:
            res += str(cell)
        print(res)
    print('++++++++++++++++++++++++++++++')
    return
#TODO END_REMOVE


def main():
    game = Tetris(10, 5)
    game.empty_row = 9
    f = Figure(3, game)
    f.move_down()
    f.move_down()
    f.move_down()
    f.move_down()
    f.move_right()
    f.rotate(game.field)
    ptf(game.field[:], f)
    f.rotate(game.field)
    ptf(game.field[:], f)
    f.print_figure()
    return


if __name__ == "__main__":
    main()
