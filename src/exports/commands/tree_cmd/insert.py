import argparse
from src.app_state.app_state import AppState
from src.base_command import BaseCommand

class Insert(BaseCommand):
    def __init__(self):
        super().__init__(
            name="insert",
            description="Insert an element to an array at a particular index, insert to the end of the array if no index were given.",
        )
        
        self.parser.add_argument("value", type=int)
        self.parser.add_argument("index", type=int, default=-1, nargs='?')
        
    def execute(self, args: list[str], app_state: AppState):
        parsed_args: argparse.Namespace = self.parser.parse_args(args)
        tree_manager = app_state.tree_manager
        segment_tree = tree_manager.segment_tree
        
        index_to_insert = len(segment_tree.array)
        if (parsed_args.index != -1):
            index_to_insert = parsed_args.index

        segment_tree.array.insert(index_to_insert, parsed_args.value)
        segment_tree.rebuild()
        tree_manager.generate_node_position()
        tree_manager.compute_transformed_coordinates()
        tree_manager.center_tree()

insert_cmd = Insert()