from dh.game import Monster, Map, Doodad
import random


class Level(object):
    """ takes all of our components and creates a level """

    def __init__(self, level):
        self.level = level
        self.map = self.generate_map()
        self.mobs = self.generate_mobs()
        self.doodads = self.generate_stairs()

    def generate_map(self):
        """right now just spits out a map, eventually will take level parameter to spit out a type"""
        map = Map.Map(50, 80, 1000, 10, 6)

        #here we can map out our larger map structure
        if self.level < 2:
            map.make_greathall()
        elif self.level >= 2 and self.level < 20:
            map.make_map()
        elif self.level >= 20:
            map.make_cave()
        else:
            map.make_map()
        return map

    def generate_stairs(self):
        doodads = []
        c = 0
        z = 0
        while c == 0:
            x = random.randint(0, self.map.width - 1)
            y = random.randint(0, self.map.height - 1)
            if self.map.map[x][y].blocked == False:
                if z == 0:
                    doodads.append(Doodad.Stairs(x=x, y=y, direction=1, char="<"))
                    z += 1
                else:
                    doodads.append(Doodad.Stairs(x=x, y=y, direction=-1, char=">"))
                    c += 1
        return doodads

    def generate_mobs(self):
        """spit out a collection of monsters, will eventually take level into consideration"""
        mobs = []
        z = 0
        while z < 10:  # 10 mobs per level for now
            c = 0
            while c == 0:
                x = random.randint(0, self.map.width - 1)
                y = random.randint(0, self.map.height - 1)
                if self.map.map[x][y].blocked == False:
                    mobs.append(Monster.Monster(x=x, y=y))
                    z += 1
                    c += 1

        return mobs
