from typing import Optional

from src.utils import VisibilityEnum
from src.base_command import BaseCommand
from src.app_state.app_state import AppState
from src.exceptions import ArgumentError, CommandException

class ViewNodeInfo(BaseCommand):
    def __init__(self):
        super().__init__(
            name="view-node-info",
            description="Toggle the visibility of a hovered node info."
        )

    def execute(self, args: list[str], app_state: AppState) -> Optional[ArgumentError | CommandException]:
        app_state.rendering.visibility_dict[VisibilityEnum.NODE_INFO_FIELD] = not app_state.rendering.visibility_dict[VisibilityEnum.NODE_INFO_FIELD]

view_node_info_cmd = ViewNodeInfo()