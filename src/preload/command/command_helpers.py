from src.preload.ui.app_ui import MessageTextBoxUI
from src.preload.system import constants as const
from src.preload.tree.segment_tree import SegmentTree
from src.preload.system.app_type import Argument
import src.preload.algorithm.reingold_tilford as RT

def rebuild_tree(segment_tree: SegmentTree):
    """Rebuild and reposition the segment tree.

    This function rebuilds the structure of the given segment tree and recalculates the positions of its nodes. It ensures that the root node is centered horizontally after the rebuild operation.

    Args:
        segment_tree (SegmentTree): The segment tree to be rebuilt and repositioned.
    """
    segment_tree.rebuild()
    RT.calculate_node_position(segment_tree.root)
    RT.move_node_by_delta_pos(segment_tree.root, const.HALF_WIDTH - segment_tree.root.x, 0)


def generate_help_header(message_box_ui: MessageTextBoxUI, available_commands, command):
    """Generate and display the help header for a specified command.

    This function constructs a formatted header that includes the command name and its associated arguments, displaying them in the message box UI. It formats the command and argument names with appropriate styling and indicates whether arguments are optional.

    Args:
        message_box_ui (MessageTextBoxUI): The message box UI instance used to display the help information.
        available_commands: A collection of available commands with their metadata.
        command: The specific command for which to generate the help header.
    """
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