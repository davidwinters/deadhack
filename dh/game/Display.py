from ..lib import libtcodpy as libtcod


class Display():
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
            color_light_wall = libtcod.Color(255, 255, 255) #white
            color_light_ground = libtcod.Color(192, 192, 192) #light grey
            for y in range(map.height):
                for x in range(map.width):
                    wall = map.map[x][y].block_sight
                    if wall:
                        libtcod.console_put_char_ex(self.con, x, y, '#', color_light_wall, libtcod.black)
                    else:
                        libtcod.console_put_char_ex(self.con, x, y, '.', color_light_ground, libtcod.black)

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
