from src.preload.system.app_type import WebLink

# - General
WIDTH: int = 1440
HEIGHT: int = 900
RESOLUTION: tuple[int, int] = (WIDTH, HEIGHT)

HALF_WIDTH: int = WIDTH//2
HALF_HEIGHT: int = HEIGHT//2

ACTIVE_FPS: int = 48
IDLE_FPS: int = 1
VERSION: str = "0.7.0-prealpha"

# -- Array viewer and hovered node viewer's constants
MAX_X_PER_LINE: int = 500
ELEMENT_SPACING: int = 30
LINE_SPACING: int = 0
X_OFFSET: int = 30
Y_OFFSET: int = 20

# Zooming
MIN_ZOOM_LEVEL: float = 0.1
MAX_ZOOM_LEVEL: float = 2.0

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

# -- UI config files
THEME_IDENTIFIER_SUFFIX: str = "-app-theme"

# Message Box constants

# Header size
H1: int = 32
H2: int = 24
H3: int = 19
H4: int = 16
H5: int = 14
H6: int = 13

# Links
GITHUB_LINK: WebLink = WebLink("https://github.com/bennett-nguyen/KAY")
LICENSE_LINK: WebLink = WebLink("https://github.com/bennett-nguyen/KAY/blob/main/LICENSE")