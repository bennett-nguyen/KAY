from typing import NoReturn
from argparse import ArgumentParser

from src.exceptions import CommandException

class ArgumentParserNoExit(ArgumentParser):
    """
    A custom ArgumentParser that overrides the default error handling behavior.
    Instead of exiting the program on error, it raises a CommandException with the
    provided error message.
    """

    def error(self, message: str) -> NoReturn:
        raise CommandException(message)