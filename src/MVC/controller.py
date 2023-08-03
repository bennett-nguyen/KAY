import pygame as pg
from src.MVC.view import View
from src.MVC.model import Model
from src.preload.business_objects.segment_tree import SegmentTree
from src.preload.business_objects.node import Node

class Controller:
    def __init__(self, st: SegmentTree):
        self.model = Model(st)
        self.view = View()

    def receive_events(self, events):
        self.model.handle_input(events)

    def update_view(self):
        # hovered_node[0]: is the mouse hovering on the queried node
        # hovered_node[1]: return the queried node's ID if mouse is hovering on that node
        hovered_node: tuple[bool, Node] = self.view.mouse_hover_node(self.model.st.root) 
        self.view.draw_tree(self.model.st.root, hovered_node)
        self.view.view_array(self.model.st.arr, hovered_node)
        self.view.view_hovered_node_info(hovered_node)