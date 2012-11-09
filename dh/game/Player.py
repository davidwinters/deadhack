from dh.game import Actor
from ..lib import libtcodpy as libtcod

#
# player class
#


class Player(Actor.Actor):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.char = "@"
        self.colour = libtcod.white
