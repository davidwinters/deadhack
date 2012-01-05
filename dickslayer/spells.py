from lib import libtcodpy as libtcod
HEAL_AMOUNT = 4
LIGHTNING_DAMAGE = 20
LIGHTNING_RANGE = 5
CONFUSE_NUM_TURNS = 10
CONFUSE_RANGE = 8

class ConfusedMonster(object):
	#AI for a confused monster.
	def __init__(self, old_ai, num_turns=CONFUSE_NUM_TURNS):
		self.old_ai = old_ai
		self.num_turns = num_turns

	def take_turn(self,player, fov_map, objects, map):
		if self.num_turns > 0:
			#move random
			self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1),objects, map)
			self.num_turns -= 1
		else:#restore previous ai
			self.owner.ai = self.old_ai
			#message('The ' + self.owner.name + ' is no longer confused!', libtcod.red)	

def cast_heal(player,objects, fov_map):
	#heal the player
	if player.fighter.hp == player.fighter.max_hp:
		#message(' You are already at full health.', libtcod.red)
		return 'cancelled'

	#message('Your wounds start to feel better!', libtcod.light_violet)
	player.fighter.heal(HEAL_AMOUNT)

def cast_lightning(player,objects, fov_map):
	#find nearest enemy
	monster = closest_monster(LIGHTNING_RANGE, objects, player, fov_map)
	if monster is None: #none around
		#message('No enemy is near enough to strike.', libtcod.red)
		return 'cancelled'
	
	#zaap
	#message('A random bolt of static electricity strikes the ' + monster.name + ' with a loud crack! The damage is ' + str(LIGHTNING_DAMAGE) + ' hit points.', libtcod.light_blue)
	monster.fighter.take_damage(LIGHTNING_DAMAGE, objects)

def cast_confuse(player,objects, fov_map):
	#cast on nearest enemy
	monster = closest_monster(CONFUSE_RANGE, objects, player, fov_map)
	if monster is None: #none in range
		#message('No enemy is close enough to confuse.', libtcod.red)
		return 'cancelled'
	old_ai = monster.ai
	monster.ai = ConfusedMonster(old_ai)
	monster.ai.owner = monster
	#message('The ' + monster.name + '\'s eyes look vacant.', libtcod.light_green)	

def closest_monster(max_range, objects, player, fov_map):
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
