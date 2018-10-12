#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random

class Board():
    def __init__(self, size=10):
        '''Board is square'''
        self.size = 10
        self.generate_board()

    def generate_board(self):
        self.board = [[0,] * self.size for _ in range(self.size)]

    def place_ship(self, ship_squares):
        for r, c in ship_squares:
            self.board[r][c] = 1

    def print_board(self):
        for r in range(self.size):
            line = ''
            for c in range(self.size):
                line += str(self.board[r][c])
            print(line)


class Ship():
    def __init__(self, size, r, c, board, position='h'):
        if size > 4 or size < 1:
            print('Error! Size of a ship 1-4 squares!')
            return

        self.size = size
        self.row_id = r
        self.column_id = c
        self.position = position
        self.board = board

        if position == 'h':
            if not self.place_ship_horizontally():
                print('Impossible to place ship here!')
        else:
            if not self.place_ship_vertically():
                print('Impossible to place ship here!')

    def place_ship_vertically(self):
        r = self.row_id
        c = self.column_id
        ship_squares = []

        #generate list of ship squares
        for i in range(self.size):
            ship_squares.append((r + i, c))

        #check is neighbour squares are empty
        #check upper side of a ship
        if r > 0:
            #check is c - first column
            if c > 1:
                if self.board.board[r - 1][c - 1] == 1:
                    return False

            if self.board.board[r - 1][c] == 1:
                return False

            #check is c - last column
            if c < self.board.size - 1:
                if self.board.board[r - 1][c + 1] == 1:
                    return False

        #check lower side of a ship
        if r < self.board.size - 1:
            #check is y - first row
            if c > 1:
                if self.board.board[r + self.size][c - 1] == 1:
                    return False

            if self.board.board[r + self.size][c] == 1:
                return False

            #check is c - last column
            if c < self.board.size - 1:
                if self.board.board[r + self.size][c + 1] == 1:
                    return False

        #check left and right sides of a ship
        for i in range(1, self.size + 1):
            if (self.board.board[r][c + i] == 1 or
                    self.board.board[r][c - i] == 1):
                return False

        #placing ship on the board
        self.board.place_ship(ship_squares)
        return True

    def place_ship_horizontally(self):
        r = self.row_id
        c = self.column_id
        ship_squares = []
        #generate list of ship squares
        for i in range(self.size):
            ship_squares.append((r, c + i))

        #check is neighbour squares are empty
        #check left side of a ship
        if c > 0:
            #check is r - first row
            if r > 1:
                if self.board.board[r - 1][c - 1] == 1:
                    return False

            if self.board.board[r][c - 1] == 1:
                return False

            #check is r - last row
            if r < self.board.size - 1:
                if self.board.board[r + 1][c - 1] == 1:
                    return False

        #check right side of a ship
        if r < self.board.size - 1:
            #check is r - first row
            if r > 1:
                if self.board.board[r - 1][c + 1] == 1:
                    return False

            if self.board.board[r][c + 1] == 1:
                return False

            #check is r - last row
            if r < self.board.size - 1:
                if self.board.board[r + 1][c + 1] == 1:
                    return False

        #check upper and lower sides of a ship
        for i in range(1, self.size + 1):
            if (self.board.board[r + i][c] == 1 or
                    self.board.board[r - i][c] == 1):
                return False

        #placing ship on the board
        self.board.place_ship(ship_squares)
        return True


class BSGame():
    def __init__(self, config):
        self.board = Board(config['board_size'])
        self.ships_info = config['ships']
        self.ships = []

        for ship_size, ship_count in self.ships_info:
            for _ in range(ship_count):
                spips.append(self.generate_ship(ship_size))

    def generate_ship(self, size):
        position = random.choice(('h', 'v'))
        ship = {}
        ship['position'] = position
        ship['size'] = size 
        #generate coordinates
        #ship['r'] =
        #ship['c'] =
        return ship

    def shoot(self, r, c):
        if self.board.board[r][c] == 1:
            #shot was successful
            return True
        return False


def main(): '''add mine? when you shoot it you need to sink one your own ship'''
    config = {}
    config['board_size'] = 10
    #(ship size, number of ships)
    config['ships'] = [(4, 1), (3, 2), (2, 3), (1, 4)]
    bsgame = BSGame(config)
    board = Board(10)
    ship1 = Ship(2, 1, 1, board)
    #ship2 = Ship(1, 2, 1, board)
    #ship2 = Ship(1, 2, 2, board)
    #ship2 = Ship(1, 3, 2, board)
    ship2 = Ship(1, 3, 3, board)
    ship2 = Ship(3, 5, 4, board, position='v')
    board.print_board()
    return


if __name__ == "__main__":
    main()
