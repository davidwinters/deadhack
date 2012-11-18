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
from dh.game import support, Map, Display, Monster, Player, Level
import sys


#
# main method
#


#
# init game state
#

#init basic display items
display = Display.Display()

####### jon's old shit below
# current_level = Map.Map(50, 80, 7, 10, 6)
# current_level.make_map()
# #create prototyping player and mpc
# player = Player.Player()
# npc = Monster.Monster()
# #put actors in a cast to possibly paint on screen or wahtever
# cast = [player, npc]
####### end of jon's old shit

# my new shit machine, WORK IN PROGRESS
current_level = Level.Level(10)
player = Player.Player(x=0, y=0)
cast = [player]

for mob in current_level.mobs:
    cast.append(mob)

#game messages
#import shared message queue
#the list of messages to be sent to viewport
#start off with a hello message
messages = support.message_queue
messages.append(("Welcome to Deadhack", libtcod.white))
#print messages.popleft()
#game 'mode', eg inventory, menu, map
#we might change it
mode = 'map'
#
# put player on the stairs
player.x = current_level.doodads[0].x
player.y = current_level.doodads[0].y
#
# main logic loop
#
while not display.display_closed():
    """ main loop """
    #
    # DISPLAY
    #
    fov_map = display.calculate_fov(player, current_level.map)
    display.draw_map(mode, current_level.map, fov_map)
    display.draw_doodads(current_level.doodads, current_level.map)
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
    player.move(current_level.map)

    # support.move(npc, current_level)
    for mob in cast:
        if isinstance(mob, Monster.Monster):
            mob.ai.act(current_level.map, cast)
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
