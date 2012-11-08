#
# support.py
#
from ..lib import libtcodpy as libtcod
#
# process_key(key,mode)
# given a key pressed and current game mode. . . shuffle
# logic somewhere?  I don't know yet
#
def process_key(key, mode, player):
    if mode == 'map':
        if key.vk == libtcod.KEY_UP:
            player.y -= 1
        elif key.vk == libtcod.KEY_DOWN:
            player.y += 1
        elif key.vk == libtcod.KEY_LEFT:
            player.x -= 1
        elif key.vk == libtcod.KEY_RIGHT:
            player.x += 1

