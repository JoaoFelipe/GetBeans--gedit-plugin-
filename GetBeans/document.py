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

class Document(object):
    
    def __init__(self, document):
        self.document = document

    def get_insert(self):
        return self.document.get_iter_at_mark(self.document.get_insert())

    def get_insert_line(self):
        return self.get_insert().get_line()

    def get_insert_offset(self):
        return self.get_insert().get_offset()

    def get_selection(self):
        return self.document.get_selection_bounds()

    def get_line_count(self):
        return self.document.get_line_count() - 1

    def is_insert_at_last_line(self):
        return self.get_insert_line() == self.get_line_count()

    def write(self, text, pos=None):
        if pos:
            self.document.insert(pos, text)
        else:
            self.document.insert_at_cursor(text)

    def read(self, start_pos, end_pos):
        return self.document.get_slice(start_pos, end_pos, True)

    def delete(self, start=None, end=None):
        if start and end:
            self.document.delete(start, end)
        else:
            self.document.delete_selection(True, True)

    def begin_user_action(self):
        self.document.begin_user_action()

    def end_user_action(self):
        self.document.end_user_action()

    def get_language(self):
        return self.document.get_language()

