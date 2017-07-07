#!/usr/bin/env python3

#
# css_autocompletion.py
#
# Copyright (C) 2015 Tobias Schönberg <tobias47n9e@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import gi
import os

gi.require_version("Gtk", "3.0")
gi.require_version("GtkSource", "3.0")
gi.require_version("GIRepository", "2.0")
gi.require_version("Ide", "1.0")

from gi.repository import GIRepository
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import GtkSource
from gi.repository import Ide

from suggestions import SUGGESTIONS

# 2 minutes
CACHE_EXPIRE_USEC = 2 * 60 * 1000 * 1000

_NamespaceIcon = Gio.ThemedIcon.new("lang-namespace-symbolic")

class CompletionProvider(Ide.Object,
                         GtkSource.CompletionProvider,
                         Ide.CompletionProvider):
    _libraries = None
    _libraries_expire_at = 0

    def do_get_name(self):
        return "CSS autocompletion"

    def do_get_icon(self):
        return None

    def do_populate(self, context):
        _, iter = context.get_iter()
        buffer = iter.get_buffer()

        copy = iter.copy()
        copy.set_line_offset(0)
        text = buffer.get_text(copy, iter, True)
        text = text.strip()

        for key in SUGGESTIONS:
            key_colon = "{}:".format(key)

            if text.startswith(key_colon):
                proposals = []
                value_text = text.replace(key_colon, "").strip()

                for item in SUGGESTIONS[key]:
                    item_completion = " {};".format(item)
                    proposal = CompletionProposal(self, context,
                                                  item_completion, value_text)
                    if (value_text == ""):
                        proposals.append(proposal)
                        continue

                    if (item.startswith(value_text)):
                        proposals.append(proposal)

                context.add_proposals(self, proposals, True)
                return

        context.add_proposals(self, [], True)

    def do_match(self, context):
        return True

    def do_get_info_widget(self, proposal):
        return None

    def do_update_info(self, proposal, info):
        pass

    def do_get_start_iter(self, context, proposal):
        _, iter = context.get_iter()
        return True, iter

    def do_activate_proposal(self, provider, proposal):
        return False, None

    def do_get_interactive_delay(self):
        return -1

    def do_get_priority(self):
        return 201


class CompletionProposal(GObject.Object, GtkSource.CompletionProposal):
    def __init__(self, provider, context, completion, start_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = provider
        self.context = context
        self.completion = completion
        self.complete = completion[len(start_text):]

    def do_get_label(self):
        return self.completion

    def do_get_markup(self):
        return self.completion

    def do_get_text(self):
        return self.complete

    def do_get_gicon(self):
        return _NamespaceIcon

    def do_hash(self):
        return hash(self.completion)

    def do_equal(self, other):
        return False

    def do_changed(self):
        pass

