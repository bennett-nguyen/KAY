import os
import json
import pygame as pg
import src.preload.system.constants as const
import src.preload.algorithm.reingold_tilford as RT
from src.preload.business_objects.theme import Theme
from src.preload.business_objects.segment_tree import SegmentTree


class Model:
    def __init__(self, st: SegmentTree):
        self.st = st

        self.current_theme: Theme = None
        self.themes: dict[str: Theme] = {}
        self.available_themes: list[str] = []

        self.load_themes()
        self.set_theme("Dark Mode")

        self.prev_mouse_pos = (0, 0)
        self.curr_mouse_pos = (0, 0)

        RT.calculate_node_position(self.st.root)

        # center the root node by the width of the screen
        delta_x = const.HALF_WIDTH - self.st.root.x
        RT.move_node_by_delta_pos(self.st.root, delta_x, 0)


    def handle_input(self, events):
        self.pan()


    def pan(self):
        mouse_pressed = pg.mouse.get_pressed()

        if not mouse_pressed[0]:
            self.prev_mouse_pos = (0, 0)
            return

        self.curr_mouse_pos = pg.mouse.get_pos()

        if self.prev_mouse_pos == (0, 0):
            self.prev_mouse_pos = self.curr_mouse_pos

        delta_x = self.curr_mouse_pos[0] - self.prev_mouse_pos[0]
        delta_y = self.curr_mouse_pos[1] - self.prev_mouse_pos[1]

        RT.move_node_by_delta_pos(self.st.root, delta_x, delta_y)
        self.prev_mouse_pos = self.curr_mouse_pos


    def load_themes(self):
        for entry in os.listdir("./theme"):
            if not entry.endswith(".json"):
                continue

            with open(f"./theme/{entry}", "r") as f:
                json_obj = json.load(f)
                self.themes[json_obj["Name"]] = Theme(json_obj["Palette"])
                self.available_themes.append(json_obj["Name"])


    def set_theme(self, name: str):
        try:
            self.current_theme = self.themes[name]
        except KeyError:
            print(f"Error: Theme <{name}> not found.")
            pg.quit()
            exit(1)
