#
# support.py
#
from ..lib import libtcodpy as libtcod
import Player
#
# process_key(key,mode)
# given a key pressed and current game mode. . . shuffle
# logic somewhere?  I don't know yet
#
def process_key(key,mode,player):
    if mode == 'map':
        if key.vk == libtcod.KEY_UP:
            print 'up'
            player.lasty = player.y
            player.y -= 1
        elif key.vk == libtcod.KEY_DOWN:
            print 'down'
            player.lasty = player.y
            player.y += 1
        elif key.vk == libtcod.KEY_LEFT:
            print 'left'
            player.lastx = player.x
            player.x -= 1
        elif key.vk == libtcod.KEY_RIGHT:
            print 'right'
            player.lastx = player.x
            player.x += 1

