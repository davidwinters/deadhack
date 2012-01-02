from lib import libtcodpy as libtcod
from dickslayer import config

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
	def __init__(self, old_ai, num_turns=config.CONFUSE_NUM_TURNS):
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

