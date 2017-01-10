import sublime
from sublime import Region
import sublime_plugin


class InBetweenListener(sublime_plugin.EventListener):

    SELECT_MODE = 0
    invoked = False
    in_plugin = False
    dirty_file = True
    mode = None

    def on_modified(self, view):

        if not InBetweenListener.invoked:
            # resetting in_plugin in case it was already set.
            self.in_plugin = False
            return

        if self.in_plugin:
            # we don't want to remove the character again, it will crash
            InBetweenListener.invoked = False
            self.in_plugin = False
            return

        self.in_plugin = True

        last_char = self.remove_last(view)
        if not self.is_dirty:
            view.run_command("save")

        if self.mode == InBetweenListener.SELECT_MODE:
            self._select(view, last_char)

    def _select(self, view, last_char):
        for sel in view.sel():
            line = view.line(sel)
            line_left = Region(line.a, sel.a)
            line_right = Region(sel.b, line.b)
            to_sel = view.substr(line_left)
            from_sel = view.substr(line_right)
            left_found_pos = to_sel.rfind(last_char)
            right_found_pos = from_sel.find(last_char)
            to_select_reg = Region(
                left_found_pos + line.a + 1, right_found_pos + sel.a)

            if view.substr(to_select_reg.a).isspace():
                # This means it didn't match anything.
                return

            if to_select_reg.a <= sel.b and to_select_reg.b >= sel.a:
                view.sel().add(to_select_reg)

    def on_text_command(self, view, command_name, args):
        if InBetweenListener.invoked and self.in_plugin:
            # ignoring anything that might happen
            return "in_between_dummy", args

    def remove_last(self, view):
        """
        Removes the last character entered and returns it because we don't want to display it.
        """
        position = view.sel()[0].begin()
        region = sublime.Region(position, position - 1)
        character = view.substr(region)
        view.run_command("left_delete")
        return character


class InBetweenCommand(sublime_plugin.TextCommand):

    def run(self, edit, mode=None):
        if mode == "select":
            InBetweenListener.mode = InBetweenListener.SELECT_MODE
        else:
            # mode is not recognised
            return
        InBetweenListener.is_dirty = self.view.is_dirty()
        InBetweenListener.invoked = not InBetweenListener.invoked


class InBetweenDummyCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        return
