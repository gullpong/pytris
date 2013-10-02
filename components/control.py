'''
created on: 9/30/2013
author: Jinyong Lee
'''

import curses

class Input:
    '''
    User-input handler
    '''
    # input key constants
    NONE, LEFT, RIGHT, SPIN, DROP, EXIT = range(6)

    def __init__( self, stdscr ):
        '''
        Initialize input handler
        '''
        self.stdscr = stdscr
        self.stdscr.keypad( 1 )
        self.stdscr.nodelay( 1 )
        self.val = Input.NONE

    def destroy( self ):
        '''
        Destructor
        '''
        self.stdscr.keypad( 0 )
        self.stdscr.nodelay( 0 )

    def refresh( self ):
        '''
        Refresh user-input
        '''
        c = self.stdscr.getch()

        if c == curses.KEY_LEFT:
            self.val = Input.LEFT
        elif c == curses.KEY_RIGHT:
            self.val = Input.RIGHT
        elif c == curses.KEY_DOWN:
            self.val = Input.DROP
        elif c == curses.KEY_UP:
            self.val = Input.SPIN
        elif c == 27: # escape key
            self.val = Input.EXIT
        else:
            self.val = Input.NONE
