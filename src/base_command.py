from typing import Optional

from src.app_state.app_state import AppState
from src.override import ArgumentParserNoExit
from src.exceptions import CommandException, ArgumentError

class BaseCommand:
    """Represents a command with a parser for handling arguments.

    This class initializes an argument parser with optional parameters
    for name, usage, description, and epilog. It provides a method to execute
    the command with given app states, this allows components in the app to be accessible
    for the command to read, modify, and write. All command objects that will be used
    in the app must inherit from this class.
    """

    def __init__(self, name: Optional[str] = None, usage: Optional[str] = None, description: Optional[str] = None, \
        epilog: Optional[str] = None, exit_on_error: bool = False):
        self.parser = ArgumentParserNoExit(name, usage, description, epilog,
                                            exit_on_error=exit_on_error)

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        ...