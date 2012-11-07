#
# mapdemo.py
#

# imports
from dh.lib import libtcodpy as libtcod
from dh.game import Map, Display

#
# setup
#
display = Display.Display()


#main loop
while not display.display_closed():
    display.flush()
    #eat a key
    key = libtcod.console_wait_for_keypress(True)
    key_char = chr(key.c)

    #if it tastes bad spit it out
    if key.vk == libtcod.KEY_ESCAPE:
        break
    elif key_char == 'c':
        newmap = Map.Map(50, 80, 1000, 10, 6)
        newmap.make_cave()

    elif key_char == 'm':
        newmap = Map.Map(50, 80, 1000, 10, 6)
        newmap.make_map()
    elif key_char == 'h':
        newmap = Map.Map(50, 80, 1000, 10, 6)
        newmap.make_greathall()
    else:
        #keep rockin
        newmap = Map.Map(50, 80, 1000, 10, 6)
        newmap.make_map()

    display.draw_map("map", newmap)
    display.flush()
