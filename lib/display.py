from lib import libtcodpy as libtcod

#
# __init__
#
# sets up graphics and draws it
#


def init():

    #set font for game
    libtcod.console_set_custom_font('terminal10x10_gs_tc.png',
                                    libtcod.FONT_TYPE_GREYSCALE |
                                    libtcod.FONT_LAYOUT_TCOD)
    #init window
    screen_width = 80
    screen_height = 80
    libtcod.console_init_root(screen_width, screen_height, 'deadhack', False)
    libtcod.console_set_foreground_color(0, libtcod.white)
    libtcod.console_print_left(0, 1, 1, libtcod.BKGND_NONE, '@')
    libtcod.console_flush()
