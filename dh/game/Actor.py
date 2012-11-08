#Actor.py
#

#from ..lib import libtcodpy as libtcod

class Actor:
    #generic game object


    #hand int to string convert for moves/pushes
    #used it for generating a random direction
    moves = ['u','ur','r','dr','d','dl','l','ul']

    def __init__(self, x, y, char, colour):
        """ x y screen loc, char: '@', colour eg libtcod.white """
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.push = ""



