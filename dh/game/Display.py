from ..lib import libtcodpy as libtcod
#Player import may be removed in future for this class


class Display():

    def __init__(self):
        '''initialize game console'''
        #set font for game
        libtcod.console_set_custom_font('dh/assets/terminal10x10_gs_tc.png',
                                        libtcod.FONT_TYPE_GREYSCALE |
                                        libtcod.FONT_LAYOUT_TCOD)
        #init window
        self.screen_width = 80
        self.screen_height = 80
        libtcod.console_init_root(self.screen_width, self.screen_height, 'deadhack', False)
        libtcod.console_set_foreground_color(0, libtcod.white)
        #flush screen to viewport
        libtcod.console_flush()
        #setup offscreen console
        self.con = libtcod.console_new(self.screen_width, self.screen_height)

    def draw(self, mode, player):
        """ draw the screen pre-blit step 1 tut"""
        #if player has moved from last position
        libtcod.console_print_left(self.con, player.x, player.y, libtcod.BKGND_NONE, '@')
        #save this position for next iteration
        libtcod.console_blit(self.con, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)
        libtcod.console_flush()

    def clear(self, mode, player):
        '''ghetto clear used in step 1 of tut pre-blit'''
        libtcod.console_print_left(self.con, player.x, player.y, libtcod.BKGND_NONE, ' ')
        libtcod.console_blit(self.con, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)
        libtcod.console_flush()

    # logic for knowing main window is still open
    # used in main game loop
    #

    def display_closed(self):
        return libtcod.console_is_window_closed()

    #
    # push visual changes to screen 'viewport'
    #
    def flush(self):
        libtcod.console_flush()
