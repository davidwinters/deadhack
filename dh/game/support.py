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
def process_key(key, mode, player):
    if mode == 'map':
        if key.vk == libtcod.KEY_UP:
            print 'up'
            player.y -= 1
        elif key.vk == libtcod.KEY_DOWN:
            print 'down'
            player.y += 1
        elif key.vk == libtcod.KEY_LEFT:
            print 'left'
            player.x -= 1
        elif key.vk == libtcod.KEY_RIGHT:
            print 'right'
            player.x += 1

