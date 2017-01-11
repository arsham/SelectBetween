
import sublime_plugin

from .utils import (
    remove_last,
    current_state,
    Constants,
    select,
    to_next,
    to_back,
)


class InBetweenListener(sublime_plugin.EventListener):

    def on_text_command(self, view, command_name, args):
        if command_name != Constants.command_name:
            # we don't want to intercept other activities
            return

        current_state().command_name = command_name
        current_state().args = args

    def on_modified(self, view):

        if not current_state().invoked:
            # resetting in_plugin in case it was already set.
            current_state().reset()
            return

        if current_state().in_plugin:
            # we don't want to remove the character again, it will crash
            current_state().reset()
            return

        current_state().in_plugin = True
        last_char = remove_last(view)

        if current_state().mode == Constants.SELECT_MODE:
            select(view, last_char)
        elif current_state().mode == Constants.NEXT_MODE:
            to_next(view, last_char)
        elif current_state().mode == Constants.BACK_MODE:
            to_back(view, last_char)


class InBetweenCommand(sublime_plugin.TextCommand):

    def run(self, edit, mode=None, select=False):
        if mode not in Constants.MODES:
            # mode is not recognised
            current_state().reset()
            return

        current_state().mode = mode
        current_state().select = select
        current_state().invoked = not current_state().invoked
