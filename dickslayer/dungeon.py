import random

class Tile(object):
	#tiles on the map
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		self.explored = False

		#blcoked tiles also block sight
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight

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
			
def make_map(map_height, map_width, max_rooms, room_min_size, room_max_size, player): #pass it all our constants
	global map, objects

	#objects = [player] ## move this shit elsewhere

	#fill map with blocked tiles because its True, if False all tiles would be unblocked
	map = [[ Tile(True)
		for y in range(map_height) ]
			for x in range(map_width) ]
				
	#our map algorithm
	rooms = []
	num_rooms = 0
	for r in range(max_rooms):
		#get random height and width
		w = random.randint(room_min_size, room_max_size)
		h = random.randint(room_min_size, room_max_size)

		#pick a random starting point
		x = random.randint(0, map_width - w - 1)
		y = random.randint(0, map_height - h - 1)

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
			#place_things(new_room)##move this function somewhere else

			#grabbing center coordinates for some reason
			(new_x, new_y) = new_room.center()

			if num_rooms == 0:
				#this must be first room, start player here at center coordinates
				player.x = new_x
				player.y = new_y
				

			else: #this is not the first room so lets make a tunnel now
				(prev_x, prev_y) = rooms[num_rooms-1].center()

				#draw a coin, if 1 go horizontal first, if 0 go vertical first
				if random.randint(0, 1) == 1:
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
	return map