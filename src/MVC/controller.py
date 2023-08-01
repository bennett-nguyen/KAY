import pygame as pg
from src.MVC.view import View
from src.MVC.model import Model
from src.preload.business_objects.segment_tree import SegmentTree

class Controller:
    def __init__(self, st: SegmentTree):
        self.model = Model(st)
        self.view = View()

    def receive_events(self, events):
        self.model.handle_input(events)
        
    def update_view(self):
        self.view.draw_tree(self.model.st.root)