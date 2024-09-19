import argparse
from typing import Optional

from src.app_state.app_state import AppState
from src.base_command import BaseCommand
from src.exceptions import ArgumentError, CommandException

class Theme(BaseCommand):
    def __init__(self):
        super().__init__(
            name="theme",
            description="Set the application's theme.",
        )

        self.parser.add_argument("theme_name", type=str)

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        try:
            parsed_args: argparse.Namespace = self.parser.parse_args(args)
            app_state.theme_manager.set_theme(parsed_args.theme_name)
            app_state.cmdline_interface.set_theme(app_state.theme_manager.current_theme)
        except (ArgumentError, CommandException) as e:
            return e

theme_cmd = Theme()