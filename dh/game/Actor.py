#Actor.py
#

#from ..lib import libtcodpy as libtcod
import math


class Actor(object):
    #generic game object

    #hand int to string convert for moves/pushes
    #used it for generating a random direction
    def __init__(self):
        """ x y screen loc, char: '@', colour eg libtcod.white """
        self.x = 0
        self.y = 0
        #self.char = char
        #self.colour = colour
        #action queue for Actor object
        #once we execute it we need to clear it
        #and by default starts clear
        self.push = ""

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

    def move(self, map):
        """ attempt move from set push value """
        #if we don't have a move just return
        if not self.push:
            return
        if not map.map[self.push[0]][self.push[1]].blocked: 
            self.x = self.push[0]
            self.y = self.push[1]
            #clear push state since we executed it
            self.push = ""

    def phase_move(self):
        """ move Actor without checking if map tile is blocked """
        if not self.push:
            return
        self.x,self.y = self.push
        #clear push state since we executed it 
        self.push = ""
        
