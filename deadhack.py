#
# deadhack
#
#http://roguebasin.roguelikedevelopment.org/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod,_part_1
#
# imports
#
#libtcodpy! libtcod game library
from dh.lib import libtcodpy as libtcod
#main imports
from dh.game import support, Actor, Map, Display
#
# fuckass defs
#

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
#
# main method
#


#
# init game state
#

#init gamemode (by default mid-game)
#20121105 JRD I intend for this to be the main switch for
#game logic later but we will probably change it out.
#setting it to 'map' since so far we start mid-game

#initialize player object and npc
player = Actor.Actor(50,50,'@',libtcod.white)
npc = Actor.Actor(45, 45, '@', libtcod.yellow)
#put them in a cast to be painted on the canvas
cast = [player, npc]
#game 'mode', eg inventory, menu, map
mode = 'map'
#init basic display items
display = Display.Display()

# duping Dave's mapdemo shiznit, need to refactor!
#map settings
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
color_light_wall = libtcod.Color(255, 255, 255) #white
color_light_ground = libtcod.Color(192, 192, 192) #light grey
#craete map
current_level = Map.Map(50, 80, 1000, 10, 6)
current_level.make_map()
#
# main logic loop
#
while not display.display_closed():
    """ main loop """

    render_all(current_level, display.con)
    display.draw(mode, cast)

    #flush state to viewport this cycle ?? not sure what it does yet!
    display.flush()

    #get user input for game loop
    key = libtcod.console_wait_for_keypress(True)
    #process key we're given
    display.clear(mode, cast)
    support.process_key(key, mode, player)
    npc_x = libtcod.random_get_int(0, -1, 1)
    npc_y = libtcod.random_get_int(0, -1, 1)
    npc.move(npc_x, npc_y)
    #once we get the key things seem complicated.
    #some keys are player actions,
    #others are meta-game commands like option or quit
    #others are simply to get status info like inventory
    #that later involve game state updates =|

    #perform game logic
    #there may be many steps here!
    #things like timers, status effects, player updates, watever
    #update(key)

    #break out of game - should this be moved elsewhere?
    if key.vk == libtcod.KEY_ESCAPE:
        break

print 'game finished!'



