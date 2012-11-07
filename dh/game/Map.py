#
#Map.py
#
#TODO 20121106JRD: I think you can integrate the map type with Map object creation
#and have init make the requested map type without having two steps
#upon map creation pretty easy, might do it later 
from ..lib import libtcodpy as libtcod


class Tile(object):
    """ Represents 1 map tile """
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.explored = False

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
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


class Map(object):

    def __init__(self, h, w, mxr, mxrs, mnrs):
        self.height = h
        self.width = w
        self.max_rooms = mxr
        self.min_room_size = mnrs
        self.max_room_size = mxrs
        self.rooms = []
        self.num_tiles = 0
        self.map = []

    def make_room(self, room):
        #make tiles in rectangle passable
        area = 0
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                if self.map[x][y].blocked == True:
                        area = area + 1
                self.map[x][y].blocked = False
                self.map[x][y].block_sight = False
        return area

    def make_room_round(self, room):
        area = 0
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                if (x == room.x1 + 1 and y == room.y1 + 1):
                    self.map[x][y].blocked = True
                    self.map[x][y].block_sight = True

                elif (x == room.x2 - 1 and y == room.y1 + 1):
                    self.map[x][y].blocked = True
                    self.map[x][y].block_sight = True

                elif (x == room.x1 + 1 and y == room.y2 - 1):
                    self.map[x][y].blocked = True
                    self.map[x][y].block_sight = True
                elif (x == room.x2 - 1 and y == room.y2 - 1):
                    self.map[x][y].blocked = True
                    self.map[x][y].block_sight = True
                else:
                    if self.map[x][y].blocked == True:
                        area = area + 1
                    self.map[x][y].blocked = False
                    self.map[x][y].block_sight = False
        return area

    def make_h_tunnel(self, x1, x2, y):
        #make horizontal tunnel
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map[x][y].blocked = False
            self.map[x][y].block_sight = False

    def make_v_tunnel(self, y1, y2, x):
        #make vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map[x][y].blocked = False
            self.map[x][y].block_sight = False

    def make_h_hall(self, x1, x2, y1):
            #make horizontal tunnel

        for y in range(y1, y1 + 2):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                delta = libtcod.random_get_int(0, -1, 1)

                self.map[x][y].blocked = False
                self.map[x][y].block_sight = False

                if x > min(x1, x2) + 3 and x < max(x1, x2) - 3:
                    if (x % 5) == 0:
                        if delta == 1:
                            self.map[x][y1 + 2].blocked = False
                            self.map[x][y1 + 2].block_sight = False
                            for xx in range(x - 1, x + 2):
                                for yy in range(y1 + 3, y1 + 8):
                                    self.map[xx][yy].blocked = False
                                    self.map[xx][yy].block_sight = False
                        if delta == -1:
                            self.map[x][y1 - 1].blocked = False
                            self.map[x][y1 - 1].block_sight = False
                            for xx in range(x - 1, x + 2):
                                for yy in range(y1 - 7, y1 - 1):
                                    self.map[xx][yy].blocked = False
                                    self.map[xx][yy].block_sight = False

    def make_v_hall(self, y1, y2, x1):
        #make vertical tunnel
        for x in range(x1, x1 + 2):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                delta = libtcod.random_get_int(0, -1, 1)

                self.map[x][y].blocked = False
                self.map[x][y].block_sight = False

                if y > min(y1, y2) + 3 and y < max(y1, y2) - 3:
                    if (y % 5) == 0:
                        if delta == 1:
                            self.map[x1 + 2][y].blocked = False
                            self.map[x1 + 2][y].block_sight = False
                            for yy in range(y - 1, y + 2):
                                for xx in range(x1 + 3, x1 + 8):
                                    self.map[xx][yy].blocked = False
                                    self.map[xx][yy].block_sight = False
                        if delta == -1:
                            self.map[x1 - 1][y].blocked = False
                            self.map[x1 - 1][y].block_sight = False
                            for yy in range(y - 1, y + 2):
                                for xx in range(x1 - 7, x1 - 1):
                                    self.map[xx][yy].blocked = False
                                    self.map[xx][yy].block_sight = False

    def make_noise(self):
        for x in range(self.width):
            for y in range(self.height):
                wat = libtcod.random_get_int(0, 0, 100)
                if wat > 95:
                    self.map[x][y].blocked = True
                    self.map[x][y].block_sight = True

    def make_map(self):

        num_rooms = 0
        self.map = [[Tile(True)
            for y in range(self.height)]
                for x in range(self.width)]
        #our map algorithm

        for r in range(self.max_rooms):
            #random width and height
            w = libtcod.random_get_int(0, self.min_room_size, self.max_room_size)
            h = libtcod.random_get_int(0, self.min_room_size, self.max_room_size)
            #pick a random starting point
            x = libtcod.random_get_int(0, 0, self.width - w - 1)
            y = libtcod.random_get_int(0, 0, self.height - h - 1)

            #lets take advantage of our Rect class now
            new_room = Rect(x, y, w, h)

            #do our rooms intersect?
            failed = False
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break
            #if we failed lets boot to next iteration
            #we don't carve the room into the map
            if failed:
                failed = False
                continue

            #if not lets carve it
            self.num_tiles += self.make_room(new_room)

            #grabbing center coordinates for some reason
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                #this must be first room, no tunnel
                pass

            else:
                #this is not the first room so lets make a tunnel now
                (prev_x, prev_y) = self.rooms[num_rooms - 1].center()

                #draw a coin, if 1 go horizontal first, if 0 go vertical first
                if libtcod.random_get_int(0, 0, 1) == 1:
                    #go horizontal first
                    self.make_h_tunnel(prev_x, new_x, prev_y)
                    self.make_v_tunnel(prev_y, new_y, new_x)

                else:
                    #go vertical first
                    self.make_v_tunnel(prev_y, new_y, prev_x)
                    self.make_h_tunnel(prev_x, new_x, new_y)

            #put the room in our list
            self.rooms.append(new_room)
            num_rooms += 1

    def make_cave(self):
            prev_x = 0
            prev_y = 0
            num_rooms = 0

            self.map = [[Tile(True)
                for y in range(self.height)]
                    for x in range(self.width)]
            #our map algorithm

            while self.num_tiles < self.max_rooms:
                #random width and height
                w = libtcod.random_get_int(0, self.min_room_size, self.max_room_size)
                h = libtcod.random_get_int(0, self.min_room_size, self.max_room_size)
                #pick a random starting point

                x = libtcod.random_get_int(0, 0, prev_x + 10)
                y = libtcod.random_get_int(0, 0, prev_y + 10)
                if x + w + 1 >= self.width:
                    x = self.width - w - 1
                if y + h + 1 >= self.height:
                    y = self.height - h - 1

                #lets take advantage of our Rect class now
                new_room = Rect(x, y, w, h)

                #if not lets carve it
                self.num_tiles += self.make_room_round(new_room)

                #grabbing center coordinates for some reason
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    #this must be first room, no tunnel
                    pass

                else:
                    #this is not the first room so lets make a tunnel now
                    (prev_x, prev_y) = self.rooms[num_rooms - 1].center()

                    #draw a coin, if 1 go horizontal first, if 0 go vertical first
                    if libtcod.random_get_int(0, 0, 1) == 1:
                        #go horizontal first
                        self.make_h_tunnel(prev_x, new_x, prev_y)
                        self.make_v_tunnel(prev_y, new_y, new_x)

                    else:
                        #go vertical first
                        self.make_v_tunnel(prev_y, new_y, prev_x)
                        self.make_h_tunnel(prev_x, new_x, new_y)

                #put the room in our list
                self.rooms.append(new_room)
                num_rooms += 1
            self.make_noise()

    def make_greathall(self):
            hall_start = libtcod.random_get_int(0, 1, 4)
            num_bends = libtcod.random_get_int(0, 2, 3)
            start_x = 0
            start_y = 0

            self.map = [[Tile(True)
                for y in range(self.height)]
                    for x in range(self.width)]

            if hall_start == 1:
                start_x = 10
                start_y = 10
                self.make_v_hall(start_y, self.height - 10, start_x)

                self.make_h_hall(start_x, self.width - 10, self.height - 10)
                if num_bends == 3:
                    self.make_v_hall(self.height - 10, 10, self.width - 10)

            elif hall_start == 2:
                start_x = self.width - 10
                start_y = 10
                self.make_h_hall(start_x, 10, start_y)
                self.make_v_hall(start_y, self.height - 10, start_x)
                if num_bends == 3:
                    self.make_h_hall(start_x, self.width - 10, self.height - 10)

            elif hall_start == 3:
                start_x = 10
                start_y = self.height - 10
                self.make_h_hall(start_x, self.width - 10, start_y)
                self.make_v_hall(start_y, 10, self.width - 10)
                if num_bends == 3:
                    self.make_h_hall(self.width - 10, start_x, 10)
            else:
                start_x = self.width - 10
                start_y = self.height - 10
                self.make_v_hall(start_y, 10, start_x)
                self.make_h_hall(start_x, 10, 10)
                if num_bends == 3:
                    self.make_v_hall(10, start_y, 10)
