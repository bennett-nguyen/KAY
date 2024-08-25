from typing import List, Optional

import src.preload.system.constants as const
import src.preload.algorithm.reingold_tilford as RT
from src.preload.ui.app_ui import MessageTextBoxUI
from src.preload.tree.segment_tree import SegmentTree
import src.preload.command.command_helpers as command_helpers


# SECTION: HIDDEN IMPLEMENTATIONS



# -- COMMANDS TO EXPORT
# SECTION: MODIFY AND REQUEST DATA FROM THE TREE
def cmd_insert(element: int, index: Optional[int] = None, **kwargs):
    """Insert an element into a segment tree at a specified index.

    This function adds a new element to the segment tree's underlying array at the given index. If no index is provided, the element is appended to the end of the array, and the segment tree is rebuilt to reflect the updated structure.

    Args:
        element (int): The element to be inserted into the segment tree.
        index (Optional[int]): The index at which to insert the element. If None, the element is appended to the end.
        **kwargs: Additional keyword arguments, including the segment tree instance.
    """
    segment_tree: SegmentTree = kwargs["segment_tree"]
    array: List[int] = segment_tree.arr
    if index is None: index = len(array)

    array.insert(index, element)
    command_helpers.rebuild_tree(segment_tree)

def cmd_remove(index: Optional[int] = None, **kwargs):
    """Remove an element from a segment tree at a specified index.

    This function removes an element from the segment tree's underlying array at the given index. If the array is empty, an error message is displayed; if the index is out of bounds, a corresponding error message is also shown, and the segment tree is rebuilt after a successful removal.

    Args:
        index (Optional[int]): The index of the element to be removed. If None, the last element is removed.
        **kwargs: Additional keyword arguments, including the segment tree instance, message box UI, and command metadata.
    """
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
        command_helpers.rebuild_tree(segment_tree)
    except IndexError as _:
        message_box_ui.create_error(command_metadata.name, f"index {index} is out of bound.")

def cmd_query(low: int, high: int, **kwargs):
    """Query the segment tree for a range of values.

    This function retrieves the result of a query on the segment tree for the specified range defined by the low and high parameters. The result is then displayed in the message box UI with appropriate formatting based on the current theme.

    Args:
        low (int): The lower bound of the range to query.
        high (int): The upper bound of the range to query.
        **kwargs: Additional keyword arguments, including the segment tree instance, message box UI, and command metadata.
    """
    command_metadata = kwargs["command_metadata"]
    segment_tree: SegmentTree = kwargs["segment_tree"]
    message_box_ui: MessageTextBoxUI = kwargs["message_box_ui"]
    message_box_ui.create_output(command_metadata.name, message_box_ui.generate_text(f"{segment_tree.query(low, high)}", message_box_ui.current_theme.NORMAL_TEXT_CLR, const.H3))

def cmd_update(value: int, index: int, **kwargs):
    """Update an element in the segment tree at a specified index.

    This function modifies the value of an element in the segment tree's underlying array at the given index. If the index is out of bounds, an error message is displayed in the message box UI, and the segment tree is rebuilt to reflect the updated structure if the update is successful.

    Args:
        value (int): The new value to be set at the specified index.
        index (int): The index of the element to be updated.
        **kwargs: Additional keyword arguments, including the segment tree instance, message box UI, and command metadata.
    """
    segment_tree: SegmentTree = kwargs["segment_tree"]
    message_box_ui: MessageTextBoxUI = kwargs["message_box_ui"]
    command_metadata = kwargs["command_metadata"]

    try:
        segment_tree.update(index, value)
    except IndexError as _:
        message_box_ui.create_error(command_metadata.name, f"index {index} is out of bound.")


# SECTION: MISCELLANEOUS
def cmd_home(**kwargs):
    """Move the root node of the segment tree to its original position.

    This function adjusts the position of the root node of the segment tree to a predefined original location based on the constants for width and depth. It ensures that the root node is centered and positioned correctly within the visual representation of the tree.

    Args:
        **kwargs: Additional keyword arguments, including the segment tree instance.
    """
    segment_tree: SegmentTree = kwargs["segment_tree"]
    RT.move_node_by_delta_pos(
        segment_tree.root,
        const.HALF_WIDTH - segment_tree.root.x,
        const.DEPTH_OFFSET * const.VERTICAL_SCALE - segment_tree.root.y
    )


def cmd_help(command: str, **kwargs):
    """Display help information for a specified command.

    This function retrieves and displays help information for a given command, including its description and usage. If the command is not found in the list of available commands, an error message is shown in the message box UI.

    Args:
        command (str): The name of the command for which to display help information.
        **kwargs: Additional keyword arguments, including command metadata, available commands, and the message box UI instance.
    """
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

    command_helpers.generate_help_header(message_box_ui, available_commands, command)
    message_box_ui.UI.append_html_text(f"<br>{message_box_ui.generate_horizontal_rule()}<br><br>")

    description_text = message_box_ui.generate_text(f"{available_commands[command].description}", message_box_ui.current_theme.NORMAL_TEXT_CLR, const.H3)
    message_box_ui.UI.append_html_text(description_text)

def cmd_about(**kwargs):
    """Display information about the application.

    This function shows an about message box that contains information regarding the application, such as its version and authors. It clears any existing content in the message box UI before displaying the about information.

    Args:
        **kwargs: Additional keyword arguments, including the message box UI instance.
    """
    message_box_ui: MessageTextBoxUI = kwargs["message_box_ui"]
    message_box_ui.UI.show()
    message_box_ui.UI.clear()
    message_box_ui.create_about()