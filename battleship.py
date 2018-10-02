#! /usr/bin/env python3
# -*- coding: utf-8 -*-


class Board():
    def __init(self, size=10):
        '''Board is square'''
        self.size = 10


class Ship():
    def __init__(self, size, x, y, board, position='h'):
        if size > 4 or size < 1:
            print('Error! Size of a ship 1-4 squares!')
            return

        self.size = size
        self.x = x
        self.y = y
        self.position = position
        self.board = board

        if not self.place_ship():
            print('Impossible to place ship here!')
    

    def place_ship_horizontally(self):
        #generate list of ship squares
        for i in range(self.size):
            ship_squares = (x + i, y)

        #check is neighbour squares are empty
        #check left side of a ship
        if x > 0:
            #check is y - first row
            if y > 1:
                if self.board.board[x - 1][y - 1] == 1:
                    return False

            if self.board.board[x - 1][y] == 1:
                return False

            #check is y - last row
            if y < self.board.size - 1:
                if self.board.board[x - 1][y + 1] == 1:
                    return False

        #check right side of a ship
        if x < self.board.size - 1:
            #check is y - first row
            if y > 1:
                if self.board.board[x + self.size][y - 1] == 1:
                    return False

            if self.board.board[x + self.size][y] == 1:
                return False

            #check is y - last row
            if y < self.board.size - 1:
                if self.board.board[x + self.size][y + 1] == 1:
                    return False

        #check upper and lower sides of a ship
        for i in range(self.size):
            if self.board.board[x + i][y] == 1:
                return False

        #placing ship on the board
        self.board.place_ship(ship_squares)
        return True


    def place_ship_vertically(self):
        #generate list of ship squares
        for i in range(self.size):
            ship_squares = (x, y + i)

        #check is neighbour squares are empty
        #check upper sides of a ship
        if y > 0:
            #check is x - first column 
            if x > 1:
                if self.board.board[x - 1][y - 1] == 1:
                    return False

            if self.board.board[x][y - 1] == 1:
                return False

            #check is x - last column 
            if x < self.board.size - 1:
                if self.board.board[x + 1][y - 1] == 1:
                    return False

        #check lower sides of a ship
        if x < self.board.size - 1:
            #check is x - first column 
            if x > 1:
                if self.board.board[x - 1][y + 1] == 1:
                    return False

            if self.board.board[x][y + 1] == 1:
                return False

            #check is x - last column 
            if x < self.board.size - 1:
                if self.board.board[x + 1][y + 1] == 1:
                    return False

        #check left and right sides of a ship
        for i in range(self.size):
            if self.board.board[x + i][y] == 1:
                return False

        #placing ship on the board
        self.board.place_ship(ship_squares)


def main():
    return


if __name__ == "__main__":
    main()
