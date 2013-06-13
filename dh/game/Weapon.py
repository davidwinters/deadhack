import random
from dh.lib import libtcodpy as libtcod
from dh.game import support


messages = support.message_queue

class Weapon:
    def __init__(self, attackMethod, sounds):
        self.name = "stick of punishment"
        self.maxDamage = 2
        self.minDamage = 1
        self.hitModifier = 0
        self.sounds = sounds
        self.attackMethod = attackMethod

    def attack(self, attacker, target):
        self.attackMethod.attack(self, attacker, target)


class StandardAttack(object):
    def attack(self, weapon, attacker, target):
        messages.append((random.choice(weapon.sounds), libtcod.white))
        damage = random.randint(1, weapon.maxDamage)
        target.hp -= damage
        print "did", target.hp, "damage to", target.name


class PainfulAttack(object):
    def attack(self, weapon, attacker, target):
        messages.append((random.choice(weapon.sounds), libtcod.white))
        damage = random.randint(1, weapon.maxDamage)
        target.hp -= damage
        print "did", target.hp, "damage to", target.name, ", but", weapon.minDamage, "to yourself."

#it was stupid anyway

# I'm pretty sure there's a way better way to do this.
Weapon_StickOfPunishment = Weapon(StandardAttack(), ["thud", "whack", "bonk"])
Weapon_StickOfSelfPunishment = Weapon(PainfulAttack(), ["thud", "whack", "bonk"])
Weapon_StickOfHappiness = Weapon(HealingAttack(), ["fwoosh", "zap", "bzzz"])