import libtcodpy as libtcod
import math

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
MAX_ROOM_MONSTERS = 3 

FOV_ALGO = 0 #default FOV algorithm in libtcod
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

color_dark_wall = libtcod.Color(80, 80, 80) #dark grey
color_dark_ground = libtcod.Color(0, 0, 0)

color_light_wall = libtcod.Color(255, 255, 255) #white
color_light_ground = libtcod.Color(192, 192, 192) #light grey


#########################################
#  2 CREATE OUR CLASSES AND FUNCTIONS   #
#                                       #
#########################################

class Tile(object):
	#tiles on the map
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		self.explored = False

		#blcoked tiles also block sight
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight


class Thing(object): #i renamed this to Thing instead of Object just cause
	#create a generic class for pc, npc, monsters, items etc.
	def __init__(self, x, y, char, name, color, blocks=False, fighter=None, ai=None):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		self.name = name
		self.blocks = blocks
		self.fighter = fighter
		if self.fighter:
			self.fighter.owner = self
		self.ai = ai
		if self.ai:
			self.ai.owner = self

	def move(self,dx,dy):

		if not is_blocked(self.x + dx, self.y +dy): #check that the tile is not blocked
			#move by given ammount
			self.x += dx
			self.y += dy

	def move_towards(self, target_x, target_y):
		#vector from this to that and distance
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)

		#normalize it to 1 and round
		dx = int(round(dx /distance))
		dy = int(round(dy / distance))
		self.move(dx, dy)
	
	def distance_to(self, other):
		#return the distance to another object
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy  ** 2)


	def draw(self):
		#set the color and then draw the character that represents this object at its position
		if libtcod.map_is_in_fov(fov_map, self.x, self.y):

			libtcod.console_set_foreground_color(con, self.color)
			libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
		
	def clear(self):
		#erase the ghosts when moving around
		libtcod.console_put_char_ex(con, self.x, self.y, ' ', libtcod.light_grey, libtcod.BKGND_NONE)

	def send_to_back(self):
		global objects
		objects.remove(self)
		objects.insert(0, self)

class Fighter(object):
	#combat properties
	def __init__(self, hp, defense, power, death_function=None):
		self.max_hp = hp
		self.hp = hp
		self.defense = defense
		self.power = power
		self.death_function = death_function

	def take_damage(self,damage):
		#apply damage
		if damage > 0:
			self.hp -= damage
		
		if self.hp <= 0:
			function = self.death_function
			if function is not None:
				function(self.owner)
	
	def attack(self, target):
		#attack damage
		damage = self.power - target.fighter.defense

		if damage > 0:
			#make the target take some damage
			print self.owner.name.capitalize() + ' slaps ' + target.name + ' for ' + str(damage) + ' hit points.'
			target.fighter.take_damage(damage)
		else:
			print self.owner.name.capitalize() + ' tries to slap ' + target.name + ' but misses'

class BasicMonster(object):
	#monster AI
	def take_turn(self):
		monster = self.owner
		
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

			#move towards player
			if monster.distance_to(player) >= 2:
				monster.move_towards(player.x, player.y)

			#close enough to attack
			elif player.fighter.hp > 0:
				monster.fighter.attack(player)
		

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
	global map, player

	#fill map with blocked tiles because its True, if False all tiles would be unblocked
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
			#add some contents to this room, such as monsters
			place_things(new_room)

			#grabbing center coordinates for some reason
			(new_x, new_y) = new_room.center()

			if num_rooms == 0:
				#this must be first room, start player here at center coordinates
				player.x = new_x
				player.y = new_y

			else: #this is not the first room so lets make a tunnel now
				(prev_x, prev_y) = rooms[num_rooms-1].center()

				#draw a coin, if 1 go horizontal first, if 0 go vertical first
				if libtcod.random_get_int(0, 0, 1) == 1:
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

def place_things(room):
	#random number of monsters
	num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)

	for i in range(num_monsters):
		#random position
		x = libtcod.random_get_int(0, room.x1, room.x2)
		y = libtcod.random_get_int(0, room.y1, room.y2)

		#only place shit if the tile isn't blocked by another thing
		if not is_blocked(x, y):
			if libtcod.random_get_int(0, 0, 100) < 80: #80% chance of getting a dick
				#make dick
				fighter_comp = Fighter(hp=10, defense=0, power=3, death_function=monster_death)
				ai_comp = BasicMonster()
				monster = Thing(x, y, 'd', 'dick', libtcod.pink, blocks=True, fighter=fighter_comp, ai=ai_comp)
			else:
				#make balls
				fighter_comp = Fighter(hp=5, defense=0, power=1, death_function=monster_death)
				ai_comp = BasicMonster()
				monster = Thing(x, y, '8', 'balls', libtcod.pink, blocks=True, fighter=fighter_comp, ai=ai_comp)
			
			objects.append(monster)

def is_blocked(x, y):
	#tests if tiles are blocked by things
	if map[x][y].blocked:
		return True
		
	#check for things
	for stuff in objects:
		if stuff.blocks and stuff.x == x and stuff.y == y:
			return True
	return False
	
def player_move_or_attack(dx, dy):
	global fov_recompute

	#the player coordinates to move/attack to
	x = player.x + dx
	y = player.y + dy

	#anything to attack?
	target =None
	for stuff in objects:
		if stuff.fighter and stuff.x == x and stuff.y == y:
			target = stuff
			break
	
	#attack or move
	if target is not None:
		player.fighter.attack(target)
	else:
		player.move(dx, dy)
		fov_recompute = True

def player_death(player):
	#game over
	global game_state
	print 'These genitals slapped you to death'
	game_state = 'dead'

	#leave a corpse
	player.char = '%'
	player.color = libtcod.dark_red

def monster_death(monster):
	#leave a corpse
	print monster.name.capitalize() + ' collapses in a puddle of unknown fluid, spent'
	monster.char = '%'
	monster.color = libtcod.dark_red
	monster.blocks = False
	monster.fighter = None
	monster.ai = None
	monster.name = 'heap of used' + monster.name
	monster.send_to_back()

def render_all():
	global fov_map, color_dark_wall, color_light_wall, color_dark_ground, color_light_ground, fov_recompute
	
	if fov_recompute:
		#recompute FOV if needed
		fov_recompute = False
		libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)	

	
		for y in range(MAP_HEIGHT):
			for x in range(MAP_WIDTH):
				visible = libtcod.map_is_in_fov(fov_map, x, y)
				wall = map[x][y].block_sight
				if not visible:
					if map[x][y].explored:
						if wall:
							libtcod.console_put_char_ex(con, x, y, '#', color_dark_wall, libtcod.black)

						else:
							libtcod.console_put_char_ex(con, x, y, '.', color_dark_ground, libtcod.black)
				else:
					if wall:
						libtcod.console_put_char_ex(con, x, y, '#', color_light_wall, libtcod.black)
					else:
						libtcod.console_put_char_ex(con, x, y, '.', color_light_ground, libtcod.black)
					map[x][y].explored = True
	
	#draw everything
	for stuff in objects:
		if stuff != player:
			stuff.draw()
	player.draw()
	#we are "blitting" our offscreen console oot the root console
	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

	#show the player's stats
	libtcod.console_set_foreground_color(con, libtcod.white)
	libtcod.console_print_left(0, 1, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, 'HP: ' + str(player.fighter.hp) + '/' + str(player.fighter.max_hp))

#moving around
#players cooridnates
def handle_keys():
	global playerx, playery, fov_recompute
	
	#console controls 
	key = libtcod.console_wait_for_keypress(True) # THIS LINE IS SPECIFIC FOR TURN BASED

	if key.vk == libtcod.KEY_ENTER and key.lalt:
		#ALT+ENTER toggle fullscreen
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
	
	elif key.vk == libtcod.KEY_ESCAPE:
		return  'exit' # exit game


	#movement keys
	#is_key_pressed is supposed to be for real-time and check_for_keypress is for TURN BASED 
	#but it behaved strangely if i did not use is_key_pressed
	if game_state == 'playing':
		if libtcod.console_is_key_pressed(libtcod.KEY_UP):
			player_move_or_attack(0,-1)
			

		elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
			player_move_or_attack(0,1)
			

		elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
			player_move_or_attack(-1,0)
			
				
		elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
			player_move_or_attack(1,0)
			
		else:
			return 'didnt-take-turn'

	

#########################################
#  3 INSTANTIATE OUR CLASSES FOR GAME   #
#                                       #
#########################################

libtcod.console_set_custom_font('terminal10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'roguelike demo with libtcod', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT) #this has created an offscreen console we'll use instead of printing to the main console
libtcod.sys_set_fps(LIMIT_FPS)

fighter_comp = Fighter(hp=30, defense=2, power=5, death_function=player_death)
player = Thing(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', 'Joe', libtcod.white, blocks=True, fighter=fighter_comp)

game_state = 'playing'
player_action = None

objects = [player]

#create the map
make_map()

#create the FOV map
fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
	for x in range(MAP_WIDTH):
		libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)

fov_recompute = True

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
	player_action = handle_keys()
	if player_action == 'exit':
		break
	
	#monsters turn
	if game_state == 'playing' and player_action != 'didnt-take-turn':
		for stuff in objects:
			if stuff.ai:
				stuff.ai.take_turn()
			
