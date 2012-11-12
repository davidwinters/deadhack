from dh.game import Actor
from ..lib import libtcodpy as libtcod

#
# player class
#


class Player(Actor.Actor):

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.char = "@"
        self.colour = libtcod.white
        self.push = ""
