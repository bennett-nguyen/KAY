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
        # collided_node[0]: does mouse collide with queried node
        # collided_node[1]: return the queried node's ID is mouse does collide with that node
        collided_node: tuple[bool, int] = self.view.mouse_collide_node(self.model.st.root) 
        self.view.draw_tree(self.model.st.root, collided_node)
        self.view.view_array(self.model.st.arr, collided_node)