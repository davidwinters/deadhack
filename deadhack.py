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
from dh.game import support, Map, Display, Monster, Player
import sys


#
# main method
#


#
# init game state
#

#init basic display items
display = Display.Display()

#craete map
current_level = Map.Map(50, 80, 1000, 10, 6)
current_level.make_map()
#create prototyping player and mpc
player = Player.Player()
npc = Monster.Monster()
#put actors in a cast to possibly paint on screen or wahtever
cast = [player, npc]
#game messages
#import shared message queue
#the list of messages to be sent to viewport
#start off with a hello message
messages = support.message_queue
messages.append(("Welcome to Deadhack", libtcod.white))
#print messages.popleft()
#sys.exit(0)
#game 'mode', eg inventory, menu, map
#we might change it
mode = 'map'
#
# gen valid positions on map for cast
for actor in cast:
    while current_level.map[actor.x][actor.y].blocked:
        actor.x = libtcod.random_get_int(0, 3, current_level.width - 3)
        actor.y = libtcod.random_get_int(0, 3, current_level.height - 3)
#
# main logic loop
#
while not display.display_closed():
    """ main loop """
    #
    # DISPLAY
    #
    fov_map = display.calculate_fov(player, current_level)
    display.draw_map(mode, current_level, fov_map)
    display.draw_cast(mode, cast, fov_map)
    display.draw_gui(player)
    #flush state to viewport this cycle
    display.flush()

    #
    # INPUT
    #
    #get user input for game loop
    key = libtcod.console_wait_for_keypress(True)
    #
    # LOGIC
    #
    #if esc - break out of game
    if key.vk == libtcod.KEY_ESCAPE:
        break
    #process key we're given and put into game objects
    support.process_keypress(key, mode, player)
    #let player move first
    player.move(current_level)

    # support.move(npc, current_level)
    npc.ai.act(current_level, player)
    #once we get the key things seem complicated.
    #some keys are player actions,
    #others are meta-game commands like option or quit
    #others are simply to get status info like inventory
    #that later involve game state updates =|

    #perform game logic
    #there may be many steps here!
    #things like timers, status effects, player updates, watever
    #update(key)


print "game finished!"
