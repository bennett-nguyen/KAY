import pygame as pg
import src.preload.system.constants as const
from pygame.locals import *
from pygame_gui._constants import (
    UI_DROP_DOWN_MENU_CHANGED
)

pg.init()
pg.event.set_allowed(
    [
        QUIT,
        KEYDOWN,
        KEYUP,
        MOUSEBUTTONDOWN,
        MOUSEBUTTONUP,
        MOUSEMOTION,
        UI_DROP_DOWN_MENU_CHANGED
    ]
)

screen = pg.display.set_mode(const.RESOLUTION)
clock = pg.time.Clock()
icon = pg.image.load("./icon/icon.ico").convert_alpha()

pg.display.set_caption(f"Segment Tree Visualizer v{const.VERSION}")
pg.display.set_icon(icon)
