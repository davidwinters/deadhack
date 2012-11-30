#
# support.py
#
from ..lib import libtcodpy as libtcod
from collections import deque

#initialize the shared message queue-
#list of message to be sent to viewport
message_queue = deque([])

""" take key and inject it into game objects for logic """
def process_keypress(key, mode, player, level_counter):
    """ take key and inject it into game objects for logic """
    if mode == 'map':
        if (key.vk == libtcod.KEY_UP or chr(key.c) == 'k'):
            player.push = (player.x,player.y-1)
        elif chr(key.c) == 'u':
            player.push = (player.x+1,player.y-1)
        elif key.vk == libtcod.KEY_RIGHT or chr(key.c) == 'l':
            player.push = (player.x+1,player.y)
        elif chr(key.c) == "n":
            player.push = (player.x+1,player.y+1)
        elif key.vk == libtcod.KEY_DOWN or chr(key.c) == 'j':
            player.push = (player.x,player.y+1)
        elif chr(key.c) == "b":
            player.push = (player.x-1,player.y+1)
        elif key.vk == libtcod.KEY_LEFT or chr(key.c) == 'h':
            player.push = (player.x-1,player.y)
        elif chr(key.c) == "y":
            player.push = (player.x-1,player.y-1)
        elif chr(key.c) == ">":
            print "down"
            level_counter += 1

        elif chr(key.c) == "<":
            print "up"
            if level_counter > 0:
                level_counter += -1
            else:
                print "no levels above"
