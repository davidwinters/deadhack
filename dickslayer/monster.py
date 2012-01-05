from lib import libtcodpy as libtcod
import random
import dungeon

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


def make_monsters(objects, room, quantity):

	for i in range(quantity):
		#random position
		x = random.randint(room.x1+1, room.x2-1)
		y = random.randint(room.y1+1, room.y2-1)

		#only place shit if the tile isn't blocked by another thing
		if not dungeon.is_blocked(x, y, objects):
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