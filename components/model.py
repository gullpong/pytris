'''
created on: 9/20/2013
author: Jinyong Lee
'''

import random

class Tetriminos:
    '''
    User-manipulable Tetris block
    '''
    SHAPE_NAMES = ['i', 'j', 'l', 'o', 's', 't', 'z']
    
    def __init__(self, shape=None, color=None):
        '''
        Constructor
        '''
        self.x = self.y = -1
        self.float_delay = -1
        self.float_counter = 0
        
        # randomly decide the shape/color
        if shape is None:
            shape = Tetriminos.SHAPE_NAMES[random.randrange(0, len(Tetriminos.SHAPE_NAMES))]            
        if color is None:
            color = random.randrange(1, 5)
        
        # initialize titles
        if shape == 'i':
            self.tiles = [[0, color, 0],[0, color, 0],[0, color, 0],[0, color, 0]]
        if shape == 'j':
            self.tiles = [[color,color,color],[0,0,color]]
        if shape == 'l':
            self.tiles = [[color,color,color],[color,0,0]]
        if shape == 'o':
            self.tiles = [[color,color],[color,color]]
        if shape == 's':
            self.tiles = [[0,color,color],[color,color,0]]
        if shape == 't':
            self.tiles = [[color,color,color],[0,color,0]]
        if shape == 'z':
            self.tiles = [[color,color,0],[0,color,color]]

        # reset dimension
        self.reset_dimension()
        
        
    def reset_dimension(self):
        '''
        Reset the dimension of the block
        '''
        self.width = len(self.tiles[0])
        self.height = len(self.tiles)

    def deploy( self, float_delay, field_width ):
        self.x = int(field_width / 2) - int(self.width / 2)
        self.y = 0
        self.float_delay = float_delay
        self.float_counter = self.float_delay

    def fall( self ):
        '''
        Fall the block
        '''
        # decrease block float counter
        self.float_counter -= 1
        if self.float_counter > 0:
            return False

        # reset block float counter
        self.float_counter = self.float_delay
        return True

    def is_dropping( self ):
        if self.float_delay <= 0:
            return True
        else:
            return False

    def drop( self ):
        '''
        Drop the block
        '''
        self.float_counter = self.float_delay = 0


    def spin(self, direction):
        '''
        Spin the block
        '''
        # preserve the original tile shape
        org_tiles = [row[:] for row in self.tiles]        
        rows = self.height
        cols = self.width
        
        # spin the block
        if direction < 0:  # counter-clock wise
            self.tiles = [[org_tiles[rows - j - 1][i] for j in range(rows)] for i in range(cols)]
        else:  # clock wise
            self.tiles = [[org_tiles[j][cols - i - 1] for j in range(rows)] for i in range(cols)]
            
        # reset dimension
        self.reset_dimension()

    def place(self, board):
        # copy the entire tile on the board
        for i in range(self.height):
            row = i + self.y
            for j in range(self.width):
                col = j + self.x

                # skip blank tiles                
                if self.tiles[i][j] == 0:
                    continue              

                # check the bound condition
                if (col < 0 or col >= board.width) or\
                   (row < 0 or row >= board.height):
                    continue

                board.tiles[row][col] = self.tiles[i][j] 

        
    def check_collision(self, board):
        '''
        Check collision
        '''
        collided = False
        
        # check if there is any collision between the block and the board     
        for i in range(self.height):
            row = i + self.y
            for j in range(self.width):
                col = j + self.x
                
                # skip blank tiles
                if self.tiles[i][j] == 0:
                    continue

                # check the bound condition
                if (col < 0 or col >= board.width) or\
                   (row < 0 or row >= board.height):
                    collided = True
                    break

                if board.tiles[row][col] != 0:
                    collided = True
                    break
                
        return collided
        

class Tetriboard:
    '''
    Tetris tile board
    '''
    
    def __init__(self, width, height):
        '''
        Constructor
        '''
        self.width = width
        self.height = height
        
        self.reset()
    
        
    def reset(self):
        self.tiles = [[0 for j in range(self.width)] for i in range(self.height)]        
    
    def check_rows(self):
        complete_rows = []
        
        # search the board to find complete rows
        for i in range(self.height):
            for j in range(self.width):
                if self.tiles[i][j] == 0:
                    break
            else:
                complete_rows.append(i)

        return complete_rows 

    def mark_rows(self, completed_rows):
        for r in completed_rows:
            row = self.tiles[r]
            for j in range(self.width):
                row[j] = -1


    def clear_rows(self):
        for i in range(self.height):
            row = self.tiles[i]
            if row[0] < 0:
                # remove the completed row
                self.tiles.remove(row)
                # append a new row
                self.tiles.insert(0, [0 for j in range(self.width)])

