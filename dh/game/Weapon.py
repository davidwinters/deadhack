import random
from dh.lib import libtcodpy as libtcod
from dh.game import support


messages = support.message_queue

class Weapon:
    def __init__(self):
        self.name = "stick of punishment"
        self.maxDamage = 2
        self.minDamage = 1
        self.hitModifier = 0
        self.sound = "thud"

    def attack(self, target):
        #maybe different weapons have different effects depending on what they're attacking... i don't know
        messages.append((self.sound, libtcod.white))
        target.hp -= random.randint(1,self.maxDamage)
