import libtcodpy as libtcod

#Some Parameters

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

"""MOVING AROUND"""
#players cooridnates
def handle_keys():
	global playerx, playery
	
	#console controls 
	key = libtcod.console_wait_for_keypress(True) # THIS LINE IS SPECIFIC FOR TURN BASED

	if key.vk == libtcod.KEY_ENTER and key.lalt:
		#ALT+ENTER toggle fullscreen
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
	
	elif key.vk == libtcod.KEY_ESCAPE:
		return  True # exit game


	#movement keys
	#is_key_pressed is supposed to be for real-time and check_for_keypress is for TURN BASED 
	#but it behaved strangely if i did not use is_key_pressed

	if libtcod.console_is_key_pressed(libtcod.KEY_UP):
		playery -= 1
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		playery += 1
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		playerx -= 1
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		playerx += 1

	

"""DRAW OUR SHIT"""
libtcod.console_set_custom_font('terminal10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)

playerx = SCREEN_WIDTH/2
playery = SCREEN_HEIGHT/2

#Main Loop 
while not libtcod.console_is_window_closed():
	#set font color
	libtcod.console_set_foreground_color(0,libtcod.white)

	#make our man
	libtcod.console_print_left(0,playerx,playery, libtcod.BKGND_NONE, '@')

	#some other shit, flushing the console?
	libtcod.console_flush()

	#clear off the @ ghosts created by movement
	libtcod.console_print_left(0, playerx, playery, libtcod.BKGND_NONE, ' ')

	#handle keys
	exit = handle_keys()
	if exit:
		break