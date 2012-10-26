#
# deadhack
#
#http://roguebasin.roguelikedevelopment.org/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod,_part_1
#
# imports
#
#display library for trying to encapsulate graphics
from dh.game import display
#import libtcod - just required, has many parts
#like keyboard processing outside of graphics
from dh.lib import libtcodpy as libtcod
#made a placeholder but not used yet
#from lib import Player
#I needed support methods for logic and didn't know where to put them
from dh.game import support
#
# main method
#
#init basic display items
display.init()
#using mode as a placeholder here for game state,
#since we by default start mid-game.
mode = 'map'


#
# main logic loop
#
while not display.console():
    #draw() --what's this?

    #flush state to viewport this cycle
    display.flush()
    
    #get user input for game loop
    key = libtcod.console_wait_for_keypress(True)
    #process key we're given
    support.process_key(key,mode)
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

