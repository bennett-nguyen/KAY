from src.preload.system.app_type import ContourType

# - General
WIDTH: int = 1300
HEIGHT: int = 700

HALF_WIDTH: int = WIDTH//2
HALF_HEIGHT: int = HEIGHT//2

FPS: int = 48
VERSION: str = "0.4.3-prealpha"

# Array viewer and hovered node viewer's constants
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
