from typing import Dict, List, Any, Callable

import pygame as pg

import src.preload.system.constants as const
import src.preload.algorithm.command_implementation as cmd
from src.preload.system.app_type import Argument
from src.preload.business_objects.app_ui import MessageTextBoxUI


class Command:
    def __init__(self, name: str, arguments: List[Argument], description: str, callback: Callable[[Any], Any], message_textbox_ui: MessageTextBoxUI):
        self.name = name
        self.arguments = arguments
        self.description = description
        self.callback = callback

        self.num_required_args = 0
        self.num_optional_args = 0
        self.num_args = len(self.arguments)

        for argument in self.arguments:
            if argument.is_optional:
                self.num_optional_args += 1
            else:
                self.num_required_args += 1

        self._message_textbox_ui = message_textbox_ui

        self._check_argument_syntax()

    def _check_valid_number_of_args(self, args: List[Any]) -> bool:
        num_of_given_args = len(args)
        command_name_text = self._message_textbox_ui.generate_text(self.name, self._message_textbox_ui.current_theme.COMMAND_CLR, const.H3)

        if self.num_required_args > num_of_given_args:
            self._message_textbox_ui.create_error(self.name, f"<i>{command_name_text}</i> command expected at least {self.num_required_args} argument(s), {num_of_given_args} were given.")
            return False

        if self.num_args < num_of_given_args:
            self._message_textbox_ui.create_error(self.name, f"<i>{command_name_text}</i> command expected {self.num_args} argument(s), {num_of_given_args} were given.")
            return False

        return True

    def _check_argument_syntax(self) -> None:
        if self.num_optional_args == 0:
            return

        found_required_argument = False

        for index in range(self.num_args-1, -1, -1):
            if not self.arguments[index].is_optional:
                found_required_argument = True
            elif found_required_argument:
                pg.quit()
                raise SyntaxError(f"Invalid argument syntax for command '{self.name}', all optional arguments must always come after required arguments!")

    def execute(self, *args, **kwargs):
        args = list(args)

        if not self._check_valid_number_of_args(args):
            return

        for index, argument in enumerate(args):
            argument_obj = self.arguments[index]
            try:
                args[index] = argument_obj.type(argument)
            except ValueError:
                self._message_textbox_ui.create_error(self.name, f"message: {self.name}: '{argument_obj.name}' expected type '{argument_obj.type}' for its value")
                return
        
        self._message_textbox_ui.should_display = False
        self.callback(*args, **kwargs, command_metadata=self, message_box_ui=self._message_textbox_ui)

        if not self._message_textbox_ui.should_display:
            self._message_textbox_ui.UI.hide()

class CommandManager:
    def __init__(self):
        self.commands: Dict[str, Command] = {}

    def init_commands(self, message_textbox_ui: MessageTextBoxUI):
        self.commands["insert"] = Command(
            name="insert",
            arguments=[
                Argument("element", int, False),
                Argument("index", int, True)
            ],
            description="Insert an element to an array at a particular index, insert to the end of the array if no index were given.",
            callback=cmd.cmd_insert,
            message_textbox_ui=message_textbox_ui
        )

        self.commands["remove"] = Command(
            name="remove",
            arguments=[Argument("index", int, True)],
            description="Remove an element at a particular index in the array, remove the last element if no index were given.",
            callback=cmd.cmd_remove,
            message_textbox_ui=message_textbox_ui
        )

        self.commands["update"] = Command(
            name="update",
            arguments=[
                Argument("value", int, False),
                Argument("index", int, False)
            ],
            description="Update an element at a particular index with a given value.",
            callback=cmd.cmd_update,
            message_textbox_ui=message_textbox_ui
        )

        self.commands["query"] = Command(
            name="query",
            arguments=[
                Argument("low", int, False),
                Argument("high", int, False)
            ],
            description="Query the value of the given segment in the tree.",
            callback=cmd.cmd_query,
            message_textbox_ui=message_textbox_ui
        )

        self.commands["home"] = Command(
            name="home",
            arguments=[],
            description="Move the tree to its original position.",
            callback=cmd.cmd_home,
            message_textbox_ui=message_textbox_ui
        )

        self.commands["help"] = Command(
            name="help",
            arguments=[Argument("command", str, False)],
            description="Display helpful information about a command.",
            callback=cmd.cmd_help,
            message_textbox_ui=message_textbox_ui
        )

        self.commands["about"] = Command(
            name="about",
            arguments=[],
            description="Display the application's information.",
            callback=cmd.cmd_about,
            message_textbox_ui=message_textbox_ui
        )
