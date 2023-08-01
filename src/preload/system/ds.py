import pygame as pg
import src.preload.system.constants as const
from pygame.locals import *

pg.init()

screen = pg.display.set_mode((const.WIDTH, const.HEIGHT))
clock = pg.time.Clock()
icon = pg.image.load("./icon/icon.ico").convert_alpha()

pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
pg.display.set_caption(f"Segment Tree Visualizer v{const.VERSION}")
pg.display.set_icon(icon)