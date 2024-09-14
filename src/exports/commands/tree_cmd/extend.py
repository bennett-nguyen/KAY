import argparse
from typing import Optional

from src.base_command import BaseCommand
from src.app_state.app_state import AppState
from src.exceptions import ArgumentError, CommandException

class Extend(BaseCommand):
    def __init__(self):
        super().__init__(
            name="extend",
            description="Extend the segment tree's array with a sequence of numbers. If an index were given, it will insert that sequence at that index.",
        )

        self.parser.add_argument("sequence", type=int, nargs="+")
        self.parser.add_argument("-i", "--index", "-index", type=int, nargs="?", default=-1)

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        try:
            parsed_args: argparse.Namespace = self.parser.parse_args(args)
            tree_manager = app_state.tree_manager
            segment_tree = tree_manager.segment_tree

            index_to_extend = len(segment_tree.array)
            if (parsed_args.index != -1):
                index_to_extend = parsed_args.index

            segment_tree.array[index_to_extend:index_to_extend] = parsed_args.sequence
            segment_tree.rebuild()
            tree_manager.generate_node_position()
            tree_manager.compute_transformed_coordinates()
            tree_manager.center_tree()
        except ArgumentError as e:
            return e
        except CommandException as e:
            return e

extend_cmd = Extend()