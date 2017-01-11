import sublime
from sublime import Region
import sublime_plugin


class InBetweenListener(sublime_plugin.EventListener):

    SELECT_MODE = 0
    NEXT_MODE = 1
    REPEAT_MODE = 2

    invoked = False
    in_plugin = False
    in_repeat = False
    dirty_file = True
    mode = None

    def _reset(self):
        self.in_plugin = False
        self.in_repeat = False

    def on_modified(self, view):

        if not InBetweenListener.invoked:
            # resetting in_plugin in case it was already set.
            self._reset()
            return

        if self.in_plugin:
            # we don't want to remove the character again, it will crash
            InBetweenListener.invoked = False
            self._reset()
            return

        self.in_plugin = True

        last_char = self.remove_last(view)
        if not self.is_dirty:
            view.run_command("save")

        if self.mode == InBetweenListener.SELECT_MODE:
            self._select(view, last_char)
        elif self.mode == InBetweenListener.NEXT_MODE:
            self._next(view, last_char)
        elif self.mode == InBetweenListener.REPEAT_MODE:
            if self.in_repeat:
                return self._repeat(view, last_char)
            self.in_repeat = True

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
                self._reset()
                return

            if to_select_reg.a <= sel.b and to_select_reg.b >= sel.a:
                view.sel().add(to_select_reg)

    def _next(self, view, last_char):
        lines = {}  # position of the cursor to line
        for sel in view.sel():
            lines[sel.a] = view.line(sel)
        regions = []

        for pos, line in lines.items():
            line_right = Region(pos, line.b)
            from_sel = view.substr(line_right)
            right_found_pos = from_sel.find(last_char)
            if right_found_pos > 0:
                # otherwise we didn't find anything
                regions.append(Region(pos + right_found_pos, pos + right_found_pos))

        if regions:
            # because we don't want to clear the selection if there is no region
            # TODO: clear only the region that can be advanced
            view.sel().clear()
            for region in regions:
                view.sel().add(region)
        self._reset()

    def _repeat(self, view, last_char):
        # TODO: get the rest of the numbers
        for i in range(int(last_char)):
            view.run_command(self.command_name, self.args)
        self._reset()

    def on_text_command(self, view, command_name, args):
        if InBetweenListener.invoked and self.in_plugin:
            # ignoring anything that might happen
            return "in_between_dummy", args

        self.command_name = command_name
        self.args = args

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
        elif mode == "next":
            InBetweenListener.mode = InBetweenListener.NEXT_MODE
        elif mode == "repeat":
            InBetweenListener.mode = InBetweenListener.REPEAT_MODE
        else:
            # mode is not recognised
            return
        InBetweenListener.is_dirty = self.view.is_dirty()
        InBetweenListener.invoked = not InBetweenListener.invoked


class InBetweenDummyCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        return
