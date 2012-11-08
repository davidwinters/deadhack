#
# support.py
#
from ..lib import libtcodpy as libtcod

""" take key and inject it into game objects for logic """
def process_key(key, mode, player):
    """ take key and inject it into game objects for logic """
    if mode == 'map':
        if (key.vk == libtcod.KEY_UP or chr(key.c) == 'k'):
            player.push = "u"
        elif chr(key.c) == 'u':
            player.push = "ur"
        elif key.vk == libtcod.KEY_RIGHT or chr(key.c) == 'l':
            player.push = "r"
        elif chr(key.c) == "n":
            player.push = "dr"
        elif key.vk == libtcod.KEY_DOWN or chr(key.c) == 'j':
            player.push = "d"
        elif chr(key.c) == "b":
            player.push = "dl"
        elif key.vk == libtcod.KEY_LEFT or chr(key.c) == 'h':
            player.push = "l"
        elif chr(key.c) == "y":
            player.push = "ul"



""" so far I think this implies 'map' mode and no combat, just a move attempt
"""
def move(actor, map):
    """ so far I think this implies 'map' mode and no combat, just a move
    attempt """
    if actor.push == "u" and not map.map[actor.x][actor.y-1].blocked:
        actor.y -= 1
        actor.push = ""
    elif actor.push == "ur" and not map.map[actor.x+1][actor.y-1].blocked:
        actor.x += 1
        actor.y -= 1
        actor.push = ""
    elif actor.push == "r" and not map.map[actor.x+1][actor.y].blocked:
        actor.x += 1
        actor.push = ""
    elif actor.push == "dr" and not map.map[actor.x+1][actor.y+1].blocked:
        actor.x += 1
        actor.y += 1
        actor.push = ""
    elif actor.push == "d" and not map.map[actor.x][actor.y+1].blocked:
        actor.y += 1
        actor.push = ""
    elif actor.push == "dl" and not map.map[actor.x-1][actor.y+1].blocked:
        actor.x -= 1
        actor.y += 1
        actor.push = ""
    elif actor.push == "l" and not map.map[actor.x-1][actor.y].blocked:
        actor.x -= 1
        actor.push = ""
    elif actor.push == "ul" and not map.map[actor.x-1][actor.y-1].blocked:
        actor.x -= 1
        actor.y -= 1
        actor.push = ""


