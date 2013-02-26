#Actor.py
#

#from ..lib import libtcodpy as libtcod
import math,random
from dh.lib import libtcodpy as libtcod
from dh.game import support

messages = support.message_queue

class Actor(object):
    #generic game object
    random.seed()

    #hand int to string convert for moves/pushes
    #used it for generating a random direction
    def __init__(self, x, y):
        """ x y screen loc, char: '@', colour eg libtcod.white """
        self.x = x
        self.y = y
        #self.char = char
        #self.colour = colour
        #action queue for Actor object
        #once we execute it we need to clear it
        #and by default starts clear
        self.push = ""
        self.blocks = True

    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def calc_move_towards(self, target_x, target_y):
        #vector from this to that and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        #normalize it to 1 and round
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return(dx, dy)

    def attack(self, target):
        """ calculate attack """
        if random.randint(1,100) < int(self.hitpct*100) and \
        random.randint(1,100) > int(target.dodgepct*100):
            print "You hit the " + target.name + "!"
            self.weapon.attack(target)
            print "target hp:", target.hp 
        return target
        

    def move(self, level):
        """ attempt move from set push value """
        cast = level.mobs
        map = level.map
        #if we don't have a move just return
        if not self.push:
            return
        #if map doesn't block
        if not map.map[self.push[0]][self.push[1]].blocked: 
            #and no castmembers block
            for i in cast:
                if i.x == self.push[0] and i.y == self.push[1]:
                    messages.append(("bump!",libtcod.white))
                    self.push=""
                    return
            self.x = self.push[0]
            self.y = self.push[1]
            #clear push state since we executed it
            self.push = ""

    def phase_move(self, cast):
        """ move Actor without checking if map tile is blocked """
        if not self.push:
            return
        #if we try to move into another monster we just wait
        for i in cast:
            if cast.x == self.push[0] and cast.y == self.push[1]:
                self.push=""
                return
        self.x,self.y = self.push
        #clear push state since we executed it 
        self.push = ""
        
