from typing import Optional

from src.base_command import BaseCommand
from src.app_state.app_state import AppState
from src.exceptions import ArgumentError, CommandException

class Home(BaseCommand):
    def __init__(self):
        super().__init__(
            name="home",
            description="Move the tree to its original position."
        )

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        app_state.tree_manager.center_tree()

home_cmd = Home()