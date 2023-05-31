import tkinter.font
import tkinter as tk
import notebook.config as config
from notebook.config import *
from enum import Enum


class FormatAction(Enum):
    """Types of text changes."""
    FAMILY = 1,
    SIZE = 2,
    WEIGHT = 3,
    SLANT = 4,
    UNDERLINE = 5,
    TEXT_COLOR = 6,
    BACK_COLOR = 7


def create_combine_tag_for_selection(action, data, selected_tag):
    """Create a new tag based on the current tag and the text type change."""
    c_family, c_size, c_weight, c_slant, c_underline, c_text_color, c_back_color = map(
        str, selected_tag.split('_'))

    if action == FormatAction.FAMILY:
        return create_tag(data, c_size, c_weight, c_slant,
                          c_underline, c_text_color, c_back_color)
    elif action == FormatAction.SIZE:
        return create_tag(c_family, data, c_weight, c_slant,
                          c_underline, c_text_color, c_back_color)
    elif action == FormatAction.WEIGHT:
        return create_tag(c_family, c_size, data, c_slant,
                          c_underline, c_text_color, c_back_color)
    elif action == FormatAction.SLANT:
        return create_tag(c_family, c_size, c_weight, data,
                          c_underline, c_text_color, c_back_color)
    elif action == FormatAction.UNDERLINE:
        return create_tag(c_family, c_size, c_weight,
                          c_slant, data, c_text_color, c_back_color)
    elif action == FormatAction.TEXT_COLOR:
        return create_tag(c_family, c_size, c_weight,
                          c_slant, c_underline, data, c_back_color)
    elif action == FormatAction.BACK_COLOR:
        return create_tag(c_family, c_size, c_weight,
                          c_slant, c_underline, c_text_color, data)


def create_tag(family, size, weight, slant,
               underline, text_color, back_color):
    """Create a tag string from text parameters."""
    return f'{family}_{size}_{weight}_{slant}_{underline}_{text_color}_{back_color}'


def create_tags():
    """Create a list of all possible tags based on the config."""
    fonts = []

    for family in families:
        for size in sizes:
            for weight in weights:
                for slant in slants:
                    for underline in underlines:
                        for textColor in text_colors:
                            for backColor in back_colors:
                                fonts.append(
                                    create_tag(
                                        family,
                                        size,
                                        weight,
                                        slant,
                                        underline,
                                        color_codes.get(textColor),
                                        color_codes.get(backColor)))

    return fonts


def parse_tag(tag: str):
    """Convert tag string to font object."""
    family, size, weight, slant, underline, text_color, back_color = map_tag_string(
        tag)

    return tkinter.font.Font(
        family=family,
        size=size,
        weight=weight,
        slant=slant,
        underline=underline,
    ), text_color, back_color


def map_tag_string(tag: str):
    """Map tag string to items."""
    return tag.split('_')


def update_selected_text(text: tk.Text, action, data):
    """Change the text based on the text change parameter, the current text
    format and the selected text area."""
    try:
        index = text.index(f'{tk.SEL_FIRST}')
        while text.compare(index, '<', tk.SEL_LAST):

            index_tags = list(text.tag_names(index))
            current_index_tag = config.default_tag
            for index_tag in index_tags:

                if index_tag.count('_') == 6:
                    current_index_tag = index_tag

                text.tag_remove(index_tag, index)

            text.tag_add(
                create_combine_tag_for_selection(
                    action, data, current_index_tag), index)

            index = text.index(f'{index}+1c')
    except tk.TclError:
        pass


def set_text_by_tag_dump(tk_text: tk.Text, dump):
    """Set text to tkinter text widget by tags data."""
    for tag_text_pair in dump:
        text, tag = tag_text_pair
        tk_text.insert(tk.INSERT, text, tag)
