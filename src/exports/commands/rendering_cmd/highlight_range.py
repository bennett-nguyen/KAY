import argparse
from typing import Optional

from src.utils import CommandRequestFields
from src.app_state.app_state import AppState
from src.base_command import BaseCommand
from src.exceptions import ArgumentError, CommandException

class HighlightRange(BaseCommand):
    def __init__(self):
        super().__init__(
            name="highlight-range",
            description="Highlight the nodes whose segments is within the specified range.",
        )

        self.parser.add_argument("low", nargs="?", type=int, default=-1)
        self.parser.add_argument("high", nargs="?", type=int, default=-1)

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        try:
            parsed_args: argparse.Namespace = self.parser.parse_args(args)
            command_request_data = app_state.rendering.command_request_data
            command_request_data[CommandRequestFields.HIGHLIGHT_RANGE_LOW] = parsed_args.low
            command_request_data[CommandRequestFields.HIGHLIGHT_RANGE_HIGH] = parsed_args.high
        except ArgumentError as e:
            return e
        except CommandException as e:
            return e

highlight_range_cmd = HighlightRange()