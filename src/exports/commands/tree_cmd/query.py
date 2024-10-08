import argparse
from typing import Optional

from src.base_command import BaseCommand
from src.app_state.app_state import AppState
from src.exceptions import ArgumentError, CommandException

class Query(BaseCommand):
    def __init__(self):
        super().__init__(
            name="query",
            description="Query the segment tree for value from a given range.",
        )

        self.parser.add_argument("low", type=int)
        self.parser.add_argument("high", type=int)

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        try:
            parsed_args: argparse.Namespace = self.parser.parse_args(args)
            segment_tree = app_state.tree_manager.segment_tree
            print(segment_tree.query(parsed_args.low, parsed_args.high))
        except (ArgumentError, CommandException) as e:
            return e

query_cmd = Query()