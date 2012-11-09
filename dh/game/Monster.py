from dh.game import Actor, support
from ..lib import libtcodpy as libtcod
import random


class Monster(Actor.Actor):
    """generic monster object"""
    def __init__(self):
        self.seed = random.randint(0, len(mob) - 1)
        self.x = 0
        self.y = 0
        self.colour = libtcod.yellow
        self.char = mob[self.seed][1]
        self.ai = mob[self.seed][2]
        self.push = ""
        if self.ai:
            self.ai.owner = self


class AIrandom(object):
    """ moves in random direction """
    def __init__(self):
        self.moves = ['u', 'ur', 'r', 'dr', 'd', 'dl', 'l', 'ul']

    def act(self, map):
        self.owner.push = self.moves[random.randint(0, 7)]
        support.move(self.owner, map)

#our primary data structure for monster stats
mob = [
["Skeleton", "s", AIrandom()],
["Dragon", "D", AIrandom()],
["Jon", "3", AIrandom()]
]
