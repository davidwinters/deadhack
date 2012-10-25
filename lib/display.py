from lib import libtcodpy as libtcod

#
# __init__
#
# sets up graphics and draws it
#
def __init__():
    
    #set font for game
    libtcod.console_set_custom_font('terminal10x10_gs_tc.png',
                                    libtcod.FONT_TYPE_GREYSCALE |
                                    libtcod.FONT_LAYOUT_TCOD)
    #init window
    screen_width = 80
    screen_height = 80
    libtcod.console_init_root(screen_width, screen_height, 'deadhack', False) 
