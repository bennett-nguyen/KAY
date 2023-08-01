import pygame as pg
import src.preload.system.constants as const
from pygame.locals import *

pg.init()

screen = pg.display.set_mode((const.WIDTH, const.HEIGHT))
clock = pg.time.Clock()

pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
pg.display.set_caption(f"Segment Tree Visualizer v{const.VERSION}")