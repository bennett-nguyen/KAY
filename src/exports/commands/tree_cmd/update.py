import argparse
from typing import Optional

from src.app_state.app_state import AppState
from src.base_command import BaseCommand
from src.exceptions import ArgumentError, CommandException

class Update(BaseCommand):
    def __init__(self):
        super().__init__(
            name="update",
            description="Update an element at a particular index with a given value.",
        )

        self.parser.add_argument("value", type=int)
        self.parser.add_argument("index", type=int)

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        try:
            parsed_args: argparse.Namespace = self.parser.parse_args(args)
            segment_tree = app_state.tree_manager.segment_tree
            segment_tree.update(parsed_args.index, parsed_args.value)
        except ArgumentError as e:
            return e
        except CommandException as e:
            return e

update_cmd = Update()