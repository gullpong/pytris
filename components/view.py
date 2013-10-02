'''
created on: 9/18/2013
author: Jinyong Lee
'''

import curses

class Window:
    '''
    Sub-screen
    '''
    def __init__( self, stdscr, y, x, h, w ):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.h = h
        self.w = w

    def drawstr(self, y, x, str):
        self.stdscr.addstr(y + self.y, x + self.x, str)

    def clear(self):
        for y in range(self.y, self.y + self.h):
            self.stdscr.addstr(y, self.x, ' ' * self.w)


class Screen:
    '''
    Entire view screen
    '''
    def __init__(self, stdscr, board_width, board_height):
        '''
        Initialize main screen
        '''
        self.stdscr = stdscr

        '''
        Create sub screens
        '''
        self.boardscr = Window(self.stdscr, 5, 4, board_height, board_width * 2)
        self.infoscr = Window(self.stdscr, 5, self.boardscr.x + self.boardscr.w + 3, 11, 8)

        self.headscr = Window(self.stdscr, 1, 1, 2, self.infoscr.x + self.infoscr.w - 2)
        self.msgscr = Window(self.stdscr, (self.boardscr.h / 2) - 1 + self.boardscr.y, 1, 3, self.infoscr.x + self.infoscr.w - 2)
        
        self.height = self.boardscr.y + self.boardscr.h
        self.blink = 0

    def destroy( self ):
        '''
        Destructor
        '''
        pass
        
    def draw_frame(self):
        self.msgscr.clear()

        # draw the screen boarder
        self.stdscr.addstr(self.boardscr.y - 1, self.boardscr.x - 1, '+')
        self.stdscr.addstr(self.boardscr.y - 1, self.boardscr.x, '-' * self.boardscr.w)
        self.stdscr.addstr(self.boardscr.y - 1, self.boardscr.x + self.boardscr.w, '+')
        self.stdscr.addstr(self.boardscr.y + self.boardscr.h, self.boardscr.x - 1, '+')
        self.stdscr.addstr(self.boardscr.y + self.boardscr.h, self.boardscr.x, '-' * self.boardscr.w)
        self.stdscr.addstr(self.boardscr.y + self.boardscr.h, self.boardscr.x + self.boardscr.w, '+')
        for r in range(self.boardscr.y, self.boardscr.y + self.boardscr.h):
            self.stdscr.addstr(r, self.boardscr.x - 1, '|')
            self.stdscr.addstr(r, self.boardscr.x + self.boardscr.w, '|')
        
    def show_message( self, message ):
        self.msgscr.clear()

        self.msgscr.drawstr( 0, 0, '=' * self.msgscr.w )
        self.msgscr.drawstr( 1, (self.msgscr.w - len( message )) / 2, message )
        self.msgscr.drawstr( 2, 0, '=' * self.msgscr.w )

    def print_stats(self, stats):
        self.headscr.drawstr( 0, 0, 'Player: ' + str( stats.player ) )

        self.headscr.drawstr( 1, 0, 'Level: ' + str( stats.level ) )
        self.headscr.drawstr( 1, self.headscr.w - 15, 'Score: ' + str( stats.score ) )
        
    def draw_tiles(self, window, y, x, tiles):
        dy, dx = y, x
        for row in tiles:
            for tile in row:
                if tile < 0:
                    if self.blink < 2:
                        window.drawstr(dy, dx, '**')
                    else:
                        window.drawstr(dy, dx, '  ')
                elif tile == 1:
                    window.drawstr(dy, dx, '[]')
                elif tile == 2:
                    window.drawstr(dy, dx, 'II')
                elif tile == 3:
                    window.drawstr(dy, dx, 'HH')
                elif tile == 4:
                    window.drawstr(dy, dx, '%%')
                else:
                    window.drawstr(dy, dx, '  ')
                dx += 2
            dy += 1
            dx = x
    
    def draw_next(self, block, lines):
    	self.infoscr.clear()
    	self.infoscr.drawstr(0, 0, 'Next')
    	self.draw_tiles(self.infoscr, 2, 0, block.tiles)
    	if lines <= 3 and self.blink < 2:
    	    self.infoscr.drawstr(8, 1, ' ')
    	else:
    	    self.infoscr.drawstr(8, 1, str(lines))
    	self.infoscr.drawstr(10, 0, "Lines")
    	self.infoscr.drawstr(11, 0, "Left")
    
    def draw_board(self, board):
        self.draw_tiles(self.boardscr, 0, 0, board.tiles)
    
    def refresh(self):
        # cycle blink flag
        self.blink += 1
        if self.blink >= 4:
            self.blink = 0

        # place the cursor at the bottom of window
        self.stdscr.addstr(self.height + 1, 0, ' ')

        # refresh screen
        self.stdscr.refresh()

