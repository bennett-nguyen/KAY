import argparse
from typing import Optional
from collections import deque

from src.base_command import BaseCommand
from src.app_state.app_state import AppState
from src.exceptions import ArgumentError, CommandException

class Propagate(BaseCommand):
    def __init__(self):
        super().__init__(
            name="propagate",
            description="Manually propagate lazy values that may present in some nodes."
        )

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        segment_tree = app_state.tree_manager.segment_tree
        queue = deque([segment_tree.root])

        while queue:
            node = queue.popleft()
            segment_tree.propagate(node)

            if node.is_leaf():
                continue

            for child in node.children:
                queue.append(child)

propagate_cmd = Propagate()