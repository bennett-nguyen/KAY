from enum import Enum, unique, auto

@unique
class Contour(Enum):
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
class Visibility(Enum):
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
