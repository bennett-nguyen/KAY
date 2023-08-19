from typing import List

import src.preload.system.constants as const
import src.preload.algorithm.reingold_tilford as RT
from src.preload.system.app_type import Argument
from src.preload.business_objects.app_ui import MessageTextBoxUI
from src.preload.business_objects.segment_tree import SegmentTree


# SECTION: HIDDEN IMPLEMENTATIONS
def _rebuild_tree(segment_tree: SegmentTree):
    segment_tree.rebuild()
    RT.calculate_node_position(segment_tree.root)
    RT.move_node_by_delta_pos(segment_tree.root, const.HALF_WIDTH - segment_tree.root.x, 0)


def _generate_help_header(message_box_ui: MessageTextBoxUI, available_commands, command):
    command_information_header = f"<b><i>{message_box_ui.generate_text(command, message_box_ui.current_theme.COMMAND_CLR, const.H2)}</i></b>"
    arguments_metadata: list[Argument] = available_commands[command].arguments

    argument_information_header = ""

    for argument_metadata in arguments_metadata:
        argument_text = message_box_ui.generate_text(argument_metadata.name, message_box_ui.current_theme.ARGUMENT_NAME_CLR, const.H2)
        colon_text = message_box_ui.generate_text(":", message_box_ui.current_theme.COLON_CLR, const.H2)
        type_text = message_box_ui.generate_text(f"<i>{argument_metadata.type.__name__}</i>", message_box_ui.current_theme.TYPE_CLR, const.H2)
        optional_notation_text = ""
        
        if argument_metadata.is_optional:
            optional_notation_text = message_box_ui.generate_text('*', message_box_ui.current_theme.OPTIONAL_NOTATION_CLR, const.H2)
        
        if len(argument_information_header) == 0:
            argument_information_header = f"{optional_notation_text}{argument_text}{colon_text}{type_text}"
        else:
            argument_information_header = f"{argument_information_header}  {optional_notation_text}{argument_text}{colon_text}{type_text}"

    message_box_ui.UI.set_text(f"{command_information_header}  {argument_information_header}")


# -- COMMANDS TO EXPORT
# SECTION: MODIFY AND REQUEST DATA FROM THE TREE
def cmd_insert(element: int, index: int = None, **kwargs):
    segment_tree: SegmentTree = kwargs["segment_tree"]
    array: List[int] = segment_tree.arr
    if index is None: index = len(array)

    array.insert(index, element)
    _rebuild_tree(segment_tree)

def cmd_remove(index: int = None, **kwargs):
    segment_tree: SegmentTree = kwargs["segment_tree"]
    message_box_ui: MessageTextBoxUI = kwargs["message_box_ui"]
    command_metadata = kwargs["command_metadata"]

    array: List[int] = segment_tree.arr
    if not array:
        message_box_ui.create_error(
            command_metadata.name,
            "cannot remove an element from an empty array.",
        )
        return

    if index is None: index = -1

    try:
        array.pop(index)
        _rebuild_tree(segment_tree)

    except IndexError as _:
        message_box_ui.create_error(command_metadata.name, f"index {index} is out of bound.")

def cmd_query(low: int, high: int, **kwargs):
    command_metadata = kwargs["command_metadata"]
    segment_tree: SegmentTree = kwargs["segment_tree"]
    message_box_ui: MessageTextBoxUI = kwargs["message_box_ui"]
    message_box_ui.create_output(command_metadata.name, message_box_ui.generate_text(f"{segment_tree.query(low, high)}", message_box_ui.current_theme.NORMAL_TEXT_CLR, const.H3))

def cmd_update(value: int, index: int, **kwargs):
    segment_tree: SegmentTree = kwargs["segment_tree"]
    message_box_ui: MessageTextBoxUI = kwargs["message_box_ui"]
    command_metadata = kwargs["command_metadata"]
    array: List[int] = segment_tree.arr

    try:
        array[index] = value
        _rebuild_tree(segment_tree)
    except IndexError as _:
        message_box_ui.create_error(command_metadata.name, f"index {index} is out of bound.")


# SECTION: MISCELLANEOUS
def cmd_home(**kwargs):
    segment_tree: SegmentTree = kwargs["segment_tree"]
    RT.move_node_by_delta_pos(
        segment_tree.root,
        const.HALF_WIDTH - segment_tree.root.x,
        const.DEPTH_OFFSET * const.VERTICAL_SCALE - segment_tree.root.y
    )


def cmd_help(command: str, **kwargs):
    command_metadata = kwargs["command_metadata"]
    available_commands = kwargs["available_commands"]
    message_box_ui: MessageTextBoxUI = kwargs["message_box_ui"]
    message_box_ui.should_display = True

    command_name_text = message_box_ui.generate_text(command, message_box_ui.current_theme.COMMAND_CLR, const.H3)
    if command not in available_commands:
        message_box_ui.create_error(command_metadata.name, f"command <i>{command_name_text}</i> was not found.")
        return

    message_box_ui.UI.show()
    message_box_ui.UI.clear()

    _generate_help_header(message_box_ui, available_commands, command)
    message_box_ui.UI.append_html_text(f"<br>{message_box_ui.generate_horizontal_rule()}<br><br>")

    description_text = message_box_ui.generate_text(f"{available_commands[command].description}", message_box_ui.current_theme.NORMAL_TEXT_CLR, const.H3)
    message_box_ui.UI.append_html_text(description_text)

def cmd_about(**kwargs):
    message_box_ui: MessageTextBoxUI = kwargs["message_box_ui"]
    message_box_ui.UI.show()
    message_box_ui.UI.clear()
    message_box_ui.create_about()