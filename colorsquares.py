#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import json
import tkinter as tk


class ColorSquare():
    PATH = './data/'

    def __init__(self, size_r, size_c, colors=5):
        if colors > 5:
            print('Sorry, to many colors!')
            exit()
        # generating colors
        self.colors = [i for i in range(1, colors + 1)]
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
            new_row = []
            for column in range(self.size_c):
                cell = random.choice(self.colors)
                new_row.append(cell)
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
        for row in self.field:
            res_row = '\033[1m'
            res_row += str(i)
            res_row += '\033[0m'
            for cell in row:
                res_row += self.colorize(cell)
            print(res_row)
            i += 1
        print('__________________________')

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
        self.move_left_cells()

    def move_left_cells(self):
        '''Move columns to the left'''
        moved = False

        for c_id in range(self.size_c):
            if not self.field[-1][c_id]:
                # current column is empty move row from the right here

                # looking for not empty column
                for j in range(c_id + 1, self.size_c):
                    if not self.field[-1][j]:
                        continue

                    # move column to the left
                    moved = True
                    for r_id in range(self.size_r - 1, -1, -1):
                        if not self.field[r_id][j]:
                            # upper cells are empty, nothing to do here
                            break
                        self.field[r_id][c_id] = self.field[r_id][j]
                        self.field[r_id][j] = 0
                    break

                if not moved:
                    return
                moved = False

    def find_all_squares(self, row, column, cells):
        base_cell = self.field[row][column]
        cells.add((row, column))

        if (row + 1 < self.size_r and
                self.field[row + 1][column] == base_cell and
                (row + 1, column) not in cells):
            cells = self.find_all_squares(row + 1, column, cells)

        if (row - 1 >= 0 and self.field[row - 1][column] == base_cell and
                (row - 1, column) not in cells):
            cells = self.find_all_squares(row - 1, column, cells)

        if (column + 1 < self.size_c and
                self.field[row][column + 1] == base_cell and
                (row, column + 1) not in cells):
            cells = self.find_all_squares(row, column + 1, cells)

        if (column - 1 >= 0 and self.field[row][column - 1] == base_cell and
                (row, column - 1) not in cells):
            cells = self.find_all_squares(row, column - 1, cells)
        return cells

    def select_cell(self, row, column):
        if not self.field[row][column]:
            # cell is empty nothing to do here
            return

        cells = set()
        cells = self.find_all_squares(row, column, cells)
        self.update_score(len(cells))
        if len(cells) < 3:
            return
        for cell in cells:
            self.field[cell[0]][cell[1]] = 0
        self.move_down_cells()
        self.print_ui_field()
        return

    def update_score(self, score):
        '''update score'''
        # TODO develop better algorithm for updating score
        # more cells was destroyed - more points user get
        if not score:
            print('here')
            return
        mult = score % 10
        if mult:
            score *= mult
        else:
            score *= 10
        self.score += score

    def new_game(self):
        self.__init__(self.size_r, self.size_c, len(self.colors))
        self.print_ui_field()

    def save_game(self):
        '''Saving game to a file'''
        # TODO save score
        with open(self.PATH + 'save_colosquare.txt', 'w') as f:
            json.dump(self.field, f)

    def load_game(self):
        '''Loading saved game'''
        # TODO check is saving exists
        with open(self.PATH + 'save_colosquare.txt', 'r') as f:
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

        file_menu.add_command(label='New game', command=self.new_game)
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
        self.root.bind('<Control-s>', lambda e: self.save_game())
        self.root.bind('<Control-l>', lambda e: self.load_game())
        self.root.bind('<Control-q>', lambda e: self.root.destroy())

        # creating field
        self.ui_field = []

        for r_id in range(self.size_r):
            self.ui_field.append([])

            for c_id in range(self.size_c):
                # creating cell
                self.create_cell(r_id, c_id)
                self.ui_field[r_id][c_id].grid(row=r_id, column=c_id)

        self.main_frame.focus()
        self.print_ui_field()
        self.root.mainloop()

    def create_cell(self, row, column):
        '''creating new cell'''
        self.ui_field[row].append(
            tk.Label(
                self.main_frame,
                font=14,
                width=1,
                height=1,
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

    def print_ui_field(self):
        '''updating values in the field'''
        for r_id in range(self.size_r):
            for c_id in range(self.size_c):
                if self.field[r_id][c_id]:
                    bg_color = self.colorize(self.field[r_id][c_id], gui=True)
                    self.ui_field[r_id][c_id].config(bg=bg_color)
                else:
                    # empty cell
                    self.ui_field[r_id][c_id].config(bg='white')


def main():
    mg = ColorSquare(20, 30, 3)
    mg.init_ui()
    mg.print_ui_field()
    return

    # cli
    while True:
        s = input('x y of the cell: \n')
        s = s.split()
        if s == 'l':
            mg.load()
        else:
            try:
                r = int(s[0])
                c = int(s[1])
                mg.select_cell(r, c)
            except:
                print('wrong data')
        mg.print_field()


if __name__ == "__main__":
    main()
