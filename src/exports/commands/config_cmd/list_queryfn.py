from typing import Optional

from src.app_state.app_state import AppState
from src.base_command import BaseCommand
from src.exceptions import ArgumentError, CommandException

class ListQueryFN(BaseCommand):
    def __init__(self):
        super().__init__(
            name="list-queryfn",
            description="List out available query functions.",
        )

    def execute(self, args: list[str], app_state: AppState)  -> Optional[ArgumentError | CommandException]:
        for fn_name in app_state.tree_manager.available_functions.keys():
            print(fn_name)

list_query_fn_cmd = ListQueryFN()