import pygame as pg
import src.preload.algorithm.reingold_tilford as RT
from src.preload.business_objects.segment_tree import SegmentTree

class Model:
    def __init__(self, st: SegmentTree):
        self.st = st
        RT.calculate_node_position(self.st.root)
    
    def handle_input(self, events):
        pass