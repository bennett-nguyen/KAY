from typing import Optional
import argparse

from src.app_state.app_state import AppState

class BaseCommand:
    def __init__(self, name: Optional[str] = None, usage: Optional[str] = None, description: Optional[str] = None, \
        epilog: Optional[str] = None, exit_on_error: bool = False):
        self.parser = argparse.ArgumentParser(name, usage, description, epilog,
                                            exit_on_error=exit_on_error)

    def execute(self, args: list[str], app_state: AppState):
        ...