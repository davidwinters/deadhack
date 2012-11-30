#
# support.py
#
from ..lib import libtcodpy as libtcod
from collections import deque

#initialize the shared message queue-
#list of message to be sent to viewport
message_queue = deque([])

""" take key and inject it into game objects for logic """
def process_keypress(key, mode, player, level_counter, levels):
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
            if player.x == levels[level_counter].doodads[1].x and player.y == levels[level_counter].doodads[1].y:
                try:  # lets try this, if it fails it means we need to make the new level first
                    player.x = levels[level_counter + 1].doodads[0].x
                    player.y = levels[level_counter + 1].doodads[0].y
                except IndexError:
                    pass

                return level_counter + 1

        elif chr(key.c) == "<":
            if player.x == levels[level_counter].doodads[0].x and player.y == levels[level_counter].doodads[0].y:
                if level_counter > 0:  # when going up we need to make sure we're not trying to go past 0
                    player.x = levels[level_counter - 1].doodads[1].x
                    player.y = levels[level_counter - 1].doodads[1].y
                    return level_counter - 1
                else:
                    pass  # this is where we'd put a message indicating that you've hit the ceiling and can't go up
        return -1
