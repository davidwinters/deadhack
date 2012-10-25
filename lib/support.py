#
# support.py
#
import libtcodpy as libtcod
#
# process_key(key,mode)
# given a key pressed and current game mode. . . shuffle
# logic somewhere?  I don't know yet
#
def process_key(key,mode):
    if mode == 'map':
        if key.vk == libtcod.KEY_UP:
            print 'up'
        elif key.vk == libtcod.KEY_DOWN:
            print 'down'
        elif key.vk == libtcod.KEY_LEFT:
            print 'left'
        elif key.vk == libtcod.KEY_RIGHT:
            print 'right'


