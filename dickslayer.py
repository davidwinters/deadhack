from lib import libtcodpy as libtcod
from dickslayer import dungeon
from dickslayer import doodads

import math
import textwrap
import shelve

#########################################
#  1 DEFINE CONSTANTS                   #
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




#classes removed	
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
#map stuff removed from here

def draw(x,y,char):
	if libtcod.map_is_in_fov(fov_map, x, y):
			libtcod.console_set_foreground_color(con, libtcod.white)
			libtcod.console_put_char(con, x, y, char, libtcod.BKGND_NONE)

def clear(x,y,char):
	#erase the ghosts when moving around
		libtcod.console_put_char_ex(con, x, y, ' ', libtcod.light_grey, libtcod.BKGND_NONE)

def initialize_fov():
	global fov_recompute, fov_map

	libtcod.console_clear(con) #reset console to black

	fov_recompute = True

	#create the FOV map
	fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
	
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
		player.fighter.attack(target, objects)
	else:
		player.move(dx, dy, objects, map)
		fov_recompute = True

def player_death(player, objects):
	#game over
	global game_state
	message('These genitals slapped you to death', libtcod.white)
	game_state = 'dead'

	#leave a corpse
	player.char = '%'
	player.color = libtcod.dark_red



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
			draw(stuff.x, stuff.y, stuff.char)
	draw(player.x, player.y, player.char)
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
	if header == '':
		header_height = 0
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

def msgbox(text, width=50):
	menu(text, [], width) #use menu() for message box

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

def main_menu():
	while not libtcod.console_is_window_closed():
		
		#show game title
		libtcod.console_print_center(0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-4, libtcod.BKGND_NONE, 'Dick Slayer')


		#show options
		choice = menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)

		if choice == 0: #new game
			new_game()
			play_game()
		elif choice == 1: #load game
			try:
				load_game()
			except:
				msgbox('\n No saved game to load. \n', 24)
				continue
			play_game()	
		elif choice == 2: #quit
			break


def new_game():
	global player, inventory, game_msgs, game_state, objects, map

	fighter_comp = doodads.Fighter(hp=30, defense=2, power=5, death_function=player_death)
	player = doodads.Thing(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', 'Joe', libtcod.white, blocks=True, fighter=fighter_comp)

	game_state = 'playing'
	

	objects = [player]
	game_msgs = []
	inventory = []

	#create the map
	map = dungeon.make_map(MAP_HEIGHT, MAP_WIDTH, MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE, player, objects, MAX_ROOM_MONSTERS)

	initialize_fov()
	
	#a welcome message
	message('Welcome jerk! Prepare to get slapped by dicks and balls.', libtcod.red)



def play_game():
	player_action = None
	while not libtcod.console_is_window_closed():
		#draw all the things	
		render_all()
		

		#some other shit, flushing the console?
		libtcod.console_flush()

		#clear off the @ ghosts created by movement
		for stuff in objects:
			clear(stuff.x, stuff.y, stuff.char)

		#handle keys
		player_action = handle_keys()
		if player_action == 'exit':
			save_game()
			break
	
		#monsters turn
		if game_state == 'playing' and player_action != 'didnt-take-turn':
			for stuff in objects:
				if stuff.ai:
					stuff.ai.take_turn(player, fov_map, objects, map)

def save_game():
	#open a new empty shelve possibly overwriting an old one
	file = shelve.open('savegame', 'n')
	file['map'] = map
	file['objects'] = objects
	file['player_index'] = objects.index(player) #position of player in objects list
	file['inventory'] = inventory
	file['game_msgs'] = game_msgs
	file['game_state'] = game_state

	file.close()			

def load_game():
	#open previously saved shelve
	global map, objects, player, inventory, game_msgs, game_state

	file = shelve.open('savegame', 'r')
	map = file['map']
	objects = file['objects']
	player = objects[file['player_index']]
	inventory = file['inventory']
	game_msgs = file['game_msgs']
	game_state = file['game_state']
	file.close()

	initialize_fov()

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
main_menu()