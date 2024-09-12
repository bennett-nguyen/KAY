from src.utils import VisibilityEnum
from src.app_state.states import ThemeManager, TreeManager, CMDLineInterface, Rendering

class AppState:
    """Manages the overall state of the application.

    This class initializes the core components necessary for the application's
    functionality, including theme management, tree management with initial data,
    command line interface, and rendering. It serves as a central point for managing
    the application's state and interactions.
    
    Commands have access to the object instantiated from this class
    to modify, read, and write to change how the application behaves.
    """

    def __init__(self):
        self.theme_manager = ThemeManager()
        self.tree_manager = TreeManager([1, 3, -2, 8, -7])
        self.cmdline_interface = CMDLineInterface()
        self.rendering = Rendering()

