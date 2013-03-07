import random
from dh.lib import libtcodpy as libtcod
from dh.game import support


messages = support.message_queue

class Container(object):
    def __init__(self, x, y, char, name, contents):
        self.char = char
        self.x = x
        self.y = y
        self.name = name
        self.contents = contents

    def open(self):
        message = "You open the " + self.name
        messages.append((message, libtcod.white))