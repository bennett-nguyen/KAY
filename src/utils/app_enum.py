from enum import Enum, unique, auto

@unique
class ContourEnum(Enum):
    """
    Enumerates the possible sides for contour representation in a
    tree structure. This class defines two constants, LEFT and RIGHT,
    which can be used to specify the direction of contours in tree-related operations.

    Attributes:
        LEFT: Represents the left side contour.
        RIGHT: Represents the right side contour.
    """

    LEFT = auto()
    RIGHT = auto()

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

    BACKGROUND_CLR = "background_clr"

    NODE_INFO_TEXT_CLR = "node_info_text_clr"
    NODE_INFO_DATA_CLR = "node_info_data_clr"
    NODE_FILLINGS_CLR = "node_fillings_clr"
    NODE_OUTLINE_CLR = "node_outline_clr"
    NODE_DISPLAY_DATA_CLR = "node_display_data_clr"

    NODE_OUTLINE_HIGHLIGHT_CLR = "node_outline_highlight_clr"
    NODE_DISPLAY_DATA_HIGHLIGHT_CLR = "node_display_data_highlight_clr"
    NODE_LAZY_DATA_CLR = "node_lazy_data_clr"
    NODE_LAZY_DATA_HIGHLIGHT_CLR = "node_lazy_data_highlight_clr"

    ARRAY_TEXT_CLR="array_text_clr"
    ARRAY_HIGHLIGHT_CLR="array_highlight_clr"

    LINE_CLR = "line_clr"
    LINE_HIGHLIGHT_CLR = "line_highlight_clr"
    NODE_LAZY_LINE_CLR = "node_lazy_line_clr"
    NODE_LAZY_LINE_HIGHLIGHT_CLR = "node_lazy_line_highlight_clr"

@unique
class CommandRequestFields(Enum):
    """Enumeration for command request fields.

    This class defines a set of fields which commands
    can change when they are executed, the application will
    read whatever mapped data from these fields and make
    changes to some aspects of the app state.

    For example, a command can request which nodes are highlighted
    by specifying a range where those nodes' managed segments are
    inside of using HIGHLIGHT_RANGE_LOW and HIGHLIGHT_RANGE_HIGH.
    """

    HIGHLIGHT_RANGE_LOW = auto()
    HIGHLIGHT_RANGE_HIGH = auto()