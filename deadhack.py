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
from dh.game import support, Display, Monster, Player, Level
#import math


#
# main method
#


#
# init game state
#

#init basic display items
display = Display.Display()

# my new shit machine, WORK IN PROGRESS
level_counter = 0
levels = []
levels.append(Level.Level(level_counter))

player = Player.Player(x=0, y=0)


#game messages
#import shared message queue
#the list of messages to be sent to viewport
#start off with a hello message
messages = support.message_queue
messages.append(("Welcome to Deadhack", libtcod.white))

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
    while(True):
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_SHIFT:
            print 'shift!'
        else:
            break
    #process key we're given and put into game objects
    key_char = chr(key.vk)
    levelcheck = support.process_keypress(key, mode, player, level_counter, levels)
    #
    # LOGIC
    #
    #if esc - break out of game
    if key.vk == libtcod.KEY_ESCAPE:
        break

    #see if we need to change the level
    if levelcheck >= 0:  # this part in particular feels REALLY ghetto
        level_counter = levelcheck
        if len(levels) == level_counter + 1:
            pass  # a level already exists so don't need to append a new one

        else:
            levels.append(Level.Level(level_counter))
            player.x = levels[level_counter].doodads[0].x  # move our dude to the correct stairs
            player.y = levels[level_counter].doodads[0].y


    #let player move first
    player.move(levels[level_counter])

    # support.move(npc, current_level)
    for mob in levels[level_counter].mobs:
        if isinstance(mob, Monster.Monster):
            mob.ai.act(levels[level_counter], player)
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
