import argparse
from typing import Optional

from src.app_state.app_state import AppState
from src.base_command import BaseCommand
from src.exceptions import ArgumentError, CommandException

class UpdateRange(BaseCommand):
    def __init__(self):
        super().__init__(
            name="update-range",
            description="Update a segment by adding each element by a value."
        )

        self.parser.add_argument("segment_low", type=int)
        self.parser.add_argument("segment_high", type=int)
        self.parser.add_argument("value", type=int)

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        try:
            parsed_args: argparse.Namespace = self.parser.parse_args(args)
            app_state.tree_manager.segment_tree.update_segment_lazy(parsed_args.value, parsed_args.segment_low, parsed_args.segment_high)
        except (ArgumentError, CommandException) as e:
            return e

update_range_cmd = UpdateRange()