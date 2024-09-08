import pygame as pg

from pygame.locals import *

from src.core.utils import const

pg.init()
pg.event.set_allowed(
    [
        QUIT,
        KEYDOWN,
        KEYUP,
        MOUSEBUTTONDOWN,
        MOUSEBUTTONUP,
        MOUSEMOTION,
        WINDOWFOCUSGAINED,
        WINDOWFOCUSLOST
    ]
)

screen = pg.display.set_mode(const.RESOLUTION)
clock = pg.time.Clock()
icon = pg.image.load("./icon/icon.ico").convert_alpha()

pg.display.set_caption(f"Segment Tree Visualizer v{const.VERSION}")
pg.display.set_icon(icon)
