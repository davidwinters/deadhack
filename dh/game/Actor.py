#Actor.py
#

#from ..lib import libtcodpy as libtcod
import math


class Actor(object):
    #generic game object

    #hand int to string convert for moves/pushes
    #used it for generating a random direction
    def __init__(self, x, y, char, colour):
        """ x y screen loc, char: '@', colour eg libtcod.white """
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.push = ""

    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_towards(self, target_x, target_y):
        #vector from this to that and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        #normalize it to 1 and round
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return(dx, dy)
