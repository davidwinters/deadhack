#Actor.py
#

#from ..lib import libtcodpy as libtcod

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



