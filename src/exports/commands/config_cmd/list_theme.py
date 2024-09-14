from typing import Optional

from src.app_state.app_state import AppState
from src.base_command import BaseCommand
from src.exceptions import ArgumentError, CommandException

class ListTheme(BaseCommand):
    def __init__(self):
        super().__init__(
            name="list-theme",
            description="List out available themes.",
        )

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        for theme in app_state.theme_manager.available_themes:
            print(theme)

list_theme_cmd = ListTheme()