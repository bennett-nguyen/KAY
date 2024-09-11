import argparse
from src.app_state.app_state import AppState
from src.base_command import BaseCommand

class Theme(BaseCommand):
    def __init__(self):
        super().__init__(
            name="theme",
            description="Set the application's theme.",
            exit_on_error=False
        )

        self.parser.add_argument("theme_name", type=str)

    def execute(self, args: list[str], app_state: AppState):
        parsed_args: argparse.Namespace = self.parser.parse_args(args)
        app_state.theme_manager.set_theme(parsed_args.theme_name)
        app_state.cmdline_interface.set_theme(app_state.theme_manager.current_theme)

theme_cmd = Theme()