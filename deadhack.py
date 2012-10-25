#
# deadhack
#


#main lib import - has all key functions
#is the main lib we are working with
from lib import libtcodpy as libtcod

from lib import display
#libtcod.console_set_custom_font('terminal10x10_gs_tc.png',
#                                         libtcod.FONT_TYPE_GREYSCALE |
#                                         libtcod.FONT_LAYOUT_TCOD)
#screen_width = 80
#screen_height = 80
#libtcod.console_init_root(screen_width, screen_height,
#                                        'deadhack', False)
display.init()
print 'done!'
