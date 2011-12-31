##################################
# TO DO							
#
# 1. finish tutorial spells and menu, last 2 parts
# 2. elaborate spells, add polymorph etc.
# 3. add a boss mob
# 4. create companion player character
#     a. allow users to view game session
#	  b. allow users to control companion
# 5. add multiple levels
# 6. etc.

import libtcodpy as libtcod
import math
import textwrap

#########################################
#  1 DEFINE PARAMETERS                  #
#                                       #
#########################################

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
MAP_WIDTH = 80
MAP_HEIGHT = 43
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_ROOM_MONSTERS = 3 

FOV_ALGO = 0 #default FOV algorithm in libtcod
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

MAX_ROOM_ITEMS = 2

INVENTORY_WIDTH = 50

HEAL_AMOUNT = 4
LIGHTNING_DAMAGE = 20
LIGHTNING_RANGE = 5
CONFUSE_NUM_TURNS = 10
CONFUSE_RANGE = 8

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
	def __init__(self, x, y, char, name, color, blocks=False, fighter=None, ai=None, item=None):
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
		self.item = item
		if self.item:
			self.item.owner = self

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
			message(self.owner.name.capitalize() + ' slaps ' + target.name + ' for ' + str(damage) + ' hit points.', libtcod.white)
			target.fighter.take_damage(damage)
		else:
			message(self.owner.name.capitalize() + ' tries to slap ' + target.name + ' but misses', libtcod.white)
	
	def heal(self, amount):
		#heal
		self.hp += amount
		if self.hp > self.max_hp:
			self.hp = self.max_hp

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

class ConfusedMonster(object):
	#AI for a confused monster.
	def __init__(self, old_ai, num_turns=CONFUSE_NUM_TURNS):
		self.old_ai = old_ai
		self.num_turns = num_turns

	def take_turn(self):
		if self.num_turns > 0:
			#move random
			self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
			self.num_turns -= 1
		else:#restore previous ai
			self.owner.ai = self.old_ai
			message('The ' + self.owner.name + ' is no longer confused!', libtcod.red)



class Item(object):
	#items that can be picked up and used
	def __init__(self, use_function=None):
		self.use_function = use_function

	def pick_up(self):
		#add to inventory and remove from map
		if len(inventory) >= 26:
			message('Your inventory is full, cannot pick up ' + self.owner.name + '.', bitcod.red)
		else:
			inventory.append(self.owner)
			objects.remove(self.owner)
			message('You picked up a ' + self.owner.name + '!', libtcod.green)

	def use(self):
		#use_function if it exists
		if self.use_function is None:
			message('The ' + self.owner.name + ' cannot be used.')

		else:
			if self.use_function() != 'cancelled':
				inventory.remove(self.owner) #destory item after use

	def drop(self):
		#add to map and remove from inventory
		objects.append(self.owner)
		inventory.remove(self.owner)
		self.owner.x = player.x
		self.owner.y = player.y
		message('You dropped a ' + self.owner.name + '.', libtcod.yellow)
					


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
	global map, objects

	objects = [player]

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
		x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
		y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

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

	#random number of items
	num_items = libtcod.random_get_int(0, 0, MAX_ROOM_ITEMS)

	for i in range(num_items):
		#random spot
		x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
		y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

		#only put on unblocked tiles
		if not is_blocked(x, y):
			dice = libtcod.random_get_int(0, 0, 100)
			if dice < 70:
				#create health pot
				item_comp = Item(use_function=cast_heal)
				item = Thing(x, y, '!', 'healing potion', libtcod.violet, item=item_comp)
			elif dice < 70 + 15:
				#create confuse scroll
				item_comp = Item(use_function=cast_confuse)
				item = Thing(x, y, '?', 'scroll of confusion', libtcod.white, item=item_comp)
			else:
				#create lightning bolt scroll
				item_comp = Item(use_function=cast_lightning)
				item = Thing(x, y, '?', 'scroll of static lightning', libtcod.light_yellow, item=item_comp)
				
			objects.append(item)
			item.send_to_back() #items appear below other objects when drawn on the console

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
	message('These genitals slapped you to death', libtcod.white)
	game_state = 'dead'

	#leave a corpse
	player.char = '%'
	player.color = libtcod.dark_red

def monster_death(monster):
	#leave a corpse
	message(monster.name.capitalize() + ' collapses in a puddle of unknown fluid, spent', libtcod.white)
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

	#render GUI
	libtcod.console_set_background_color(panel, libtcod.black)
	libtcod.console_clear(panel)

	#print game messages
	y = 1
	for (line, color) in game_msgs:
		libtcod.console_set_foreground_color(panel, color)
		libtcod.console_print_left(panel, MSG_X, y, libtcod.BKGND_NONE, line)
		y += 1

	#show player stats
	render_bar(1, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)

	#blit onto root console
	libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)

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
			#all other keys
			key_char = chr(key.c)
			if key_char == 'g':
				#pick up item
				for stuff in objects:
					if stuff.x == player.x and stuff.y == player.y and stuff.item:
						stuff.item.pick_up()
						break
			if key_char == 'i':
				#show inventory
				chosen_item = inventory_menu('Press the key next to an item to use it, or any other to cancel. \n')
				if chosen_item is not None:
					chosen_item.use()
			if key_char == 'd':
				chosen_item = inventory_menu('Press they key next to an item to drop it, or any other to cancel. \n')
				if chosen_item is not None:
						chosen_item.drop()

			return 'didnt-take-turn'

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
	#render a bar	
	bar_width = int(float(value) / maximum * total_width)

	#background first
	libtcod.console_set_background_color(panel, back_color)
	libtcod.console_rect(panel, x, y, total_width, 1, False)

	#put bar at top
	libtcod.console_set_background_color(panel, bar_color)
	if bar_width > 0:
		libtcod.console_rect(panel, x, y, bar_width, 1, False)

	#some text and values
	libtcod.console_set_foreground_color(panel, libtcod.white)
	libtcod.console_print_center(panel, x + total_width / 2, y, libtcod.BKGND_NONE, name + ': ' + str(value) + '/' + str(maximum))

def message(new_msg, color = libtcod.white):
	#break lines if you need
	new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

	for line in new_msg_lines:
		#clear buffer
		if len(game_msgs) == MSG_HEIGHT:
			del game_msgs[0]

		#add new messages
		game_msgs.append( (line,color) )

def menu(header, options, width):
	if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

	#calc height of header
	header_height = libtcod.console_height_left_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
	height = len(options) + header_height

	#offscreen conolse
	window = libtcod.console_new(width, height)
	
	#print the header
	libtcod.console_set_foreground_color(window, libtcod.white)
	libtcod.console_print_left_rect(window, 0, 0, width, height, libtcod.BKGND_NONE, header)
	
	y = header_height
	letter_index= ord('a')
	for option_text in options:
		text = '(' + chr(letter_index) + ') ' + option_text
		libtcod.console_print_left(window, 0, y, libtcod.BKGND_NONE, text)
		y += 1
		letter_index += 1
	
	#blit the contents to the main console
	x = SCREEN_WIDTH/2 - width/2
	y = SCREEN_HEIGHT/2 - height/2
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

	#wait for keypress
	libtcod.console_flush()
	key = libtcod.console_wait_for_keypress(True)

	#convert ascii to index
	index = key.c - ord('a')
	if index >= 0 and index < len(options): return index
	return None

def inventory_menu(header):
	#show a menu with each item of inventory as an option
	if len(inventory) == 0:
		options = ['Inventory is empty.']
	else:
		options = [item.name for item in inventory]

	index = menu(header, options, INVENTORY_WIDTH)

	#if item was chosen, return it
	if index is None or len(inventory) == 0: return None
	return inventory[index].item

def cast_heal():
	#heal the player
	if player.fighter.hp == player.fighter.max_hp:
		message(' You are already at full health.', libtcod.red)
		return 'cancelled'

	message('Your wounds start to feel better!', libtcod.light_violet)
	player.fighter.heal(HEAL_AMOUNT)

def cast_lightning():
	#find nearest enemy
	monster = closest_monster(LIGHTNING_RANGE)
	if monster is None: #none around
		message('No enemy is near enough to strike.', libtcod.red)
		return 'cancelled'
	
	#zaap
	message('A random bolt of static electricity strikes the ' + monster.name + ' with a loud crack! The damage is ' + str(LIGHTNING_DAMAGE) + ' hit points.', libtcod.light_blue)
	monster.fighter.take_damage(LIGHTNING_DAMAGE)

def cast_confuse():
	#cast on nearest enemy
	monster = closest_monster(CONFUSE_RANGE)
	if monster is None: #none in range
		message('No enemy is close enough to confuse.', libtcod.red)
		return 'cancelled'
	old_ai = monster.ai
	monster.ai = ConfusedMonster(old_ai)
	monster.ai.owner = monster
	message('The ' + monster.name + '\'s eyes look vacant.', libtcod.light_green)	

def closest_monster(max_range):
	#find nearest enemy
	closest_enemy = None
	closest_dist = max_range + 1

	for object in objects:
		if object.fighter and not object == player and libtcod.map_is_in_fov(fov_map, object.x, object.y):
			#find distance
			dist = player.distance_to(object)
			if dist < closest_dist:
				closest_enemy = object
				closest_dist = dist
	return closest_enemy

def new_game():
	global player, inventory, game_msgs, game_state

	fighter_comp = Fighter(hp=30, defense=2, power=5, death_function=player_death)
	player = Thing(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', 'Joe', libtcod.white, blocks=True, fighter=fighter_comp)

	game_state = 'playing'
	

	objects = [player]
	game_msgs = []
	inventory = []

	#create the map
	make_map()

	initialize_fov()
	
	#a welcome message
	message('Welcome jerk! Prepare to get slapped by dicks and balls.', libtcod.red)

def initialize_fov():
	global fov_recompute, fov_map

	fov_recompute = True

	#create the FOV map
	fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)

def play_game():
	player_action = None
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
			

#########################################
#  3 INSTANTIATE OUR CLASSES FOR GAME   #
#                                       #
#########################################

libtcod.console_set_custom_font('terminal10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'roguelike demo with libtcod', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT) #this has created an offscreen console we'll use instead of printing to the main console
libtcod.sys_set_fps(LIMIT_FPS)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)


#########################################
#  4 MAIN LOOP                           #
#                                       #
#########################################
new_game()
play_game()