from ..lib import libtcodpy as libtcod
import textwrap


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
            self.screen_height = 80
            libtcod.console_init_root(self.screen_width, self.screen_height, 'deadhack', False)
            libtcod.console_set_foreground_color(0, libtcod.white)
            #flush screen to viewport
            libtcod.console_flush()
            #setup offscreen console
            self.con = libtcod.console_new(self.screen_width, self.screen_height)

        def draw_map(self, mode, map):
            """ draw map to back console """
            #colours motherfuck do you has them
            color_light_wall = libtcod.Color(255, 255, 255)  # white
            color_dark_wall = libtcod.Color(0, 0, 100)
            color_light_ground = libtcod.Color(192, 192, 192)  # light grey
            color_dark_ground = libtcod.Color(50, 50, 150)
            for y in range(map.height):
                for x in range(map.width):
                    wall = map.map[x][y].block_sight
                    if wall:
                        libtcod.console_put_char_ex(self.con, x, y, '#', color_light_wall, libtcod.black)
                    else:
                        libtcod.console_put_char_ex(self.con, x, y, '.', color_light_ground, libtcod.black)

        def calcluate_fov(self, player, map):
            """ calc fov based on player loc onto map object """
            torch_radius = 10
            fov_light_walls = True
            fov_algo = 0
            libtcod.map(map, player.x, player.y, torch_radius, fov_light_walls,
                        fov_algo)

        def draw_cast(self, mode, cast):
            """ draw the actors on back console """
            for object in cast:
                libtcod.console_set_foreground_color(self.con, object.colour)
                libtcod.console_print_left(self.con, object.x, object.y, libtcod.BKGND_NONE, object.char)

        def display_closed(self):
            """ boolean is window closed (are we bailing?) """
            return libtcod.console_is_window_closed()

        def flush(self):
            """ flush back console to screen """
            libtcod.console_blit(self.con, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)
            libtcod.console_flush()

        def draw_gui(self, player, messages):
            """ draw all of the gui elements to the console """
            messagebox = MessageBox(x=1, y=1, w=self.screen_width, h=5)
            for message, color in messages:
                messagebox.append(message, color)
            messagebox.display(window=self.con)


class GUIelement(object):
    """generic holder for any gui element"""
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class MessageBox(GUIelement):
    """game messages printed at top of screen"""
    def __init__(self, **kwargs):
        super(MessageBox, self).__init__(**kwargs)  # this super/kwargs shit is so we can use the variables defined in the parent class
        self.messages = []

    def append(self, message, colour):
        """add a message to our buffer"""
        #break lines if you need
        new_msg_lines = textwrap.wrap(message, self.w)

        for line in new_msg_lines:
            #clear buffer
            if len(self.messages) == self.h:
                del self.messages[0]

            #add new messages
            self.messages.append((line, colour))

    def display(self, window):
        y = 1
        for (line, color) in self.messages:
            libtcod.console_set_foreground_color(window, color)
            libtcod.console_print_left(window, self.x, y, libtcod.black, line)
            y += 1
