#! /usr/bin/env python3
# -*- coding: utf-8 -*-


class Fball():
    # empty cell
    CELL = 0
    # cell that only player can clear
    CL_CELL = 1
    WALL = 2
    BALL = 3
    # 4 - enemy that moves
    ENEMY1 = 4
    # 5 - enemy that waits till player go near it
    ENEMY2 = 5
    PLAYER = 6
    objects = [0, 1, 2, 3, 4, 5, 6]

    def __init__(self, size_r, size_c):
        self.size_r = size_r
        self.size_c = size_c
        self.generate_field()
        #self.player = [1, 1]
        #self.field[1][1] = 6
        #self.enemy = [[5, 5],[4, 4]]
        self.enemy_base_line = 0

    def generate_field(self):
        '''Creating new field'''
        self.field = [[0] * self.size_c for _ in range(self.size_r)]

        for r in range(self.size_r):
            self.field[r][0] = self.WALL
            self.field[r][-1] = self.WALL

        for c in range(self.size_c):
            self.field[0][c] = self.WALL
            self.field[-1][c] = self.WALL

    def print_field(self):
        print('__________________________')
        for row in self.field:
            res_row = ''
            for cell in row:
                res_row += str(cell)
            print(res_row)
        print('__________________________')

    def check_neighbours(self, position, what_to_look):
        pr, pc = position
        if self.field[pr][pc + 1] == what_to_look:
            return True
        if self.field[pr][pc - 1] == what_to_look:
            return True
        if self.field[pr + 1][pc] == what_to_look:
            return True
        if self.field[pr - 1][pc] == what_to_look:
            return True
        return False

    def move_player(self, destination):
        '''Move player to neightbour cell (destination)'''
        dr, dc = destination
        #change it!
        exit()
        old_r, old_c = self.player

        # if destination is empty or clearable cell
        if self.field[dr][dc] <= CL_self.CELL:
            # check if we activated an enemy
            #if self.check_neighbours(destination, 5):
                ## TODO activate an enemy
            #    pass

            self.player = destination
            self.field[old_r][old_c] = self.CELL
            self.field[dr][dc] = PLAYER
            return True

        # check if we commited suicide
        if self.field[dr][dc] == self.ENEMY1 or\
                self.field[dr][dc] == self.ENEMY2:
            # we moved to an enemy and were killed by it
            # TODO improve this message and do something with result
            print('You lose!')
            exit()

        return False

    def move_ball_horizontally(self, ball_coord, direction=0):
        '''moves ball left (direction=-1) or right (direction=1),
        self move right (if below this ball another one)
        if possible or left otherwise'''
        br, bc = ball_coord

        print(ball_coord)
        # is it a ball?
        if self.field[br][bc] != self.BALL:
            return False

        # is it self move
        if not direction:
            # is there a ball below this ball
            if self.field[br + 1][bc] != self.BALL:
                return False

            # try to move right
            if self.field[br][bc + 1] == self.CELL and\
                    self.field[br + 1][bc + 1] == self.CELL:
                self.field[br][bc] = self.CELL
                self.field[br + 1][bc + 1] = self.BALL
                self.move_ball_down((br + 1, bc + 1))
                return True

            # try to move left
            if self.field[br][bc - 1] == self.CELL and\
                    self.field[br + 1][bc - 1] == self.CELL:
                self.field[br][bc] = self.CELL
                self.field[br + 1][bc - 1] = self.BALL
                self.move_ball_down((br + 1, bc - 1))
                return True

        new_bc = bc + direction

        # is destination cell is clear
        if self.field[br][new_bc] == self.CELL:
            self.field[br][bc] = self.CELL
            self.field[br][new_bc] = self.BALL
            # check is it possible to move ball down
            if not self.move_ball_down((br, new_bc)):
                self.move_ball_horizontally((br, new_bc))
            return True
        return False

    def move_ball_down(self, ball_coord):
        br, bc = ball_coord

        # is it ball?
        if self.field[br][bc] != self.BALL:
            return False

        # moving down ball
        i = 1
        while self.field[br + i][bc] == self.CELL:
            self.field[br + i][bc] = self.BALL
            self.field[br + i - 1][bc] = self.CELL
            i += 1

        # current ball's row id
        current_br = br + i - 1
        # next cell's row id
        next_cell_r = br + i

        # is there any balls higher than current ball
        j = 1
        while self.field[br - j][bc] == self.BALL:
            self.field[current_br - j][bc] = self.BALL
            self.field[br - j][bc] = self.CELL
            j += 1

        # TODO test it!!!
        # ball killed enemy continue to move ball down if possible
        if self.field[next_cell_r][bc] == self.ENEMY1 or\
                self.field[next_cell_r][bc] == self.ENEMY2:
            self.field[nex_cell_r][bc] = self.BALL
            self.field[current_br][bc] = self.CELL
            self.move_ball_down((next_cell_r, bc))
            return True
here>>>>>>>>>>>>
        if self.field[next_cell_r][bc] == self.PLAYER:
            print('we killed player! game over :(')

        # cell below isn't empty, stop moving ball down
        if self.field[next_cell_r][bc] <= self.WALL:
            print(self.field[br + j - 1][bc])
            exit()
            #self.move_ball_horizontally((br + j - 1, bc))
            # check from up of the stack
            ##########
            #
            # * <===
            #**
            #**
            #########
            return False
        # check is below current ball is another ball
        #self.move_ball_horizontally((current_br, bc))
        return

    #def move_enemy(self, enemy):
        #'''Move enemy to neightbour cell '''
        #if not enemy:
            #exit()

        # 'direction'
        # [1, 1] row - down, column right
        # [-1, -1] row - up, column left
        # old_r, old_c = enemy['position']

        ## destination row and column
        #dr, dc = enemy['position']
        #dc += enemy['direction'][1]
        #print(dr, dc)

        ### where to store and update it?
        ##if self.enemy_base_line != dr:
            ##if self.field[dr - enemy['direction'][0]][dc] == 0:
                ###move there
                ### save coordinate
        ##self.enemy_base_line = dr

        ## if destination is empty cell
        #if self.field[dr][dc] == 0:
            #self.field[old_r][old_c] = 0
            #self.field[dr][dc] = 4
            #enemy['position'] = [dr, dc]
            #return enemy
        ## wall or clearable cell
        #elif self.field[dr][dc] <= 2:
            ## destination column
            #dc = enemy['position'][1]

            ##it's a wall!
            #if self.field[dr + enemy['direction'][0]][dc] == 0:
                ## cell is empty move to it
                #self.field[old_r][old_c] = 0
                #self.field[dr + enemy['direction'][0]][dc] = 4
                #enemy['position'] = [dr + enemy['direction'][0], dc]
                #return enemy
            #elif self.field[dr + enemy['direction'][0]][dc] < 2:
                #print('here')
                ## try to move to previous cell
                #enemy['direction'][1] *= -1
                #return enemy
                # look to cell from what enemy went
                # if it's a wall, look up and if there a wall
                # we're surrounded by walls
                # TODO finish it
            # move to r coordinate (down/up)
        #elif self.field[dr][dc] == 6:
            #print('You lose!')
        #    exit()
        #else:
            # we'are near another enemy
            # what to do?
            #pass
        return False


def main():
    mg = Fball(7, 7)
    mg.field[1][1] = 3
    mg.field[2][1] = 3
    mg.field[3][1] = 3
    mg.field[3][2] = 3
    mg.field[4][1] = 1
    mg.field[4][2] = 1
    mg.print_field()
    mg.move_ball_horizontally([1, 1], direction=0)
    mg.print_field()
#    mg.move_ball_horizontally([5,2], direction=1)
#    mg.print_field()
    exit()
#    enemy = {'position': [1, 1], 'direction': [1, 1]}

    #while True:
        #enemy = mg.move_enemy(enemy)
#        mg.print_field()
        #s = input()
        #char_pos = mg.player[:]
        ## up
        #if s == 'w':
            #char_pos[0] -= 1
            #mg.move_player(char_pos)
        ## down
        #elif s == 's':
            #char_pos[0] += 1
            #mg.move_player(char_pos)
        ## left
        #elif s == 'a':
            #char_pos[1] -= 1
            #mg.move_player(char_pos)
        ## right
        #elif s == 'd':
            #char_pos[1] += 1
            #mg.move_player(char_pos)
        #mg.print_field()

if __name__ == "__main__":
    main()
