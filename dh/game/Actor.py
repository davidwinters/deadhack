#Actor.py
#

from ..lib import libtcodpy as libtcod

class Actor:
    #generic game object
    def __init__(self, x, y, char, colour):
        """ x y screen loc, char: '@', colour eg libtcod.white """
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour

    def move(self, dx, dy):
        ''' move my ass'''
        self.x += dx
        self.y += dy

    #we need a method in Display to draw an object?
    #and a method to clear
