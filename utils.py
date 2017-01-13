# Copyright 2016 Arsham Shirvani <arshamshirvani@gmail.com>. All rights reserved.
# Use of this source code is governed by the Apache 2.0 license
# License that can be found in the LICENSE file.

from sublime import Region


class Constants:

    BRACKETS = {
        "[": "]",
        "(": ")",
        "{": "}",
        "<": ">",
    }


class State:
    """
    Defines the current state of the plug-in.
    An object of this class the only source of the truth.
    """
    invoked = False
    in_plugin = False
    select = False

    def reset(self):
        self.invoked = False
        self.in_plugin = False


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
    # undoing twice to remove the character and also retain the view's dirty state.
    view.run_command("undo")
    view.run_command("undo")

    return character


def select(view, character):
    """
    selects the region around current position between both occurrences of the `character`
    """
    chars = get_char_pairs(character)
    for sel in view.sel():
        current_line = view.line(sel)
        left_portion = Region(current_line.a, sel.a)
        right_portion = Region(sel.b, current_line.b)

        # the left and right portion of the text to inspect.
        to_sel = view.substr(left_portion)
        from_sel = view.substr(right_portion)

        found_left_pos = to_sel.rfind(chars[0])
        found_right_pos = from_sel.find(chars[1])

        to_select_reg = Region(found_left_pos + current_line.a + 1, found_right_pos + sel.a)

        if view.substr(to_select_reg.a).isspace() or (to_select_reg.a == current_line.a and view.substr(to_select_reg.a) != character):
            # This means it didn't match anything.
            current_state().reset()
            return

        if to_select_reg.a <= sel.b and to_select_reg.b >= sel.a:
            view.sel().add(to_select_reg)


def get_char_pairs(character):
    """
    If the character is a bracket, it returns the beginning and ending
    parts. Otherwise it returns the character as both items.
    If the user presses the ending, it swaps the position.
    :rtype: tuple
    """
    if character in Constants.BRACKETS.keys():
        chars = (character, Constants.BRACKETS[character])

    elif character in Constants.BRACKETS.values():
        # the user pressed the closing part of the character
        char = {v: k for k, v in Constants.BRACKETS.items()}[character]
        chars = (char, character)

    else:
        chars = (character, character)
    return chars
