from src.utils import kay_typing

# - General
DEFAULT_SCREEN_OCCUPATION_PERCENTAGE: float = 80 / 100

ACTIVE_FPS: int = 60
IDLE_FPS: int = 1
VERSION: str = "0.9.0-prealpha"

# -- Array viewer and hovered node viewer's constants
MAX_X_PER_LINE: int = 500
ELEMENT_SPACING: int = 30
LINE_SPACING: int = 0
X_OFFSET: int = 30
Y_OFFSET: int = 20

# Zooming
MIN_ZOOM_LEVEL: float = 0.1
MAX_ZOOM_LEVEL: float = 2.0
ZOOM_INTENSITY: float = 0.1

# - RT's algo constants
# -- Scalar
SCALE: int = 240
VERTICAL_SCALE: int = 160

# -- Offset
DEPTH_OFFSET: float = 1
ROOT_DEPTH: int = 0

# -- Shape's properties
CIRCLE_OUTLINE_THICKNESS: int = 4
LINE_THICKNESS: float = CIRCLE_OUTLINE_THICKNESS / 2.0
NODE_CIRCLE_RADIUS: int = 50

# -- Distance between nodes and subtrees
NODE_DISTANCE: float = 0.7
SIBLING_DISTANCE: float = 0.0
TREE_DISTANCE: float = 0.1

# -- UI config files
THEME_IDENTIFIER_SUFFIX: str = "-app-theme"
CMD_THEME_FILE: str = "theme/cmdline_ui-DO-NOT-EDIT.json"

# -- Command box
COMMAND_BOX_OBJECT_ID = "#command-box"
COMMAND_BOX_ANCHOR_OFFSET = 20
COMMAND_BOX_HEIGHT = 50

LAZY_LINE_LENGTH = 20
LAZY_LINE_THICKNESS = 1
LAZY_LINE_OFFSET = NODE_CIRCLE_RADIUS - CIRCLE_OUTLINE_THICKNESS - 5

HISTORY_SIZE_LIMIT: int = 100

# Links
GITHUB_LINK: kay_typing.WebLink = kay_typing.WebLink("https://github.com/bennett-nguyen/KAY")
LICENSE_LINK: kay_typing.WebLink = kay_typing.WebLink("https://github.com/bennett-nguyen/KAY/blob/main/LICENSE")

DEFAULT_CMD_THEME: str = """
{
    \"#command-box\": {
        \"colours\": {
            \"normal_border\": \"#5c6062\",
            \"dark_bg\": \"#313338\",
            \"normal_text\": \"#B5B2B4\",
            \"selected_bg\": \"#365880\",
            \"selected_text\": \"#B5B2B4\"
        },

        \"font\": {
            \"name\": \"Jetbrains Mono\",
            \"size\": 20,
            \"regular_path\": \"fonts/JetBrainsMonoNL-Regular.ttf\",
            \"bold_path\": \"fonts/JetBrainsMono-Bold.ttf\",
            \"italic_path\": \"fonts/JetBrainsMonoNL-LightItalic.ttf\",
            \"bold_italic_path\": \"fonts/JetBrainsMono-BoldItalic.ttf\"
        },

        \"misc\": {
            \"shape\": \"rounded_rectangle\",
            \"shape_corner_radius\": 10,
            \"padding\": \"10,2\"
        }
    }
}
"""