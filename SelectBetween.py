# Copyright 2016 Arsham Shirvani <arshamshirvani@gmail.com>. All rights reserved.
# Use of this source code is governed by the Apache 2.0 license
# License that can be found in the LICENSE file.

import sublime_plugin

from .utils import (
    remove_last,
    current_state,
    select,
)


class SelectBetweenListener(sublime_plugin.EventListener):
    """
    This listener observes the on_modified and on_text_command events on the view.
    It returns if the actions are not in the list or the plug-in is not invoked to
    prevent slow downs.
    """

    def on_text_command(self, view, command, args):
        if command != "select_between":
            # we don't want to intercept other activities
            current_state().reset()
            return

    def on_modified(self, view):

        if not current_state().invoked:
            # resetting in_plugin in case it was already set.
            current_state().reset()
            return

        if current_state().in_plugin:
            # we don't want to remove the character again, it will crash the
            # plug-in server.
            current_state().reset()
            return

        current_state().in_plugin = True
        entered_char = remove_last(view)

        select(view, entered_char)


class SelectBetweenCommand(sublime_plugin.TextCommand):

    def run(self, edit, select=False):
        current_state().select = select
        current_state().invoked = True
