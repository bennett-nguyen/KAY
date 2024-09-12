from src.app_state.app_state import AppState
from src.base_command import BaseCommand
from src.exports.commands import exported_core_cmds

class CommandManager:
    """Manages the loading and execution of commands in the application.

    This class is responsible for loading available commands, parsing user inputs,
    and executing the corresponding command with the provided arguments. It
    ensures that commands are properly registered and can be invoked by the user.
    """

    def __init__(self):
        self.loaded_commands: dict[str, BaseCommand] = {}
        self.load_commands(exported_core_cmds)

    def load_commands(self, exported_cmds: list[BaseCommand]):
        """Loads commands into the command manager.

        This method registers each command from the provided list into the
        loaded_commands dictionary, allowing them to be executed later. It
        maps the command's program name to its corresponding command object.

        Args:
            exported_cmds (list[BaseCommand]): A list of command objects to be loaded.
        """

        for cmd in exported_cmds:
            self.loaded_commands[cmd.parser.prog] = cmd

    def parse_inputs(self, text: str, app_state: AppState):
        """Parses user input and executes the corresponding command.

        This method splits the input text into a command name and its arguments,
        checks if the command exists in the loaded commands, and executes it with
        the provided application state. If the command does not exist, an error
        message is printed.

        Args:
            text (str): The input text containing the command and its arguments.
            app_state (AppState): The current state of the application.
        """

        splited_text = text.split(" ")

        cmd_name = splited_text[0]
        args = splited_text[1:]

        if cmd_name not in self.loaded_commands:
            print("Command doesn't exist!")
            return

        self.loaded_commands[cmd_name].execute(args, app_state)