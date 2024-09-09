from enum import Enum, unique, auto

@unique
class ContourEnum(Enum):
    """
    Enumerates the possible sides for contour representation in a
    tree structure. This class defines two constants, LEFT and RIGHT,
    which can be used to specify the direction of contours in tree-related operations.

    Attributes:
        LEFT (str): Represents the left side contour.
        RIGHT (str): Represents the right side contour.
    """

    LEFT = "left"
    RIGHT = "right"

@unique
class VisibilityEnum(Enum):
    """
    Enumerates the different visibility fields used in the application.
    This class defines constants for various fields that can be displayed or hidden.

    Attributes:
        ARRAY_FIELD: Represents the visibility of the array field.
        NODE_DATA_FIELD: Represents the visibility of the node data field.
        NODE_INFO_FIELD: Represents the visibility of the node information field.
    """

    ARRAY_FIELD = auto()
    NODE_DATA_FIELD = auto()
    NODE_INFO_FIELD = auto()

@unique
class JSONThemeFieldsEnum(Enum):
    """
    Enumerates the fields used in JSON theme files that this app uses. 
    This class provides a set of constants that represent the various attributes 
    listed in a JSON theme file, facilitating safer data access.
    """

    NAME = "Name"
    PALETTE = "Palette"
    USE_DEFAULT_CMD_UI = "use_default_cmd_ui"

    BACKGROUND = "background"
    NODE_OUTLINE = "node_outline"
    NODE_OUTLINE_HIGHLIGHT = "node_outline_highlight"
    NODE_FILLINGS = "node_fillings"
    NODE_DISPLAY_DATA = "node_display_data"
    NODE_DISPLAY_DATA_HIGHLIGHT = "node_display_data_highlight"
    LINE = "line"
