import pygame as pg
import preload.constants as const
from sys import exit
from pygame.locals import *

pg.init()

screen = pg.display.set_mode((const.WIDTH, const.HEIGHT))
clock = pg.time.Clock()

pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
pg.display.set_caption(f"Segment Tree Visualizer v{const.VERSION}")