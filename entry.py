import pygame as pg
import preload.ds as ds
import preload.constants as const
from comp.host import Host
from sys import exit
from preload.segment_tree import SegmentTree

array = [2, 3, 1, 5, 1, 3, 5]
invalid_query_val = float("-inf")
query_function = update_function = max

st = SegmentTree(array, invalid_query_val, query_function, update_function)

host = Host(st)

while True:
    ds.screen.fill("White")
    ds.clock.tick(const.FPS)

    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)
    
    host.update(events)
    pg.display.flip()