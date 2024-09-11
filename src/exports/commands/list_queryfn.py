import argparse
from src.app_state.app_state import AppState
from src.base_command import BaseCommand

class ListQueryFN(BaseCommand):
    def __init__(self):
        super().__init__(
            name="list-queryfn",
            description="List out available query functions.",
            exit_on_error=False
        )

    def execute(self, args: list[str], app_state: AppState):
        for fn_name in app_state.tree_manager.available_functions.keys():
            print(fn_name)

list_query_fn_cmd = ListQueryFN()