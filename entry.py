import math
from sys import exit

import pygame as pg

import src.preload.system.window as window
import src.preload.system.constants as const
from src.MVC.controller import Controller
from src.preload.tree.segment_tree import SegmentTree

array = [1, 3, -2, 8, -7]
invalid_query_val = 0
function = lambda x, y: x + y

st = SegmentTree(array, invalid_query_val, function)
controller = Controller(st)

while True:
    window.screen.fill(controller.model.current_theme.BACKGROUND_CLR)
    dt_time = window.clock.tick(const.FPS) / 1000.0

    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

    controller.process(events, dt_time)
    controller.update_view()

    pg.display.update()
