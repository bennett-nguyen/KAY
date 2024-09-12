from src.app_state.app_state import AppState
from src.base_command import BaseCommand
from src.exports.commands import exported_core_cmds

class CommandManager:
    def __init__(self):
        self.loaded_commands: dict[str, BaseCommand] = {}
        self.load_commands(exported_core_cmds)
        
    def load_commands(self, exported_cmds: list[BaseCommand]):
        for cmd in exported_cmds:
            self.loaded_commands[cmd.parser.prog] = cmd

    def read_inputs(self, text: str, app_state: AppState):
        splited_text = text.split(" ")

        cmd_name = splited_text[0]
        args = splited_text[1:]

        if cmd_name not in self.loaded_commands:
            print("Command doesn't exist!")
            return

        self.loaded_commands[cmd_name].execute(args, app_state)