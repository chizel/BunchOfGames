#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import json
import tkinter as tk
import time


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
        # user's score
        self.score = 0
        # cell that was selected for move
        self.selected_cell = None

    def generate_field(self):
        '''Creating new field'''
        field = []

        for row in range(self.size_r):
            new_row = []
            for column in range(self.size_r):
                cell = random.choice(self.items)
                new_row.append(cell)
            field.append(new_row)
        self.field = field[:]
        self.init_ui()

    def colorize(self, num, gui=False):
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

    def check_row(self, row, column, min_length=3):
        '''Looking for chains in all rows starting from [row, columng].'''
        cell = self.field[row][column]
        chain_length = 1
        start = column
        # list with chains' data
        res = []

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

    def check_column(self, row, column, min_length=3):
        '''Looking for chains in all columns starting from [row, columng].'''
        cell = self.field[row][column]
        chain_length = 1
        start = row
        # list with chains' data
        res = []

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
        '''Checking field for chains in rows and columns, removing them'''
        # if we need to check field something had happend to it, so print it
        self.print_ui_field()
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
            self.print_ui_field()
            self.update_score(score)
            print('Your score is: ', self.score)
            self.move_down_cells()
            return True
        else:
            return False

    def fill_cells(self):
        '''Generate values for empty cells'''
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
        exchanging cells values and checking is move make sense
        e.g. after moving there is at least one chain'''
        fr, fc = from_coord
        tr, tc = to_coord

        # is coordinates are in borders of the field
        if fr >= self.size_r and tr >= self.size_r:
            return
        elif fc >= self.size_c and tc >= self.size_c:
            return

        # are cells neighbours?
        if fr == tr:
            if abs(fc - tc) != 1:
                return
        elif fc == tc:
            if abs(fr - tr) != 1:
                return
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
        self.print_ui_field()
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
        # TODO save score
        with open(self.PATH + 'save.txt', 'w') as f:
            json.dump(self.field, f)

    def load_game(self):
        '''Loading saved game'''
        # TODO check is saving exists
        with open(self.PATH + 'save.txt', 'r') as f:
            self.field = json.load(f)
        # checking loaded data
        self.size_r = len(self.field)
        self.size_c = len(self.field[0])
        for line in self.field:
            if len(line) != self.size_c:
                print('Error! Loaded game has wrong data! (number of columns \
                       in each row aren\'t equal.)')
                exit()
        self.print_ui_field()
        #self.print_field()

    def init_ui(self):
        '''initializing user interface'''
        self.root = tk.Tk()
        self.root.minsize(500, 500)
        self.root.maxsize(500, 500)

        self.main_frame = tk.Frame(
            self.root,
            width=450,
            height=450,
            )

        self.main_frame.place(x=0, y=0)

        # menu
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Menu', menu=file_menu)

        #file_menu.add_command(label='New game', command=self.new_game)
        file_menu.add_command(label='Save', command=self.save_game)
        file_menu.add_command(label='Load', command=self.load_game)
        #file_menu.add_command(label='Settings', command=self.settings)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.root.destroy)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Help', menu=help_menu)
        #help_menu.add_command(label='Help', command=self.show_help)
        #help_menu.add_command(label='About', command=self.show_about)

        self.root.config(menu=menu_bar)
        # end menu

        # key bindings
       # self.main_frame.bind('<Enter>', lambda e: self.move('select'))
       # self.main_frame.bind('<Enter>', lambda e: self.move('select'))
        #self.main_frame.bind('<Right>', lambda e: self.move('right'))
        #self.main_frame.bind('<Left>', lambda e: self.move('left'))
        #self.main_frame.bind('<Up>', lambda e: self.move('up'))
       # self.main_frame.bind('<Down>', lambda e: self.move('down'))
        self.root.bind('<Control-s>', lambda e: self.save_game())
        self.root.bind('<Control-l>', lambda e: self.load_game())
        self.root.bind('<Control-q>', lambda e: self.root.destroy())

        # creating field
        self.ui_field = []

        for i in range(self.size_r):
            self.ui_field.append([])

            for j in range(self.size_c):
                # creating cell
                self.create_cell(i, j)
        self.main_frame.focus()
        #self.print_ui_field()
        self.check_field()
        self.root.mainloop()

    def create_cell(self, row, column):
        self.ui_field[row].append(
            tk.Label(
                self.main_frame,
                font=14,
                width=4,
                height=3,
                justify=tk.CENTER,
                relief=tk.RAISED,
                bd=1,
                bg='#F7CD8B'
                )
            )
        self.ui_field[row][column].grid(row=row, column=column)
        self.ui_field[row][column].bind(
            '<Button-1>',
            lambda e: self.select_cell(row, column))

    def select_cell(self, row, column):
        if self.selected_cell:
            # cell was selected, check is it possible to exchange value
            # with current on
            r,c = self.selected_cell
            self.ui_field[r][c].config(bg='#F7CD8B')
            self.exchange_cells(self.selected_cell, [row, column])
            self.selected_cell = None
        else:
            # save current cell's coordinates
            self.selected_cell = (row, column)
            self.ui_field[row][column].config(bg='#F2B6EC')

    def print_ui_field(self):
        '''updating values in the field'''
        for r in range(self.size_r):
            for c in range(self.size_c):
                if self.field[r][c]:
                    fgcolor = self.colorize(self.field[r][c], gui=True)
                    self.ui_field[r][c].config(
                        text=self.field[r][c],
                        fg=fgcolor)
                else:
                    # empty cell
                    self.ui_field[r][c].config(text='')


def main():
    mg = game(6, 6)
    mg.generate_field()
    exit()
    while True:
        s = input('x y from x y to\n')
        if s == 'l':
            mg.load()
            #mg.print_field()
            mg.print_ui_field()
        elif len(s) == 4:
            fr = int(s[0])
            fc = int(s[1])
            tr = int(s[2])
            tc = int(s[3])
            mg.exchange_cells([fr, fc], [tr, tc])
            mg.check_field_for_moves()
        else:
            #mg.print_field()
            mg.print_ui_field()
    return


if __name__ == "__main__":
    main()
