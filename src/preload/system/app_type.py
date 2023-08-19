import pygame as pg
from collections import namedtuple
from collections.abc import Sequence
from typing import Union, TypeAlias, NewType


# -- Theme
ThemeField: TypeAlias = str

# Format: [r, g, b] | (r, g, b)
# Where r, g, b are non-negative integers within [0; 255]
RGB_Format: TypeAlias = Sequence[int, int, int]

# Format: [r, g, b, a] | (r, g, b, a)
# Where r, g, b, a are non-negative integers within [0; 255]
RGBA_Format: TypeAlias = Sequence[int, int, int, int]

# Format: Any valid format of Python literal 'int' type's value
# It's recommended to use hex format for readability
# Format hex: 0xrrggbbaa
# Where rr, gg, bb, and aa are 2-digit hex numbers within [0x00; 0xFF] (aa is compulsory)
# Notice: this is an 'int' literal, not a string
NumberFormat: TypeAlias = int

# Format: "0xrrggbb" or "0xrrggbbaa"
# Where rr, gg, bb, and aa are 2-digit hex numbers within [0x00; 0xFF]
HexStrFormat: TypeAlias = str

# Format: "#rrggbb" or "#rrggbbaa"
# Where rr, gg, bb, and aa are 2-digit hex numbers within [0x00; 0xFF]
HTMLColorFormat: TypeAlias = str

# All supported color name strings in https://www.pygame.org/docs/ref/color_list.html
NamedColors: TypeAlias = str

# All accepted color formats according to pygame.Color documentations https://www.pygame.org/docs/ref/color.html
ValidColorFormats: TypeAlias = Union[
    RGB_Format,
    RGBA_Format,
    NumberFormat,
    HexStrFormat,
    HTMLColorFormat,
    NamedColors,
    pg.Color
]

# Available and recommended color formats whose syntax are valid in Pygame and JSON
ValidJSONColorFormats: TypeAlias = Union[
    RGB_Format,
    RGBA_Format,
    HexStrFormat,
    HTMLColorFormat,
    NamedColors
]
# --

# Contours
ContourType = NewType("ContourType", str)

# Visibility Field
VisibilityField = NewType("VisibilityField", str)

# Command's Argument metadata
Argument = namedtuple("Argument", ("name", "type", "is_optional"))

# Message Box Links
WebLink = NewType("WebLink", str)