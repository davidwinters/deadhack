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

    def act(self, map, player):
        self.owner.push = self.moves[random.randint(0, 7)]
        support.move(self.owner, map)


class AIchase(object):
    """ moves towards player """

    def act(self, map, player):
        if self.owner.distance_to(player) >= 2:
                dx, dy = self.owner.move_towards(player.x, player.y)
                testx = self.owner.x + dx
                testy = self.owner.y + dy

                if map.map[testx][self.owner.y].blocked == False:
                    self.owner.x += dx
                if map.map[self.owner.x][testy].blocked == False:
                    self.owner.y += dy


class AIxorn(object):
    """ moves towards player, doesn't give a fuck """

    def act(self, map, player):
        if self.owner.distance_to(player) >= 2:
                dx, dy = self.owner.move_towards(player.x, player.y)
                self.owner.x += dx
                self.owner.y += dy

#our primary data structure for monster stats
mob = [
["Skeleton", "s", AIrandom()],
["Dragon", "D", AIxorn()],
["Jon", "3", AIchase()]
]
