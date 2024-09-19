import argparse
from typing import Optional

from src.base_command import BaseCommand
from src.app_state.app_state import AppState
from src.exceptions import ArgumentError, CommandException

class Remove(BaseCommand):
    def __init__(self):
        super().__init__(
            name="remove",
            description="Remove an element at a particular index in the array, remove the last element if no index were given.",
        )

        self.parser.add_argument("index", type=int, default=-1, nargs="?")

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        try:
            parsed_args: argparse.Namespace = self.parser.parse_args(args)
            tree_manager = app_state.tree_manager
            segment_tree = tree_manager.segment_tree
            
            index_to_remove = len(segment_tree.array)-1
            if (parsed_args.index != -1):
                index_to_remove = parsed_args.index

            segment_tree.array.pop(index_to_remove)
            segment_tree.rebuild()
            tree_manager.generate_node_position()
            tree_manager.compute_transformed_coordinates()
            tree_manager.center_tree()
        except (ArgumentError, CommandException) as e:
            return e

remove_cmd = Remove()