from enum import Enum, unique, auto

@unique
class Contour(Enum):
    LEFT = "left"
    RIGHT = "right"

@unique
class Visibility(Enum):
    ARRAY_FIELD = auto()
    NODE_DATA_FIELD = auto()
    NODE_INFO_FIELD = auto()
