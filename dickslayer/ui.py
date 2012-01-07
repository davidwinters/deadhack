import curses
import random





def curses_make_map(map_x, map_y ,min_size, max_size, max_rooms):
    global map
    
    map = [[ Tile(True)
            for y in range(map_y) ]
                for x in range(map_x) ]

    rooms = []
    num_rooms = 0
    for r in range(max_rooms):
        #get random sizes

        w = random.randint(min_size, max_size)
        h = random.randint(min_size, max_size)

        #random starting point
        x = random.randint(0, map_x - w - 1)
        y = random.randint(0, map_y - h - 1)

        new_room = Rect(x, y, w, h)

        #do rooms overlap?
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            make_room(new_room)

            #get center location
            (new_x, new_y) = new_room.center()

        if num_rooms == 0:
            #this is the first room
            pass
        else:
            #not first room so make a tunnel
            (prev_x, prev_y) = rooms[num_rooms-1].center()

            #flip a coin
            if random.randint(0,1) == 1:
                #go horizontal
                make_h_tunnel(prev_x, new_x, prev_y)
                make_v_tunnel(prev_y, new_y, new_x)

            else:
                #go vertical
                make_v_tunnel(prev_y, new_y, prev_x)
                make_h_tunnel(prev_x, new_x, new_y)

        #add the room to our list
        rooms.append(new_room)
        num_rooms += 1

    return map


class Tile(object):
    #map tiles
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.explored = False

        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class Rect(object):
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) /2
        center_y = (self.y1 + self.y2) /2
        return (center_x, center_y)

    def intersect(self, other):
        #do we intersect
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

def make_h_tunnel(x1, x2, y):
    global map
    #make horizontal tunnel
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False


def make_v_tunnel(y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False
def make_room(room):
    #make tiles in rectangle passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False

def curses_render_all(map, stage, map_x, map_y):
    #lets draw it with curses

    for y in range(map_y):
        for x in range(map_x):
            wall = map[x][y].block_sight

           # without try/except this shit fails hard
            if wall:
                try: stage.addch(y, x, ord("#"))
                except curses.error: pass
            else:
                try: stage.addstr(y, x, ".")
                except curses.error: pass

def testui(stdscr):
    global myscreen

    myscreen = curses.initscr()
    size = myscreen.getmaxyx()
    map_x = size[1]#curses returns (y,x) 
    map_y = size[0]

    myscreen.border(0)
    mymap = curses_make_map(map_x, map_y, 6, 10, 30)
    curses_render_all(mymap, myscreen, map_x, map_y)
    
    
    myscreen.refresh()
    myscreen.getch()
    curses.endwin()


#curses.wrapper(testui)
