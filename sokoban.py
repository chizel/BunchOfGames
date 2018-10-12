#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import tkinter as tk


# 1 box: move - true
# 2 wall: move - false
# 3 teleport:move - false

class Sokoban():
    # TODO change it
    PATH = './data/'

    def __init__(self, num_r, num_c):
        self.num_r = num_r
        self.num_c = num_c
        self.__init_field()
        self.player_pos = [0, 0]

    def __init_field(self):
        '''Creating empty field'''
        tmp_line = [0 for i in range(self.num_r)]
        self.field = [tmp_line[:] for i in range(self.num_c)]

    def print_field(self):
        for line in self.field:
            result = '|'
            for cell in line:
                if cell:
                    result += '{:^4}'.format(str(cell))
                else:
                    result += '    '
                result += '|'
            print(result)
        print('===============')

    def move_object(self, row, column, coord):
        '''moving object to neighbour cell'''
        # is it possible to move?
        if self.field[row][column] != 1:
            return

        ar, ac = coord
        if self.field[row + ar][column + ac] == 0:
            self.field[row + ar][column + ac] = self.field[row][column]
            self.field[row][column] = 0
            return True
        return False

    def move_player(self, dest):
        '''moving player in dest direction'''
        row, column = self.player_pos

        if dest == 'left':
            # is it possible to move here?
            if column == 0:
                return False

            # destination cell's empty, move player there
            if self.field[row][column - 1] == 0:
                self.player_pos[1] -= 1
                return True

            # there is no space behind object - nowhere to move it
            if column == 1:
                return False

            # destination cell isn't empty, check is it possible to move
            # object in the cell
            moved = self.move_object(row, column - 1, (0, -1))

            if moved:
                self.player_pos[1] -= 1
                return True
        elif dest == 'right':
            # is it possible to move here?
            if column == self.num_c - 1:
                return False

            # destination cell's empty, move player there
            if self.field[row][column + 1] == 0:
                self.player_pos[1] += 1
                return True

            # there is no space behind object - nowhere to move it
            if column == self.num_c - 2:
                return False

            # destination cell isn't empty, check is it possible to move
            # object in the cell
            moved = self.move_object(row, column + 1, (0, 1))

            if moved:
                self.player_pos[1] += 1
                return True
        elif dest == 'up':
            # is it possible to move here?
            if row == 0:
                return False

            # destination cell's empty, move player there
            if self.field[row - 1][column] == 0:
                self.player_pos[0] -= 1
                return True

            # there is no space behind object - nowhere to move it
            if row == 1:
                return False

            # destination cell isn't empty, check is it possible to move
            # object in the cell
            moved = self.move_object(row - 1, column, (-1, 0))

            if moved:
                self.player_pos[0] -= 1
                return True
        else:
            # is it possible to move here?
            if row == self.num_r - 1:
                return False

            # destination cell's empty, move player there
            if self.field[row + 1][column] == 0:
                self.player_pos[0] += 1
                return True

            # there is no space behind object - nowhere to move it
            if row == self.num_r - 2:
                return False

            # destination cell isn't empty, check is it possible to move
            # object in the cell
            moved = self.move_object(row + 1, column, (1, 0))

            if moved:
                self.player_pos[0] += 1
                return True

    def move(self, dest):
        moved = self.move_player(dest)
        if moved:
            self.check_field()
            self.print_ui_field()

    def check_field(self):
        '''checking is all objects in right positions'''
        pass

    def save_game(self):
        #TODO save player's position!!!
        with open(self.PATH + 'save_2048.txt', 'w') as f:
            json.dump(self.field, f)

    def load_game(self):
        with open(self.PATH + 'save_2048.txt', 'r') as f:
            self.field = json.load(f)
            self.size = len(self.field)
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
        self.main_frame.bind('<Right>', lambda e: self.move('right'))
        self.main_frame.bind('<Left>', lambda e: self.move('left'))
        self.main_frame.bind('<Up>', lambda e: self.move('up'))
        self.main_frame.bind('<Down>', lambda e: self.move('down'))
        self.root.bind('<Control-s>', lambda e: self.save_game())
        self.root.bind('<Control-l>', lambda e: self.load_game())
        self.root.bind('<Control-q>', lambda e: self.root.destroy())

        # creating field
        self.ui_field = []

        for i in range(self.num_r):
            self.ui_field.append([])

            for j in range(self.num_c):
                # creating cell
                self.ui_field[i].append(
                    tk.Label(
                        self.main_frame,
                        font=14,
                        width=4,
                        height=3,
                        justify=tk.CENTER,
                        relief=tk.RAISED,
                        bd=1,
                        bg='#D7FFCB'
                        )
                    )
                self.ui_field[i][j].grid(row=i, column=j)
        self.main_frame.focus()
        self.print_ui_field()
        self.root.mainloop()

    def print_ui_field(self):
        '''updating values in the field'''
        for i in range(self.num_r):
            for j in range(self.num_c):
                if self.field[i][j]:
                    self.ui_field[i][j].config(text=self.field[i][j])
                else:
                    # empty cell
                    self.ui_field[i][j].config(text='')
        row, column = self.player_pos
        self.ui_field[row][column].config(text='*')


def main():
    g = Sokoban(7, 7)
    g.player_pos = [3, 3]
    g.field[0][0] = 2
    g.field[0][1] = 2
    g.field[0][2] = 2
    g.field[1][0] = 2
    g.field[1][2] = 2
    g.field[3][1] = 1
    g.field[3][2] = 2
    g.field[3][5] = 1
    g.init_ui()


if __name__ == "__main__":
    main()
