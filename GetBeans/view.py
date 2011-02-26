# -*- coding: utf8 -*-

"""
GedBeans editing plugin

Copyright (C) 2011 João Felipe Nicolaci Pimentel <joaofelipenp@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 dated June, 1991.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Library General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

If you find any bugs or have any suggestions email: joaofelipenp@gmail.com
"""

import gtk
import math

class View(object):

    def __init__(self, view):
        self.view = view

    def move_line_cursor(self, number, select=False):
        if number:
            self.view.do_move_cursor(self.view, gtk.MOVEMENT_DISPLAY_LINES, number, int(select))

    def move_position_cursor(self, number, select=False):
        if number:
            self.view.do_move_cursor(self.view, gtk.MOVEMENT_VISUAL_POSITIONS, number, int(select))

    def move_to_begin_of_line(self, select=False):
        self.view.do_move_cursor(self.view, gtk.MOVEMENT_PARAGRAPH_ENDS, -1, int(select))

    def move_to_end_of_selection_block(self, document, end_line):
        selection_line_count = end_line - document.get_insert_line()
        self.move_line_cursor(-math.fabs(selection_line_count), select=False)
        self.move_to_begin_of_line(select=False)

    def select_by_offsets(self, start, current, end):
        self.move_position_cursor(start-current, select=False)
        self.move_position_cursor(end-start, select=True)
