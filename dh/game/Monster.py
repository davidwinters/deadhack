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
            mobcard = mob[random.randint(0, len(mob) - 1)]
        else:
            #search for requested mob in list
            found = 0
            for index,item in enumerate(mob):
                if item[0] == monster:
                    found = 1
                    mobcard = mob[index]
            if found == 0:
                raise NameError("mob requested not found")
        self.name, self.char, self.colour, self.maxhp, self.hp, self.hitpct,\
                self.dodgepct, self.damage = mobcard[:8]
        
        #ai object needs instantiated instead of assigned
        self.ai = mobcard[8]()
        #let ai object know who owns it
        self.ai.owner = self




class AIrandom(object):
    """ moves in random direction """
    def act(self, map, cast, player):
        """ """
        #don't move if we can't 'hear' him
        if self.owner.distance_to(player) > 15:
            return

        #AI: select a random direction to push to
        self.owner.push = self.owner.x + random.randint(-1, 1), self.owner.y + random.randint(-1, 1)
        xx, yy = self.owner.push
        if map.is_blocked(xx, yy, cast):
            print "omg blocked!"
        self.owner.move(map, cast)
        if self.owner.distance_to(player) == 0:
            messages.append(("WOOF", libtcod.white))


class AIchase(object):
    """ moves towards player """
    def act(self, map, cast, player):
        """ """
        #don't move if we can't 'hear' him
        if self.owner.distance_to(player) > 15:
            return

        #if we're more than 2sq from player calc a move towards them
        #and execute it
        if self.owner.distance_to(player) >= 2:
            a, b = self.owner.calc_move_towards(player.x, player.y)
            self.owner.push = self.owner.x + a, self.owner.y + b
            self.owner.move(map, cast)

        if self.owner.distance_to(player) == 0:
            messages.append(("GOTCHA", libtcod.white))


class AIxorn(object):
    """ moves towards player, doesn't give a fuck """
    def act(self, map, cast, player):
        """ """
        #don't move if we can't 'hear' him
        if self.owner.distance_to(player) > 15:
            return

        #if we're more than 2sq from player calc a move towarsd them
        #and execute it
        if self.owner.distance_to(player) >= 2:
            a, b = self.owner.calc_move_towards(player.x, player.y)
            self.owner.push = self.owner.x + a, self.owner.y + b
            self.owner.phase_move(cast)

        if self.owner.distance_to(player) == 0:
            messages.append(("RAWR!", libtcod.white))



#our primary data structure for monster stats
mob = [
#name, symbol, colour, maxhp, hp, hitpct, dodgepct, damage, aimethod
["Skeleton", "s", libtcod.white, 5, 5, .5, .1, 2, AIrandom],
["angry rat", "r", libtcod.dark_orange,  5, 5, .7, .1, 2, AIchase],
["rat", "r", libtcod.orange, 5, 5, .5, .1, 1, AIchase]
]

#mobline:
#0 name
#1 symbol
#2 colour
#3 maxhp
#4 hp
#5 hitpct
#6 dodgepct
#7 damage
#8 aimethod
