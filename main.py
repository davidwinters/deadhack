import libtcodpy as libtcod

#########################################
#  1 DEFINE PARAMETERS                  #
#                                       #
#########################################

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
MAP_WIDTH = 80
MAP_HEIGHT = 45

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)


#########################################
#  2 CREATE OUR CLASSES AND FUNCTIONS   #
#                                       #
#########################################

class Tile(object):
	#tiles on the map
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked

		#blcoked tiles also block sight
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight


class Thing(object):
	#create a generic class for pc, npc, monsters, items etc.
	def __init__(self, x, y, char, color):
		self.x = x
		self.y = y
		self.char = char
		self.color = color

	def move(self,dx,dy):

		if not map[self.x +dx][self.y + dy].blocked: #check that the tile is not blocked
			#move by given ammount
			self.x += dx
			self.y += dy

	def draw(self):
		#set the color and then draw the character that represents this object at its position
		libtcod.console_set_foreground_color(con, self.color)
		libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
		
	def clear(self):
		#erase the ghosts when moving around
		libtcod.console_put_char_ex(con, self.x, self.y, '.', libtcod.light_grey, libtcod.BKGND_NONE)
		
			
def make_map():
	global map

	#fill map with unblocked tiles
	map = [[ Tile(False)
		for y in range(MAP_HEIGHT)]
			for x in range(MAP_WIDTH)]

	map[30][22].blocked = True
	map[30][22].block_sight = True
	map[55][22].blocked = True
	map[55][22].block_sight = True

def render_all():

	
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			wall = map[x][y].block_sight
			if wall:
				#libtcod.console_set_back(con, x, y, color_dark_wall, libtcod.BKGND_SET)
				libtcod.console_put_char_ex(con, x, y, '#', libtcod.white, libtcod.black)
			else:
				#libtcod.console_set_back(con, x, y, color_dark_ground, libtcod.BKGND_SET)
				libtcod.console_put_char_ex(con, x, y, '.', libtcod.light_grey, libtcod.black)

	
	#draw everything
	for stuff in objects:
		stuff.draw()
	#we are "blitting" our offscreen console oot the root console
	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

#moving around
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
		player.move(0,-1)
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		player.move(0,1)
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		player.move(-1,0)	
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		player.move(1,0)

	

#########################################
#  3 INSTANTIATE OUR CLASSES FOR GAME   #
#                                       #
#########################################

libtcod.console_set_custom_font('terminal10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'roguelike demo with libtcod', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT) #this has created an offscreen console we'll use instead of printing to the main console
libtcod.sys_set_fps(LIMIT_FPS)

player = Thing(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)

npc = Thing(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.yellow)

objects = [npc, player]

#create the map
make_map()



#########################################
#  4 MAIN LOOP                           #
#                                       #
#########################################
while not libtcod.console_is_window_closed():
	#draw all the things	
	render_all()
		

	#some other shit, flushing the console?
	libtcod.console_flush()

	#clear off the @ ghosts created by movement
	for stuff in objects:
		stuff.clear()

	#handle keys
	exit = handle_keys()
	if exit:
		break