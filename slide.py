#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import json
import tkinter as tk


class Slide():
    # TODO change it
    PATH = './data/'

    def __init__(self, size=4):
        self.size = size
        self.__init_field()

    def __init_field(self):
        '''Creating field'''
        numbers = [i for i in range(self.size**2)]
        random.shuffle(numbers)
        self.field = []
        i = 0
        for row in range(self.size):
            self.field.append([0] * self.size)
            for column in range(self.size):
                self.field[row][column] = numbers[i]
                i += 1

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

    def empty_cell_pos(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == 0:
                    return (i, j)

    def move(self, dest):
        #self.check_field()
        moved = False
        row, column = self.empty_cell_pos()

        if dest == 'left':
            # is it possible to move cell?
            if column == self.size - 1:
                return
            self.field[row][column] = self.field[row][column + 1]
            self.field[row][column + 1] = 0
        elif dest == 'right':
            # is it possible to move cell?
            if column == 0:
                return
            self.field[row][column] = self.field[row][column - 1]
            self.field[row][column - 1] = 0
        elif dest == 'up':
            # is it possible to move cell?
            if row == self.size - 1:
                return
            self.field[row][column] = self.field[row + 1][column]
            self.field[row + 1][column] = 0
        else:
            # is it possible to move cell?
            if row == 0:
                return
            self.field[row][column] = self.field[row - 1][column]
            self.field[row - 1][column] = 0
        self.check_field()
        self.print_ui_field()

    def check_field(self):
        num = 1
        for i in range(self.size):
            for j in range(self.size):
                if not self.field[i][j] == num:
                    return False
                num += 1
                if num == self.size**2 - 1:
                    print('You have win!!!')
                    exit()

    def save_game(self):
        with open(self.PATH + 'save_slide.txt', 'w') as f:
            json.dump(self.field, f)

    def load_game(self):
        with open(self.PATH + 'save_slide.txt', 'r') as f:
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
                    self.ui_field[i][j].config(text=self.field[i][j])
                else:
                    # empty cell
                    self.ui_field[i][j].config(text='')


def main():
    g = Slide(5)
    g.init_ui()


if __name__ == "__main__":
    main()
