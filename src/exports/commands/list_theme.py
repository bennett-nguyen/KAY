import argparse
from src.app_state.app_state import AppState
from src.base_command import BaseCommand

class ListTheme(BaseCommand):
    def __init__(self):
        super().__init__(
            name="list-theme",
            description="List out available themes.",
            exit_on_error=False
        )
    
    def execute(self, args: list[str], app_state: AppState):
        for theme in app_state.theme_manager.available_themes:
            print(theme)

list_theme_cmd = ListTheme()