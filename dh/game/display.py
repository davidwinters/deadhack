from ..lib import libtcodpy as libtcod
import Player
#
# __init__
#
# sets up graphics and draws it
#


def init(player):

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

    #initialize playerlast


def draw(mode,player):
    """ draw the screen """
    #if player has moved from last position
    libtcod.console_print_left(0, player.lastx, player.lasty, libtcod.BKGND_NONE, ' ')
    libtcod.console_print_left(0, player.x, player.y, libtcod.BKGND_NONE, '@')
    #save this position for next iteration
    libtcod.console_flush()
#
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
