from ..lib import libtcodpy as libtcod


class Tile(object):
    #tiles on the map
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.explored = False

        #blocked tiles also block sight
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

        self.map = []

    def make_room(self, room):
        #make tiles in rectangle passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.map[x][y].blocked = False
                self.map[x][y].block_sight = False

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

            #if not lets carve it
            if not failed:
                self.make_room(new_room)

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
