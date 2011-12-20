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
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

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


class Rect(object):
	#this is for dungeon building
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h	
	
	def center(self):
		center_x = (self.x1 + self.x2) / 2
		center_y = (self.y1 + self.y2) / 2
		return (center_x, center_y)
	
	def intersect(self, other):
		#tell us if this rect intersects another
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

def make_room(room):
	global map
	#make tiles in rectangle passable
	for x in range(room.x1 + 1 , room.x2): 
		for y in range(room.y1 + 1, room.y2):
			map[x][y].blocked = False
			map[x][y].block_sight = False	

def make_h_tunnel(x1, x2, y):
	global map
	#make horizontal tunnel
	for x in range(min(x1, x2), max(x1, x2) +1):
		map[x][y].blocked = False
		map[x][y].block_sight = False

def make_v_tunnel(y1, y2, x):
	global map
	#make vertical tunnel
	for y in range(min(y1, y2), max(y1, y2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False
			
def make_map():
	global map

	#fill map with unblocked tiles
	map = [[ Tile(True)
		for y in range(MAP_HEIGHT) ]
			for x in range(MAP_WIDTH) ]

	#our map algorithm
	rooms = []
	num_rooms = 0
	for r in range(MAX_ROOMS):
		#random width and height
		w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		#pick a random starting point
		x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
		y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

		#lets take advantage of our Rect class now
		new_room = Rect(x, y, w, h)

		#do our rooms intersect?
		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break

		#if not lets carve it
		if not failed:
			make_room(new_room)

			#grabbing center coordinates for some reason
			(new_x, new_y) = new_room.center()

			if num_rooms == 0:
				#this must be first room, start player here at center coordinates
				player.x = new_x
				player.y = new_y

			else: #this is not the first room so lets make a tunnel now
				(prev_x, prev_y) = rooms[num_rooms-1].center()

				#draw a coin, if 1 go horizontal first, if 0 go vertical first
				if libtcod.random_get_int(0, 0, 1) ==1:
					#go horizontal first
					make_h_tunnel(prev_x, new_x, prev_y)
					make_v_tunnel(prev_y, new_y, new_x)

				else:
					#go vertical first
					make_v_tunnel(prev_y, new_y, prev_x)
					make_h_tunnel(prev_x, new_x, new_y)
			
			#put the room in our list
			rooms.append(new_room)
			num_rooms += 1
	
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