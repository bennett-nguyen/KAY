import pygame as pg
import preload.ds as ds
from preload.segment_tree import SegmentTree
from comp.visualizer import Visualizer
import preload.constants as const


class Host:
    def __init__(self, arr, invalid_query_val, query_fn, update_fn):
        self.st = SegmentTree(arr, invalid_query_val, query_fn, update_fn)
        self.visualizer = Visualizer(self, self.st.root)

    def redraw(self):
        self.visualizer.draw(self.st.root)

    def update(self, events):
        # self.user_input(events)
        self.redraw()

    def user_input(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.visualizer.change_view_scale(1)
                elif event.button == 5:
                    self.visualizer.change_view_scale(-1)
