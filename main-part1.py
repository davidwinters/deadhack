import libtcodpy as libtcod

#Some Parameters

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

libtcod.console_set_custom_font('terminal10x10_gs_tc.png',libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)


#Main Loop 
while not libtcod.console_is_window_closed():
	#set font color
	libtcod.console_set_foreground_color(0,libtcod.white)

	#make our man
	libtcod.console_print_left(0,1,1, libtcod.BKGND_NONE, '@')

	#some other shit, flushing the console?
	libtcod.console_flush()

