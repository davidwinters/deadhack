from ..lib import libtcodpy as libtcod
from dh.game import support
import textwrap

#import shared message queue -
#the list of messages to be sent to viewport
messages = support.message_queue

class Display(object):
        """ handle to methods that write to screen """

        def __init__(self):
            '''initialize game console'''
            #set font for game
            libtcod.console_set_custom_font('dh/assets/terminal10x10_gs_tc.png',
                                            libtcod.FONT_TYPE_GREYSCALE |
                                            libtcod.FONT_LAYOUT_TCOD)
            #init window
            self.screen_width = 80
            self.screen_height = 70
            libtcod.console_init_root(self.screen_width, self.screen_height, 'deadhack', False)
            libtcod.console_set_foreground_color(0, libtcod.white)
            #flush screen to viewport
            libtcod.console_flush()
            #setup offscreen console
            self.con = libtcod.console_new(self.screen_width, self.screen_height)

        def draw_map(self, mode, map, fov_map):
            """ draw map to back console """
            libtcod.console_clear(self.con)
            #colours motherfuck do you has them
            color_light_wall = libtcod.Color(255, 255, 255)  # white
            color_dark_wall = libtcod.Color(0, 0, 100)
            color_light_ground = libtcod.Color(192, 192, 192)  # light grey
            color_dark_ground = libtcod.Color(50, 50, 150)
            for y in range(map.height):
                for x in range(map.width):
                    visible = libtcod.map_is_in_fov(fov_map, x, y)
                    wall = map.map[x][y].block_sight
                    if not visible:
                        if map.map[x][y].explored:
                            if wall:
                                libtcod.console_put_char_ex(self.con, x, y, '#',
                                                            color_dark_wall, libtcod.black)
                            else:
                                libtcod.console_put_char_ex(self.con, x, y, '.',
                                                        color_dark_ground, libtcod.black)

                    else:
                        if wall:
                            libtcod.console_put_char_ex(self.con, x, y, '#',
                                                        color_light_wall, libtcod.black)
                            map.map[x][y].explored = True
                        else:
                            libtcod.console_put_char_ex(self.con, x, y, '.',
                                                        color_light_ground, libtcod.black)
                            map.map[x][y].explored = True

        def calculate_fov(self, player, map):
            """ calc fov based on player loc onto map object """
            torch_radius = 10
            fov_light_walls = True
            fov_algo = 0
            #create a map object to hold fov data
            fov_map = libtcod.map_new(map.width, map.height)
            for y in range(map.height):
                for x in range(map.width):
                    libtcod.map_set_properties(fov_map, x, y,
                                               not map.map[x][y].block_sight,
                                               not map.map[x][y].blocked)
            libtcod.map_compute_fov(fov_map, player.x, player.y, torch_radius,
                                    fov_light_walls, fov_algo)
            return fov_map

        def draw_cast(self, mode, cast, player, fov_map):
            """ draw the actors on back console """
            libtcod.console_set_foreground_color(self.con, player.colour)
            libtcod.console_print_left(self.con, player.x, player.y, libtcod.BKGND_NONE, player.char)
            for object in cast:
                if libtcod.map_is_in_fov(fov_map, object.x, object.y):
                    libtcod.console_set_foreground_color(self.con, object.colour)
                    libtcod.console_print_left(self.con, object.x, object.y, libtcod.BKGND_NONE, object.char)

        def draw_doodads(self, doodads, map):
            for doodad in doodads:
                if map.map[doodad.x][doodad.y].explored == True:
                    libtcod.console_set_foreground_color(self.con, libtcod.white)
                    libtcod.console_print_left(self.con, doodad.x, doodad.y, libtcod.BKGND_NONE, doodad.char)

        def draw_containers(self, containers, map):
            for container in containers:
                if map.map[container.x][container.y].explored == True:
                    libtcod.console_set_foreground_color(self.con, libtcod.white)
                    libtcod.console_print_left(self.con, container.x, container.y, libtcod.BKGND_NONE, container.char)

        def display_closed(self):
            """ boolean is window closed (are we bailing?) """
            return libtcod.console_is_window_closed()

        def flush(self):
            """ flush back console to screen """
            libtcod.console_blit(self.con, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)
            libtcod.console_flush()

        def draw_gui(self, player, level_counter):
            """ draw all of the gui elements to the console """
            #create text notification area at top
            infobar = MessageBox(x=1, y=50, w=30, h=5)
            levelbox = LevelBox(x=40, y=50, w=30, h=5, level_counter=level_counter)
            for message, color in messages:
                #beautify queued messages
                infobar.append(message, color)
            #display beautified queued messages
            infobar.display(window=self.con)
            levelbox.display(window=self.con)


class GUIelement(object):
    """generic holder for any gui element"""
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class MessageBox(GUIelement):
    """ generic container for displaying messages/information on the game screen """
    def __init__(self, **kwargs):
        super(MessageBox, self).__init__(**kwargs)  # this super/kwargs shit is so we can use the variables defined in the parent class
        self.formatted_messages = []

    def append(self, message, colour):
        """add a message to the messagebox buffer"""
        #break lines if you need
        new_msg_lines = textwrap.wrap(message, self.w)

        for line in new_msg_lines:
            #if our display area is full remove the oldest messages
            if len(self.formatted_messages) == self.h:
                del self.formatted_messages[0]

            #add new messages
            self.formatted_messages.append((line, colour))

    def display(self, window):
        """ display this messagebox """
        y = self.y 
        for (line, color) in self.formatted_messages:
            line = line.ljust(self.w, ' ')
            libtcod.console_set_foreground_color(window, color)
            libtcod.console_print_left(window, self.x, y, libtcod.black, line)
            y += 1


class LevelBox(GUIelement):
    """ generic container for displaying current level """
    def __init__(self, level_counter, **kwargs):
        self.level_counter = level_counter
        super(LevelBox, self).__init__(**kwargs)  # this super/kwargs shit is so we can use the variables defined in the parent class
        self.formatted_messages = []

    def display(self, window):
        line = "Level " + str(self.level_counter)
        delete = "Level 00000000000"

        # clear the screen first
        libtcod.console_set_foreground_color(window, libtcod.black)
        libtcod.console_print_left(window, self.x, self.y, libtcod.black, delete)

        #display our current level
        libtcod.console_set_foreground_color(window, libtcod.white)
        libtcod.console_print_left(window, self.x, self.y, libtcod.black, line)
