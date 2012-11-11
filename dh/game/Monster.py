from dh.game import Actor
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
    def act(self, map, player, messages):
        self.owner.push = self.owner.x + random.randint(-1, 1), self.owner.y + random.randint(-1, 1)
        self.owner.move(map)
        if self.owner.distance_to(player) == 0:
            messages.append(("WOOF", libtcod.white))


class AIchase(object):
    """ moves towards player """
    def act(self, map, player, messages):
        """ """
        #if we're more than 2sq from player calc a move towards them
        #and execute it
        if self.owner.distance_to(player) >= 2:
            a, b = self.owner.calc_move_towards(player.x, player.y)
            self.owner.push = self.owner.x + a, self.owner.y + b
            self.owner.move(map)

        if self.owner.distance_to(player) == 0:
            messages.append(("GOTCHA", libtcod.white))


class AIxorn(object):
    """ moves towards player, doesn't give a fuck """
    def act(self, map, player, messages):
        """ """
        #if we're more than 2sq from player calc a move towarsd them
        #and execute it
        if self.owner.distance_to(player) >= 2:
            a, b = self.owner.calc_move_towards(player.x, player.y)
            self.owner.push = self.owner.x + a, self.owner.y + b
            self.owner.phase_move()

        if self.owner.distance_to(player) == 0:
            messages.append(("RAWR!", libtcod.white))



#our primary data structure for monster stats
mob = [
["Skeleton", "s", AIrandom()],
["Dragon", "D", AIxorn()],
["Jon", "3", AIchase()]
]
