import argparse
from src.utils import VisibilityEnum
from src.app_state.app_state import AppState
from src.base_command import BaseCommand

class ViewNodeInfo(BaseCommand):
    def __init__(self):
        super().__init__(
            name="view-node-info",
            description="Toggle the visibility of a hovered node info."
        )

    def execute(self, args: list[str], app_state: AppState):
        app_state.rendering.visibility_dict[VisibilityEnum.NODE_INFO_FIELD] = not app_state.rendering.visibility_dict[VisibilityEnum.NODE_INFO_FIELD]

view_node_info_cmd = ViewNodeInfo()