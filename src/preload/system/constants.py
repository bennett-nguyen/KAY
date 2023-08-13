from typing import Tuple
from src.preload.system.app_type import ContourType, VisibilityField

# - General
WIDTH: int = 1300
HEIGHT: int = 700
RESOLUTION: Tuple[int, int] = (WIDTH, HEIGHT)

HALF_WIDTH: int = WIDTH//2
HALF_HEIGHT: int = HEIGHT//2

FPS: int = 48
VERSION: str = "0.5.0-prealpha"

# -- App UI
THEME_DROP_DOWN_OBJ_ID: str = "#theme-selection-drop-down"
VISIBILITY_WINDOW_OBJ_ID: str = "#visibility-window"
VISIBILITY_DROP_DOWN_OBJ_ID: str = "#visibility-drop-down"

THEME_DROP_DOWN_WIDTH: int = 250
THEME_DROP_DOWN_HEIGHT: int = 40
THEME_DROP_DOWN_OFFSET: int = 30

VISIBILITY_WINDOW_WIDTH: int = 400
VISIBILITY_WINDOW_HEIGHT: int = 315

VISIBILITY_OFFSET_WIDTH: int = 32
VISIBILITY_OFFSET_HEIGHT: int = 60
VISIBILITY_DROP_DOWN_WIDTH: int = VISIBILITY_WINDOW_WIDTH - VISIBILITY_OFFSET_WIDTH
VISIBILITY_DROP_DOWN_HEIGHT: int = VISIBILITY_WINDOW_HEIGHT - VISIBILITY_OFFSET_HEIGHT

# -- Visibility Fields
VIEW_ARRAY_FIELD = VisibilityField("View Array")
VIEW_NODE_DATA_FIELD = VisibilityField("View Node Data")
VIEW_NODE_INFO_FIELD = VisibilityField("View Node Info")
DISPLAY_THEME_SELECTION_FIELD = VisibilityField("Display Theme Selection")

# -- Array viewer and hovered node viewer's constants
MAX_X_PER_LINE: int = 500
ELEMENT_SPACING: int = 30
LINE_SPACING: int = 0
X_OFFSET: int = 30
Y_OFFSET: int = 20


# - RT's algo constants
# -- Scalar
SCALE: int = 200
VERTICAL_SCALE: int = 150

# -- Offset
DEPTH_OFFSET: float = 1
ROOT_DEPTH: int = 0

# -- Shape's properties
LINE_THICKNESS: int = 4
NODE_CIRCLE_RADIUS: int = 40

# -- Distance between nodes and subtrees
NODE_DISTANCE: float = 0.7
SIBLING_DISTANCE: float = 0.0
TREE_DISTANCE: float = 0.0

# -- Contours
CONTOUR_LEFT: ContourType = ContourType("left")
CONTOUR_RIGHT: ContourType = ContourType("right")

# -- UI config files
DEFAULT_UI_FILE: str = "./theme/default_ui.json"
CUSTOM_UI_FILE: str = "app_ui.json"
ACTIVE_UI_FILE: str = "./theme/app-theme.json"
THEME_IDENTIFIER_SUFFIX: str = "-app-theme"
