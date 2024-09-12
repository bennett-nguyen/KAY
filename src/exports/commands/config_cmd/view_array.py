from src.utils import VisibilityEnum
from src.app_state.app_state import AppState
from src.base_command import BaseCommand

class ViewArray(BaseCommand):
    def __init__(self):
        super().__init__(
            name="view-array",
            description="Toggle the visibility of the segment tree's array."
        )

    def execute(self, args: list[str], app_state: AppState):
        app_state.rendering.visibility_dict[VisibilityEnum.ARRAY_FIELD] = not app_state.rendering.visibility_dict[VisibilityEnum.ARRAY_FIELD]

view_array_cmd = ViewArray()