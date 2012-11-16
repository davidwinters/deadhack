from dh.game import Actor, Player
from ..lib import libtcodpy as libtcod
import random

from dh.game import support

messages = support.message_queue


class Monster(Actor.Actor):
    """generic monster object"""
    def __init__(self, monster=-1, **kwargs):
        super(Monster, self).__init__(**kwargs)
        #don't search most list for match if we don't specify one
        if monster == -1:
            self.seed = random.randint(0, len(mob) - 1)
            self.char = mob[self.seed][1]
            self.ai = mob[self.seed][2]()
        else:
            #search for requested mob in list
            found = 0
            for index,item in enumerate(mob):
                if item[0] == monster:
                    found = 1
                    self.seed = index
                    self.char = item[1]
                    self.ai = item[2]()
            if found == 0:
                raise NameError("mob requested not found")

        if self.ai:
            self.ai.owner = self

        self.colour = libtcod.yellow



class AIrandom(object):
    """ moves in random direction """
    def act(self, map, cast):
        #pull out player object from cast
        for item in cast:
            if isinstance(item, Player.Player):
                player = item
        #remove player object from cast
        monstercast = [x for x in cast if not isinstance(x, Player.Player)]

        #AI: select a random direction to push to
        self.owner.push = self.owner.x + random.randint(-1, 1), self.owner.y + random.randint(-1, 1)
        xx, yy = self.owner.push
        if map.is_blocked(xx, yy, cast):
            print "omg blocked!"
        self.owner.move(map)
        if self.owner.distance_to(player) == 0:
            messages.append(("WOOF", libtcod.white))


class AIchase(object):
    """ moves towards player """
    def act(self, map, cast):
        """ """
        #pull out player object from cast
        for item in cast:
            if isinstance(item, Player.Player):
                player = item
        #remove player object from cast
        monstercast = [x for x in cast if not isinstance(x, Player.Player)]
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
    def act(self, map, cast):
        """ """
        #pull out player object from cast
        for item in cast:
            if isinstance(item, Player.Player):
                player = item
        #remove player object from cast
        monstercast = [x for x in cast if not isinstance(x, Player.Player)]
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
["Skeleton", "s", AIrandom],
["Dragon", "D", AIchase],
["Jon", "3", AIchase]
]
