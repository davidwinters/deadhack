from ..lib import libtcodpy as libtcod
#Player import may be removed in future for this class
import Player

class Display():

    def __init__(self):
        '''initialize game console'''
        #set font for game
        libtcod.console_set_custom_font('dh/assets/terminal10x10_gs_tc.png',
                                        libtcod.FONT_TYPE_GREYSCALE |
                                        libtcod.FONT_LAYOUT_TCOD)
        #init window
        screen_width = 80
        screen_height = 80
        libtcod.console_init_root(screen_width, screen_height, 'deadhack', False)
        libtcod.console_set_foreground_color(0, libtcod.white)
        #flush screen to viewport
        libtcod.console_flush()
        #setup offscreen console
        self.con = libtcod.console_new(screen_width,screen_height)



    def draw(mode, player):
        """ draw the screen pre-blit step 1 tut"""
        #if player has moved from last position
        libtcod.console_print_left(con, player.x, player.y, libtcod.BKGND_NONE, '@')
        #save this position for next iteration
        libtcod.console_blit(con,0,0,screen_width,screen_height,0,0,0)
        libtcod.console_flush()


    def clear(mode, player):
        '''ghetto clear used in step 1 of tut pre-blit'''
        libtcod.console_print_left(con, player.x, player.y, libtcod.BKGND_NONE, ' ')
        libtcod.console_blit(con,0,0,screen_width,screen_height,0,0,0)
        libtcod.console_flush()

    # logic for knowing main window is still open
    # used in main game loop
    #


    def console():
        return libtcod.console_is_window_closed()

    #
    # push visual changes to screen 'viewport'
    #
    def flush():
        libtcod.console_flush()
