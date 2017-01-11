# Copyright 2016 Arsham Shirvani <arshamshirvani@gmail.com>. All rights reserved.
# Use of this source code is governed by the Apache 2.0 license
# License that can be found in the LICENSE file.

from sublime import Region


class Constants:

    command_name = "in_between"

    SELECT_MODE = "select"
    NEXT_MODE = "next"
    BACK_MODE = "back"
    MODES = (SELECT_MODE, NEXT_MODE, BACK_MODE)

    RIGHT = 1
    LEFT = -1


class State:
    """
    Defines the current state of the plug-in
    """
    invoked = False
    in_plugin = False
    in_repeat = False
    dirty_file = True
    mode = None
    select = False

    def reset(self):
        self.invoked = False
        self.in_plugin = False
        self.in_repeat = False


state_object = None


def current_state():
    global state_object
    if state_object is None:
        state_object = State()
    return state_object


def remove_last(view):
    """
    Removes the last character entered and returns it because we don't want to display it.
    """
    position = view.sel()[0].begin()
    region = Region(position, position - 1)
    character = view.substr(region)
    view.run_command("left_delete")
    # undoing twice to remove the character and also retain the view's dirty state
    view.run_command("undo")
    view.run_command("undo")

    return character


def select(view, last_char):
    for sel in view.sel():
        current_line = view.line(sel)
        left_portion = Region(current_line.a, sel.a)
        right_portion = Region(sel.b, current_line.b)

        to_sel = view.substr(left_portion)
        from_sel = view.substr(right_portion)
        found_left_pos = to_sel.rfind(last_char)
        found_right_pos = from_sel.find(last_char)
        to_select_reg = Region(found_left_pos + current_line.a + 1, found_right_pos + sel.a)

        if view.substr(to_select_reg.a).isspace():
            # This means it didn't match anything.
            current_state().reset()
            return

        if to_select_reg.a <= sel.b and to_select_reg.b >= sel.a:
            view.sel().add(to_select_reg)


def to_next(view, last_char):
    return _find(view, last_char, Constants.RIGHT)


def to_back(view, last_char):
    return _find(view, last_char, Constants.LEFT)


def _find(view, last_char, direction):
    lines = {}  # selection of the cursor to line
    for sel in view.sel():
        a = min(sel.a, sel.b)
        b = max(sel.a, sel.b)

        # in case of going right, the current position is checked
        cell_check = 0
        if direction == Constants.LEFT:
            # otherwise the previous one
            cell_check = -1

        if a == b and view.substr(a + cell_check) == last_char:
            #  to move over the character if is the last_char already and look for the next
            a += direction
            b += direction
            sel = Region(a, b)
        lines[(a, b)] = view.line(sel)

    regions = []
    for sel, line in lines.items():
        regions.append(_get_found_regions(view, last_char, sel, line, direction))

    if regions:
        # because we don't want to clear the selection if there is no region
        view.sel().clear()
        for region in regions:
            view.sel().add(region)

    current_state().reset()


def _get_found_regions(view, last_char, sel, line, direction):
    if direction == Constants.RIGHT:
        line_portion = Region(sel[0], line.b)
    else:
        line_portion = Region(line.a, sel[1])

    from_sel = view.substr(line_portion)

    if direction == Constants.RIGHT:
        found_pos = from_sel.find(last_char)
    else:
        found_pos = from_sel.rfind(last_char)

    if found_pos > 0:
        # otherwise we didn't find anything
        if current_state().select:
            if direction == Constants.RIGHT:
                a = sel[0]
                b = sel[0] + found_pos
            else:
                a = line.a + found_pos
                b = sel[1]
        else:
            if direction == Constants.RIGHT:
                a = b = sel[0] + found_pos
            else:
                a = b = line.a + found_pos

        return Region(a, b)

    # for clearing only the region that can be advanced, we need to
    # push back the current selection
    return Region(sel[0], sel[1])
