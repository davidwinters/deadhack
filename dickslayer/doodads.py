from lib import libtcodpy as libtcod
import spells
import random
import math

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

	def move(self,dx,dy,objects, map):

		if not is_blocked(self.x + dx, self.y +dy, objects, map): #check that the tile is not blocked
			#move by given ammount
			self.x += dx
			self.y += dy

	def move_towards(self, target_x, target_y, objects, map):
		#vector from this to that and distance
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)

		#normalize it to 1 and round
		dx = int(round(dx /distance))
		dy = int(round(dy / distance))
		self.move(dx, dy, objects, map)
	
	def distance_to(self, other):
		#return the distance to another object
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy  ** 2)


	#def draw(self):
		#set the color and then draw the character that represents this object at its position
		#if libtcod.map_is_in_fov(fov_map, self.x, self.y):

			#libtcod.console_set_foreground_color(con, self.color)
			#libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
		
	#def clear(self):
		#erase the ghosts when moving around
		#libtcod.console_put_char_ex(con, self.x, self.y, ' ', libtcod.light_grey, libtcod.BKGND_NONE)

	def send_to_back(self, objects):
		
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

	def take_damage(self,damage,objects):
		#apply damage
		if damage > 0:
			self.hp -= damage
		
		if self.hp <= 0:
			function = self.death_function
			if function is not None:
				function(self.owner,objects)
	
	def attack(self, target,objects):
		#attack damage
		damage = self.power - target.fighter.defense

		if damage > 0:
			#make the target take some damage
			#message(self.owner.name.capitalize() + ' slaps ' + target.name + ' for ' + str(damage) + ' hit points.', libtcod.white)
			target.fighter.take_damage(damage,objects)
		else:
			#message(self.owner.name.capitalize() + ' tries to slap ' + target.name + ' but misses', libtcod.white)
			pass
	
	def heal(self, amount):
		#heal
		self.hp += amount
		if self.hp > self.max_hp:
			self.hp = self.max_hp

class BasicMonster(object):
	#monster AI
	def take_turn(self, player, fov_map, objects, map):
		monster = self.owner
		
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

			#move towards player
			if monster.distance_to(player) >= 2:
				monster.move_towards(player.x, player.y, objects, map)

			#close enough to attack
			elif player.fighter.hp > 0:
				monster.fighter.attack(player,objects)





class Item(object):
	#items that can be picked up and used
	def __init__(self, use_function=None):
		self.use_function = use_function

	def pick_up(self, objects, inventory):
		#add to inventory and remove from map
		if len(inventory) >= 26:
			#message('Your inventory is full, cannot pick up ' + self.owner.name + '.', bitcod.red)
			pass
		else:
			inventory.append(self.owner)
			objects.remove(self.owner)
			#message('You picked up a ' + self.owner.name + '!', libtcod.green)

	def use(self, inventory, player, objects, fov_map):
		#use_function if it exists
		if self.use_function is None:
			#message('The ' + self.owner.name + ' cannot be used.')
			pass
		else:
			if self.use_function(player,objects,fov_map) != 'cancelled':
				inventory.remove(self.owner) #destory item after use

	def drop(self, objects, inventory):
		#add to map and remove from inventory
		objects.append(self.owner)
		inventory.remove(self.owner)
		self.owner.x = player.x
		self.owner.y = player.y
		#message('You dropped a ' + self.owner.name + '.', libtcod.yellow)

def is_blocked(x, y, objects, map):
	#tests if tiles are blocked by things
	if map[x][y].blocked:
		return True
		
	#check for things
	for stuff in objects:
		if stuff.blocks and stuff.x == x and stuff.y == y:
			return True
	return False			

def monster_death(monster,objects):
	#leave a corpse
	#message(monster.name.capitalize() + ' collapses in a puddle of unknown fluid, spent', libtcod.white)
	monster.char = '%'
	monster.color = libtcod.dark_red
	monster.blocks = False
	monster.fighter = None
	monster.ai = None
	monster.name = 'heap of used' + monster.name
	monster.send_to_back(objects)


def make_monsters(objects, map, room, quantity):

	for i in range(quantity):
		#random position
		x = random.randint(room.x1+1, room.x2-1)
		y = random.randint(room.y1+1, room.y2-1)

		#only place shit if the tile isn't blocked by another thing
		if not is_blocked(x, y, objects, map):
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

def make_items(objects, map, room, quantity):

	for i in range(quantity):
		#random spot
		x = random.randint(room.x1+1, room.x2-1)
		y = random.randint(room.y1+1, room.y2-1)

		#only put on unblocked tiles
		if not is_blocked(x, y, objects, map):
			dice = libtcod.random_get_int(0, 0, 100)
			if dice < 70:
				#create health pot
				item_comp = Item(use_function=spells.cast_heal)
				item = Thing(x, y, '!', 'healing potion', libtcod.violet, item=item_comp)
			elif dice < 70 + 15:
				#create confuse scroll
				item_comp = Item(use_function=spells.cast_confuse)
				item = Thing(x, y, '?', 'scroll of confusion', libtcod.white, item=item_comp)
			else:
				#create lightning bolt scroll
				item_comp = Item(use_function=spells.cast_lightning)
				item = Thing(x, y, '?', 'scroll of static lightning', libtcod.light_yellow, item=item_comp)
				
			objects.append(item)
			item.send_to_back(objects) #items appear below other objects when drawn on the console



