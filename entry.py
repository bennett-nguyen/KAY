import math
from sys import exit

import pygame as pg

import src.preload.system.ds as ds
import src.preload.system.constants as const
from src.MVC.controller import Controller
from src.preload.business_objects.segment_tree import SegmentTree

array = [5, 2, 3, 5]
invalid_query_val = 0
query_function = update_function = lambda x, y: x + y

st = SegmentTree(array, invalid_query_val, query_function, update_function)
controller = Controller(st)

while True:
    ds.screen.fill(controller.model.current_theme.BACKGROUND_CLR)
    dt_time = ds.clock.tick(const.FPS) / 1000.0

    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

    controller.process(events, dt_time)
    controller.update_view()

    pg.display.update()
