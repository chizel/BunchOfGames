#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import json
import tkinter as tk


class Game2048():
    # TODO change it
    PATH = './data/'

    def __init__(self, size):
        self.size = size
        self.__init_field()

    def __init_field(self):
        '''Creating empty field'''
        tmp_line = [0 for i in range(self.size)]
        self.field = [tmp_line[:] for i in range(self.size)]

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

    def move_check(self):
        '''checking is it possible to move'''
        # check is it possible to move
        # check every row
        for line in self.field:
            for i in range(self.size - 1):
                # this cell's empty, it's possible to move here
                if not line[i]:
                    return
                if line[i] == line[i + 1]:
                    return
            # last cell in the row's empty
            if not line[i + 1]:
                return

        # check every column
        for j in range(self.size):
            for i in range(self.size - 1):
                if self.field[i][j] == self.field[i + 1][j]:
                    return
        self.print_ui_field()
        print('You lose!')
        #exit()

    def gen_numb(self):
        empty_cells = []
        # TODO if cell contain number 2 in it and it can't be moved
        # is still considered not the end of the game

        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] <= 2:
                    empty_cells.append((i, j))
                elif self.field[i][j] == 2048:
                    print('You\'ve win!')

        if not empty_cells:
            print('You lose! (empty_cell is empty :D)')
            exit()

        i, j = random.choice(empty_cells)

        if self.field[i][j]:
            self.field[i][j] = 4
        else:
            self.field[i][j] = 2

    def move(self, dest):
        self.move_check()
        moved = False

        if dest == 'left':
            for i in range(self.size):
                # checking is it possible to join current and right cell
                for j in range(self.size - 1):
                    if self.field[i][j]:
                        for k in range(j + 1, self.size):
                            if self.field[i][k]:
                                if self.field[i][j] == self.field[i][k]:
                                    self.field[i][j] *= 2
                                    self.field[i][k] = 0
                                    moved = True
                                break

                # moving objects in the row to the left side of the field
                for j in range(self.size - 1):
                    if not self.field[i][j]:
                        for k in range(j + 1, self.size):
                            if self.field[i][k]:
                                self.field[i][j] = self.field[i][k]
                                self.field[i][k] = 0
                                moved = True
                                break
        elif dest == 'right':
            for i in range(self.size):
                for j in range(self.size - 1, -1, -1):
                    if self.field[i][j]:
                        for k in range(j - 1, -1, -1):
                            if self.field[i][k]:
                                if self.field[i][j] == self.field[i][k]:
                                    self.field[i][j] *= 2
                                    self.field[i][k] = 0
                                    moved = True
                                break

                # moving objects in the row to the right side of the field
                for j in range(self.size - 1, 0, - 1):
                    if not self.field[i][j]:
                        for k in range(j - 1, -1, -1):
                            if self.field[i][k]:
                                self.field[i][j] = self.field[i][k]
                                self.field[i][k] = 0
                                moved = True
                                break
        elif dest == 'up':
            for j in range(self.size):
                for i in range(self.size - 1):
                    if self.field[i][j]:
                        for k in range(i + 1, self.size):
                            if self.field[k][j]:
                                if self.field[i][j] == self.field[k][j]:
                                    self.field[i][j] *= 2
                                    self.field[k][j] = 0
                                    moved = True
                                break

                # moving objects in the line to the top side of the field
                for i in range(self.size - 1):
                    if not self.field[i][j]:
                        for k in range(i + 1, self.size):
                            if self.field[k][j]:
                                self.field[i][j] = self.field[k][j]
                                self.field[k][j] = 0
                                moved = True
                                break
        else:
            for j in range(self.size):
                for i in range(self.size - 1, -1, -1):
                    if self.field[i][j]:
                        for k in range(i - 1, -1, -1):
                            if self.field[k][j]:
                                if self.field[i][j] == self.field[k][j]:
                                    self.field[i][j] *= 2
                                    self.field[k][j] = 0
                                    moved = True
                                break

                # moving objects in the line to the bottom side of the field
                for i in range(self.size - 1, -1, -1):
                    if not self.field[i][j]:
                        for k in range(i - 1, -1, -1):
                            if self.field[k][j]:
                                self.field[i][j] = self.field[k][j]
                                self.field[k][j] = 0
                                moved = True
                                break
        if moved:
            self.gen_numb()
            self.print_ui_field()

    def save_game(self):
        with open(self.PATH + 'save_2048.txt', 'w') as f:
            json.dump(self.field, f)

    def load_game(self):
        with open(self.PATH + 'save_2048.txt', 'r') as f:
            self.field = json.load(f)
            self.size = len(self.field)
        self.print_ui_field()

    def colorize(self, num):
        if num == 2:
            color = '#E9B96E'
        elif num == 4:
            color = '#AD7FA8'
        elif num == 8:
            color = '#729FCF'
        elif num == 16:
            color = '#FCE94F'
        elif num == 32:
            color = '#FCAF3E'
        elif num == 64:
            color = '#EF2929'
        elif num == 128:
            color = '#F15D37'
        elif num == 256:
            color = '#FF3500'
        elif num == 512:
            color = '#F15D37'
        elif num == 1024:
            color = '#C17D11'
        elif num == 2048:
            color = '#8F5902'
        else:
            color = 'black'
        return color

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

        for i in range(self.size):
            self.ui_field.append([])

            for j in range(self.size):
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
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j]:
                    font_color = self.colorize(self.field[i][j])
                    self.ui_field[i][j].config(fg=font_color)
                    self.ui_field[i][j].config(text=self.field[i][j])
                else:
                    # empty cell
                    self.ui_field[i][j].config(text='')


def main():
    g = Game2048(5)
    g.gen_numb()
    g.gen_numb()
    g.init_ui()


if __name__ == "__main__":
    main()
