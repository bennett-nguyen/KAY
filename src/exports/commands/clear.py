import argparse
from src.app_state.app_state import AppState
from src.base_command import BaseCommand

class Clear(BaseCommand):
    def __init__(self):
        super().__init__(
            name="clear",
            description="Clear the segment tree's array.",
            exit_on_error=False
        )
        
    def execute(self, args: list[str], app_state: AppState):
        tree_manager = app_state.tree_manager
        tree_manager.segment_tree.array.clear()
        tree_manager.generate_node_position()
        tree_manager.compute_transformed_coordinates()
        tree_manager.center_tree()

clear_cmd = Clear()