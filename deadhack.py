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
import math


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
level_counter = 0
levels = []
levels.append(Level.Level(10))

player = Player.Player(x=0, y=0)


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
player.x = levels[level_counter].doodads[0].x
player.y = levels[level_counter].doodads[0].y
#
# main logic loop
#
while not display.display_closed():
    """ main loop """
    #
    # DISPLAY
    #
    fov_map = display.calculate_fov(player, levels[level_counter].map)
    display.draw_map(mode, levels[level_counter].map, fov_map)
    display.draw_doodads(levels[level_counter].doodads, levels[level_counter].map)
    display.draw_cast(mode, levels[level_counter].mobs, player, fov_map)
    display.draw_gui(player, level_counter)
    #flush state to viewport this cycle
    display.flush()

    #
    # INPUT
    #
    #get user input for game loop
    key = libtcod.console_wait_for_keypress(True)
    key_char = chr(key.c)
    #
    # LOGIC
    #
    #if esc - break out of game
    if key.vk == libtcod.KEY_ESCAPE:
        break
    elif key_char == ">":
        print "down"
        level_counter += -1
        if len(levels) < math.fabs(level_counter) + 1:
            levels.append(Level.Level(10))
    elif key_char == "<":
        print "up"
        level_counter += 1

    #process key we're given and put into game objects
    support.process_keypress(key, mode, player)
    #let player move first
    player.move(levels[level_counter].map)

    # support.move(npc, current_level)
    for mob in levels[level_counter].mobs:
        if isinstance(mob, Monster.Monster):
            mob.ai.act(levels[level_counter].map, levels[level_counter].mobs, player)
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
