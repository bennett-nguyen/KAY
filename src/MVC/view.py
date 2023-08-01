import os
import json
import pygame as pg
import src.preload.system.ds as ds
import src.preload.system.constants as const
from pygame import gfxdraw
from src.preload.business_objects.node import Node
from src.preload.business_objects.theme import Theme


class View:
    def __init__(self):
        self.current_theme: Theme = None
        self.themes: dict[str: Theme] = {}
        self.available_themes: list[str] = []

        self.CC_FONT = pg.font.Font("./fonts/CascadiaCode.ttf", 27)
        self.CM_FONT = pg.font.Font("./fonts/cmunrm.ttf", 30)
        self.CC_ITALIC_FONT = pg.font.Font("./fonts/cmunti.ttf", 30)

        self.load_themes()
        self.set_theme("Dark Mode")
    
    def mouse_collide_node(self, node: Node) -> tuple[bool, Node]:
        mouse_pos = pg.mouse.get_pos()
        hit_box = pg.Rect((0, 0), (const.NODE_CIRCLE_RADIUS+25, const.NODE_CIRCLE_RADIUS+25))
        hit_box.center = node.coordinates

        if hit_box.collidepoint(mouse_pos):
            return (True, node)

        if node.is_leaf():
            return (False, node)

        for child in node.children:
            is_collided, queried_node = self.mouse_collide_node(child)
            if not is_collided:
                continue

            return (is_collided, queried_node)

        return (False, node)


    def view_array(self, array: list[int], collided_node: tuple[bool, Node]):
        x, y = (30, 30)
        theme = self.current_theme

        spacing = 50
        for (idx, element) in enumerate(array):
            is_collided, queried_node = collided_node
            data_color = theme.NODE_DISPLAY_DATA_CLR
            if is_collided and queried_node.low <= idx <= queried_node.high:
                data_color = theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR

            text = self.CM_FONT.render(f"{element}", True, data_color)
            ds.screen.blit(text, (x, y))
            x += spacing

    def draw_tree(self, node: Node, collided_node: tuple[bool, Node]):
        theme = self.current_theme
        is_collided, queried_node = collided_node

        node_outline_clr = theme.NODE_OUTLINE_CLR
        display_data_clr = theme.NODE_DISPLAY_DATA_CLR
        
        if is_collided and queried_node is node:
            node_outline_clr = theme.NODE_OUTLINE_HIGHLIGHT_CLR
            display_data_clr = theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR

        self._draw_lines(node)
        self._draw_circles(node, node_outline_clr)
        self._draw_node_data(node, display_data_clr)

        if node.is_leaf():
            return

        for child in node.children:
            self.draw_tree(child, collided_node)


    def _draw_circles(self, node: Node, outline_clr: pg.Color):
        theme = self.current_theme
        pg.draw.circle(ds.screen, theme.NODE_FILLINGS_CLR, node.coordinates, const.NODE_CIRCLE_RADIUS-const.LINE_THICKNESS)

        for depth in range(const.NODE_CIRCLE_RADIUS-const.LINE_THICKNESS, const.NODE_CIRCLE_RADIUS):
            gfxdraw.aacircle(ds.screen, *node.coordinates, depth, outline_clr)
            gfxdraw.aacircle(ds.screen, *node.coordinates, depth, outline_clr)


    def _draw_lines(self, node: Node):
        theme = self.current_theme

        if node.is_leaf():
            return

        pg.draw.line(
            ds.screen,
            theme.LINE_CLR,
            node.coordinates,
            node.left.coordinates,
            const.LINE_THICKNESS,
        )

        pg.draw.line(
            ds.screen,
            theme.LINE_CLR,
            node.coordinates,
            node.right.coordinates,
            const.LINE_THICKNESS,
        )


    def _draw_node_data(self, node: Node, display_data_clr: pg.Color):
        node_display_data = self.CC_FONT.render(f"{node.data}", True, display_data_clr)
        node_display_data_rect = node_display_data.get_rect(center=node.coordinates)
        ds.screen.blit(node_display_data, node_display_data_rect)


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
