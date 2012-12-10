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
        #push is a tuple of simple int coordinates on the level
        #that is supposed to be the coords they move to next
        self.push = ""
        
        #stats
        self.maxhp = 10
        self.hp = 10
        self.hitpct = .8
        self.dodgepct = .5
        self.damage = 2
