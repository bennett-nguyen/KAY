import argparse
from typing import Optional

from src.app_state.app_state import AppState
from src.base_command import BaseCommand
from src.exceptions import ArgumentError, CommandException

class QueryFN(BaseCommand):
    def __init__(self):
        super().__init__(
            name="query-fn",
            description="Change the segment tree's query function.",
        )

        self.parser.add_argument("fn_name", type=str)

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        try:
            parsed_args: argparse.Namespace = self.parser.parse_args(args)
            tree_manager = app_state.tree_manager
            segment_tree = app_state.tree_manager.segment_tree

            tree_manager.switch_function(parsed_args.fn_name)
            segment_tree.rebuild()
            tree_manager.generate_node_position()
            tree_manager.compute_transformed_coordinates()
            tree_manager.center_tree()
        except (ArgumentError, CommandException) as e:
            return e

query_fn_cmd = QueryFN()