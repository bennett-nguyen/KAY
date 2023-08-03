import math
import pygame as pg
import src.preload.system.ds as ds
import src.preload.system.constants as const

from sys import exit
from src.MVC.controller import Controller
from src.preload.business_objects.segment_tree import SegmentTree

array = [3, 6, 4, 8, 2]
invalid_query_val = 0
query_function = update_function = math.gcd

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
    

    controller.receive_events(events)
    controller.update_view()

    pg.display.update()
