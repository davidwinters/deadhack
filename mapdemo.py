#import libtcod - just required, has many parts
#like keyboard processing outside of graphics
from dh.lib import libtcodpy as libtcod
#made a placeholder but not used yet
#from lib import Player
#I needed support methods for logic and didn't know where to put them
from dh.game import Map, Display
display = Display.Display()


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

color_light_wall = libtcod.Color(255, 255, 255) #white
color_light_ground = libtcod.Color(192, 192, 192) #light grey



def render_all(map, con):

    for y in range(map.height):
        for x in range(map.width):
            wall = map.map[x][y].block_sight
            if wall:
                libtcod.console_put_char_ex(con, x, y, '#', color_light_wall, libtcod.black)
            else:
                libtcod.console_put_char_ex(con, x, y, '.', color_light_ground, libtcod.black)

    #we are "blitting" our offscreen console oot the root console
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


while not display.display_closed():
    #show the map we made above

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

    render_all(newmap, display.con)
    libtcod.console_flush()
