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

from view import View
from document import Document
import math
import gtk

class CodeTools(object):

    def __init__(self, window):
        self.document = Document(window.get_active_document())
        self.view = View(window.get_active_view())
        self.start = None
        self.end = None
        self.lines = 0
        self.text = ""
        self.selection = 0
        self._initialize_text()

    def _initialize_text(self):
        self._get_code_selection()
        self.current_start_offset = self.start.get_offset()
        self.current_start_line_offset = self.start.get_line_offset()
        self.current_end_offset = self.end.get_offset()
        self.current_insert_offset = self.document.get_insert_offset()
        self._get_selection_character_count()
        self._define_selection_block()
        self.view.move_to_end_of_selection_block(self.document, self.end.get_line())
        self.text = self.document.read(self.start, self.end)

    def _get_code_selection(self):
        selection = self.document.get_selection()
        insert = self.document.get_insert() 
        (self.start, self.end) = selection or (insert, insert.copy())
        return (self.start, self.end)

    def _get_selection_character_count(self):
        self.selection = math.fabs(self.current_end_offset - self.current_start_offset)
        return self.selection
  
    def _define_selection_block(self):        
        self.lines = self.end.get_line()-self.start.get_line()
        self.start.set_line_offset(0)
        if not self.end.ends_line():
            self.end.forward_to_line_end()

    def select_and_delete(self):
        self.view.select_by_offsets(
            self.start.get_offset(),
            self.document.get_insert_offset(),
            self.end.get_offset()
        )
        self.document.delete()

    def comment_text(self):
        self.select_and_delete()
        code_comment = CodeComment(self.document, self.text)
        code_comment.analyze_comment_tags()
        code_comment.verify_commenting()
        code_comment.do_comment_or_uncomment()
        (self.current_start_offset, self.selection) = code_comment.calculate_new_position_values(self.current_start_offset, self.selection)
        self.text = code_comment.change_text()

    def copy_text_to_clipboard(self):
        clipboard = gtk.clipboard_get()
        clipboard.set_text(self.text)
        clipboard.store()

    def erase_line(self, down):
        self.select_and_delete()
        end_line = self.document.get_insert().copy()
        end_line.set_line_offset(0)
        end_line.forward_line()
        self.document.delete(self.document.get_insert(), end_line)
        self.view.move_line_cursor(1  if down else -1, select=False)
        
    def __enter__(self):
        self.document.begin_user_action()
        return self

    def __exit__(self, type, value, traceback):
        self.document.end_user_action()


class CodeComment(object):
    def __init__(self, document, text):
        self.lang = document.get_language()
        self.lines = text.split("\n")
        self.commenting = False
        (self.start_tag, self.end_tag) = ("", "")
        (self.s_size, self.e_size) = (0, 0)

    def _get_comment_tags(self):
        if not self.lang:
            return ("", "")        
        for lb in ["line", "block"]:
            start_tag = self.lang.get_metadata(lb+'-comment-start')
            end_tag = self.lang.get_metadata(lb+'-comment-end')
            if (start_tag, end_tag) != (None, None):
                return (start_tag if start_tag else "", end_tag if end_tag else "")        
        return ("", "")

    def analyze_comment_tags(self):
        (self.start_tag, self.end_tag) = self._get_comment_tags()
        self.s_size = len(self.start_tag) if len(self.start_tag) else None
        self.e_size = -len(self.end_tag) if len(self.end_tag) else None

    def verify_commenting(self):
        self.commenting = False
        for line in self.lines:
            if not line.find(self.start_tag) == 0:
               self.commenting = True
        return self.commenting

    def do_comment_or_uncomment(self):
        for i in range(len(self.lines)):
            line = self.lines[i]
            if self.commenting:
                line = self.start_tag + line + self.end_tag
            else:
                line = line[self.s_size : self.e_size]
            self.lines[i] = line

    def calculate_new_position_values(self, new_offset, selection):
        if self.commenting:
            new_offset += len(self.start_tag)
            selection += (len(self.lines)-1)*(len(self.start_tag) + len(self.end_tag))
        else:
            new_offset -= len(self.start_tag)
            selection -= (len(self.lines)-1)*(len(self.start_tag) + len(self.end_tag))
        return (new_offset, selection)

    def change_text(self):
        text = "\n".join(self.lines)
        return text
