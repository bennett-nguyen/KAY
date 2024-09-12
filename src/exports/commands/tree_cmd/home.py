from src.app_state.app_state import AppState

from src.base_command import BaseCommand
from src.window import pygame_window
from src.utils import const

class Home(BaseCommand):
    def __init__(self):
        super().__init__(
            name="home",
            description="Move the tree to its original position."
        )
    
    def execute(self, args: list[str], app_state: AppState):
        app_state.tree_manager.center_tree()

home_cmd = Home()