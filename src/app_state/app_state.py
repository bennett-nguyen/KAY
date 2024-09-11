from src.utils import VisibilityEnum
from src.app_state.states import ThemeManager, TreeManager, CMDLineInterface

class AppState:
    def __init__(self):
        """
        Initializes the model with the necessary components for managing themes and
        tree structures. This constructor sets up the theme manager, tree manager,
        visibility settings, and initial positions, ensuring that the application is
        ready for interaction.
        """

        self.theme_manager = ThemeManager()
        self.tree_manager = TreeManager([1, 3, -2, 8, -7])
        self.cmdline_interface = CMDLineInterface()

        self.visibility_dict: dict[VisibilityEnum, bool] = {
            VisibilityEnum.ARRAY_FIELD: True,
            VisibilityEnum.NODE_DATA_FIELD: True,
            VisibilityEnum.NODE_INFO_FIELD: True
        }
