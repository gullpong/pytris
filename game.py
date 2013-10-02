'''
created on: 9/18/2013
author: Jinyong Lee
'''

import copy
import time
import random
import curses

from components.profile import Stats
from components.model import Tetriminos
from components.model import Tetriboard
from components.view import Screen
from components.control import Input


class Game:
    '''
    Main game play class
    '''
    
    BLOCK_SCORE = 10                      # score for placing a block
    ROW_SCORE = [100, 300, 600, 1000]     # score for clearing rows

    LEVEL_MAX = 10
    LEVEL_LINES = [20, 20, 18, 18, 15, 15, 12, 12, 10, 5]       # lines-to-complete the level
    LEVEL_DELAY = [80, 60, 40, 32, 24, 16, 10,  8,  5, 3]       # block floating delay (i.e. game speed)

    def __init__(self):
        '''
        Constructor
        '''
        self.stats = None
        self.board = None
        
        self.cur_block = None
        self.next_block = None   

        self.fall_counter = 0
        self.line_counter = 0
        self.pause_counter = 0
        self.pause_callback = None
        
        self.message = None
        
        self.exit = False
            

    def get_level_idx(self):
        if self.stats.level >= Game.LEVEL_MAX:
            return Game.LEVEL_MAX - 1
        else:
            return self.stats.level - 1


    def game_over(self):
        self.exit = True

                    
    def next_level(self):
        self.stats.level += 1
        self.board.reset()
        self.message = None
        self.line_counter = Game.LEVEL_LINES[self.get_level_idx()]
    
    def clear_rows(self):
        self.board.clear_rows()
        
        if self.line_counter <= 0:
            self.message = 'Next Level'
            self.pause_counter = 60
            self.pause_callback = self.next_level
       

    def reload_block(self):
        if self.cur_block is None:
            self.cur_block = self.next_block
            self.cur_block.deploy( Game.LEVEL_DELAY[self.get_level_idx()], self.board.width )
            self.next_block = None
        
        if self.next_block is None:
            self.next_block = Tetriminos()

        # check the end condition
        if self.cur_block.check_collision(self.board) is True:
            self.message = 'GAME  OVER'
            self.pause_counter = 30
            self.pause_callback = self.game_over


    def place_block(self):
        # place the current block on the board
        self.cur_block.place( self.board )
        self.cur_block = None
        
        self.stats.score += Game.BLOCK_SCORE        
        complete_rows = self.board.check_rows()
        if len(complete_rows) > 0:
            self.stats.score += Game.ROW_SCORE[len(complete_rows) - 1]
            self.board.mark_rows(complete_rows)
            self.pause_counter = 16
            self.pause_callback = self.clear_rows
            self.line_counter -= len(complete_rows)
            if self.line_counter < 0:
                self.line_counter = 0

        
    def fall_block(self):
        # fall the current block
        if self.cur_block.fall() is False:
            return

        # create a shadow block to do a collision test
        shadow_block = copy.deepcopy(self.cur_block)
        
        '''
        Drop the block three times as fast
        '''
        for i in range(2):
            shadow_block.y += 1        
            if shadow_block.check_collision(self.board) is True:
                # place the current block
                self.place_block()
                break
            else:
                # let the current block fall
                self.cur_block.y += 1

            # check if it's natural falling
            if not self.cur_block.is_dropping():
                break


    def drop_block( self ):
        # drop the current block
        self.cur_block.drop()
        
    def spin_block(self):
        # create a shadow block to do a collision test
        shadow_block = copy.deepcopy(self.cur_block)
        shadow_block.spin( 1 )
        if shadow_block.check_collision(self.board) is False:
            # spin the current block
            self.cur_block.spin( 1 )

        
    def move_block(self, disposition):
        # create a shadow block to do a collision test
        shadow_block = copy.deepcopy(self.cur_block)
        shadow_block.x += disposition        
        if shadow_block.check_collision(self.board) is False:
            # move the current block
            self.cur_block.x += disposition
        
        
    def handle_input(self):

        # refresh the user input
        self.control.refresh()

        # check if the current block is dropping
        if self.cur_block.is_dropping():
            return

        # process
        if self.control.val == Input.LEFT:
            self.move_block(-1)
        elif self.control.val == Input.RIGHT:
            self.move_block(1)
        elif self.control.val == Input.SPIN:
            self.spin_block()
        elif self.control.val == Input.DROP:
            self.drop_block()
        elif self.control.val == Input.EXIT:
            self.game_over()
            
            
    def update_screen(self):
        # create a tile board for display 
        disp_board = copy.deepcopy(self.board)
        
        if self.cur_block is not None:
            # place the current block on the display board
            self.cur_block.place(disp_board)
        
        self.view.draw_frame()
        
        self.view.print_stats(self.stats)
        self.view.draw_next(self.next_block, self.line_counter)
        self.view.draw_board(disp_board)
        
        if self.message is not None:
            self.view.show_message(self.message)

        self.view.refresh()


    def start(self):
        '''
        Initialize player profile
        '''
        print ' '
        player = raw_input( 'Input Player Name (enter to use default name "Jin Lee"): ')
        if len(player.strip()) < 1:
            player = 'Jin Lee'
        level = 1
        bw, bh = 10, 20    # board size

        '''
        Initialize system
        '''
        # initialize the random seed
        random.seed()

        # initialize curses
        stdscr = curses.initscr()
        curses.nocbreak()
        curses.noecho()

        '''
        Initialize game objects
        '''
        self.view = Screen( stdscr, bw, bh )
        self.control = Input( stdscr )
        
        self.stats = Stats( player = player, level = level )
        self.board = Tetriboard(bw, bh)
        self.next_block = Tetriminos()

        self.line_counter = Game.LEVEL_LINES[self.get_level_idx()]


    def finish( self ):
        '''
        Destroy game objects
        '''
        self.view.destroy()
        self.control.destroy()

        '''
        Terminate system
        '''
        curses.echo()
        curses.cbreak()
        #curses.endwin()
        

    def run(self):
        '''
        Start game
        '''
        self.start()
    
        '''
        Main game loop
        '''
        while self.exit is False:

            # pause
            if self.pause_counter > 0:
                self.pause_counter -= 1
                if self.pause_counter == 0:
                    self.pause_callback()
            else:
                # block cycle
                self.reload_block()
                    
                # user input
                self.handle_input()
                
                # block fall
                self.fall_block()
                
            # update the screen
            self.update_screen()
            
            # sleep frame
            time.sleep( 1.0 / 60 )      # 60 FPS

        '''
        Finish game
        '''
        self.finish()

'''
the main route
'''
if __name__ == '__main__':    
    # initialize the game
    game = Game()

    # run the game
    game.run()
    
