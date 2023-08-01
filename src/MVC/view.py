import os
import json
import pygame as pg
import src.preload.system.ds as ds
import src.preload.system.constants as const
from src.preload.business_objects.node import Node
from src.preload.business_objects.theme import Theme


class View:
    def __init__(self):
        self.current_theme: Theme = None
        self.themes: dict[str: Theme] = {}
        self.available_themes: list[str] = []

        self.load_themes()
        self.set_theme("Dark Mode")

    def draw_tree(self, node: Node):
        theme = self.current_theme

        if not node.is_leaf():
            pg.draw.line(ds.screen, theme.LINE_CLR, node.coordinates, node.left.coordinates, const.LINE_THICKNESS)
            pg.draw.line(ds.screen, theme.LINE_CLR, node.coordinates, node.right.coordinates, const.LINE_THICKNESS)

        pg.draw.circle(ds.screen, theme.NODE_OUTLINE_CLR, node.coordinates, const.NODE_CIRCLE_RADIUS)
        pg.draw.circle(ds.screen, theme.NODE_FILLINGS_CLR, node.coordinates, const.NODE_CIRCLE_RADIUS-const.LINE_THICKNESS)

        if node.is_leaf():
            return

        for child in node.children:
            self.draw_tree(child)

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
