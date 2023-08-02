# - General 
WIDTH: int = 1300
HEIGHT: int = 700

HALF_WIDTH: int = WIDTH//2
HALF_HEIGHT: int = HEIGHT//2

FPS: int = 48
VERSION: str = "0.2.1-prealpha"


# - RT's algo constants
# -- Scalar
SCALE = 200
VERTICAL_SCALE = 150

# -- Offset
DEPTH_OFFSET: float = 1
ROOT_DEPTH: float = 0

# -- Shape's properties
LINE_THICKNESS: int = 4
NODE_CIRCLE_RADIUS: int = 40

# -- Distance between nodes and subtrees
NODE_DISTANCE: float = 0.7
SIBLING_DISTANCE: float = 0.0
TREE_DISTANCE: float = 0.0

# -- Contours
CONTOUR_LEFT = "left"
CONTOUR_RIGHT = "right"
