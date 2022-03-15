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

import gedit
import gtk

from GetBeans.code_tools import CodeTools

get_edit_str = """
<ui>
  <menubar name="MenuBar">
    <menu name="EditMenu" action="Edit">
      <placeholder name="EditOps_3">
        <separator name="GetBeansEditingSep1"/>
        <menuitem name="Delete Line(s)"             action="DeleteLine"/>
        <menuitem name="Duplicate Line(s) Up"       action="DuplicateLineUp"/>
        <menuitem name="Duplicate Line(s) Down"     action="DuplicateLineDown"/>
        <menuitem name="Move Line(s) Up"            action="MoveLineUp"/>
        <menuitem name="Move Line(s) Down"          action="MoveLineDown"/>
        <separator name="GetBeansEditingSep2"/>
        <menuitem name="Multiple Lines Copy"        action="CopyLine"/>
        <menuitem name="Multiple Lines Cut"         action="CutLine"/>
        <menuitem name="Multiple Lines Comment"     action="CodeComment"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

def copy_line(window):  
    with CodeTools(window) as code:
        code.copy_text_to_clipboard()
        code.view.select_by_offsets(
            code.start.get_offset(),
            code.document.get_insert_offset(),
            code.end.get_offset()
        )

def comment_line(window):
    with CodeTools(window) as code:
        code.comment_text()
        code.document.write(code.text)
        code.view.select_by_offsets(
            code.current_start_offset,
            code.document.get_insert_offset(),
            code.current_start_offset + code.selection
        )

def duplicate_line(window, down=True):
    with CodeTools(window) as code:
        start = (code.current_start_offset + 1 + len(code.text)) if down else code.current_start_offset
        code.select_and_delete()
        code.document.write(code.text+"\n")
        code.document.write(code.text)
        code.view.select_by_offsets(
            start,
            code.document.get_insert_offset(),
            start + code.selection
        )

def move_line(window, down=True):
    with CodeTools(window) as code:
        lines = code.end.get_line() - code.start.get_line()
        start_line_offset = code.current_start_line_offset
        code.erase_line(down)
        code.document.write(code.text+"\n")
        code.view.move_line_cursor(-lines -1)
        code.view.move_position_cursor(start_line_offset)
        code.view.move_position_cursor(code.selection, select=True)

def delete_line(window):
    view = window.get_active_view()
    view.do_delete_from_cursor(view, gtk.DELETE_PARAGRAPHS, 1)

def cut_line(window):
    copy_line(window)
    delete_line(window)

class GetBeansPlugin(gedit.Plugin):
    DATA_TAG = "GetBeansPluginWindowDataKey"
    ACTION_GROUP = "GetBeansPluginActions"
    INFO = "GetBeansPluginInfo"
    ACTIONS = [
        ('DeleteLine',        None, 'Delete Line(s)',         '<Control>e',              "Delete Line",         lambda a,w: delete_line(w)),
        ('DuplicateLineUp',   None, 'Duplicate Line(s) Up',   '<Shift><Control>less',    "Duplicate Line Up",   lambda a,w: duplicate_line(w, down=False)),
        ('DuplicateLineDown', None, 'Duplicate Line(s) Down', '<Shift><Control>greater', "Duplicate Line Down", lambda a,w: duplicate_line(w, down=True)),
        ('MoveLineUp',        None, 'Move Line(s) Up',        '<Shift><Alt>less',        "Move Line Up",        lambda a,w: move_line(w, down=False)),
        ('MoveLineDown',      None, 'Move Line(s) Down',      '<Shift><Alt>greater',     "Move Line Down",      lambda a,w: move_line(w, down=True)),
        ('CopyLine',          None, 'Copy Multiple Lines',    '<Alt>c',                  "Copy Line",           lambda a,w: copy_line(w)),
        ('CutLine',           None, 'Cut Multiple Lines',     '<Alt>x',                  "Cut Line",            lambda a,w: cut_line(w)),
        ('CodeComment',       None, 'Comment Multiple Lines', '<Shift><Control>c',       "Code Comment",        lambda a,w: comment_line(w)),
    ]

    def __init__(self):
        gedit.Plugin.__init__(self)

    def activate(self, window):
        data = {}
        window.set_data(self.DATA_TAG, data)
        data["action_group"] = gtk.ActionGroup(self.ACTION_GROUP)
        data["action_group"].add_actions(self.ACTIONS, window)
        manager = window.get_ui_manager()
        manager.insert_action_group(data["action_group"], -1)
        data["ui_id"] = manager.add_ui_from_string(get_edit_str)
        window.set_data(self.INFO, data)

    def deactivate(self, window):
        data = window.get_data(self.DATA_TAG)
        manager = window.get_ui_manager()
        manager.remove_ui(data["ui_id"])
        manager.remove_action_group(data["action_group"])

    def update_ui(self, window):
        view = window.get_active_view()
        data = window.get_data(self.DATA_TAG)
        data["action_group"].set_sensitive(bool(view and view.get_editable()))

