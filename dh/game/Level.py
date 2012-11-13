from dh.game import Monster, Map
import random


class Level(object):
    """ takes all of our components and creates a level """

    def __init__(self, level):
        self.level = level
        self.map = self.generate_map()
        self.mobs = self.generate_mobs()

    def generate_map(self):
        """right now just spits out a map, eventually will take level parameter to spit out a type"""
        map = Map.Map(50, 80, 7, 10, 6)
        map.make_map()
        return map

    def generate_mobs(self):
        """spit out a collection of monsters, will eventually take level into consideration"""
        mobs = []
        z = 0
        while z < self.level:
            c = 0
            while c == 0:
                x = random.randint(0, self.map.width - 1)
                y = random.randint(0, self.map.height - 1)
                if self.map.map[x][y].blocked == False:
                    mobs.append(Monster.Monster(x=x, y=y))
                    z += 1
                    c += 1

        return mobs
