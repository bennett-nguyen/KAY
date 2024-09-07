from typing import Optional
from collections import deque

import pygame as pg
from pygame import gfxdraw

import src.preload.system.window as window
import src.preload.system.constants as const
from src.preload.tree.node import Node
from src.preload.ui.theme import Theme
from src.preload.system.app_enum import Visibility


class View:
    def __init__(self):
        self.current_theme: Theme
        self.visibility_dict: dict[Visibility, bool]
        self.node_data_font = pg.font.Font("./fonts/JetBrainsMono-Medium.ttf", 27)
        self.tree_properties_font = pg.font.Font("./fonts/JetBrainsMono-Medium.ttf", 40)

    def request_theme(self, theme: Theme):
        self.current_theme = theme

    def request_visibility(self, visibility_dict: dict[Visibility, bool]):
        self.visibility_dict = visibility_dict

    def render_text(self, font: pg.font.Font, text: str, color: pg.Color) -> tuple[pg.Surface, pg.Rect]:
        surf = font.render(text, True, color)
        rect = surf.get_rect()

        return (surf, rect)

    def view_hovered_node_info(self, hovered_node: Optional[Node]):
        if not self.visibility_dict[Visibility.NODE_INFO_FIELD]:
            return

        if hovered_node is None:
            return

        x, y = (const.WIDTH - const.X_OFFSET, const.Y_OFFSET)
        segment_rect_bounding_box_bottom = self._view_segment(x, y, hovered_node)

        y = segment_rect_bounding_box_bottom + const.LINE_SPACING
        self._view_ID(x, y, hovered_node)

    def view_array(self, array: list[int], hovered_node: Optional[Node]):
        if not self.visibility_dict[Visibility.ARRAY_FIELD]:
            return

        x, y = (const.X_OFFSET, const.Y_OFFSET)
        theme = self.current_theme

        for (idx, element) in enumerate(array):
            data_color = theme.NODE_DISPLAY_DATA_CLR
            if hovered_node is not None and hovered_node.low <= idx <= hovered_node.high:
                data_color = theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR

            text, rect = self.render_text(self.tree_properties_font, f"{element}", data_color)
            rect.topleft = (x, y)

            window.screen.blit(text, rect)
            x = rect.right + const.ELEMENT_SPACING

            if x >= const.MAX_X_PER_LINE:
                x = const.X_OFFSET
                y = rect.bottom + const.LINE_SPACING

    def draw_tree(self, root: Node):
        theme = self.current_theme
        node_outline_clr = theme.NODE_OUTLINE_CLR
        display_data_clr = theme.NODE_DISPLAY_DATA_CLR

        hovered_node = None

        mouse_pos = pg.mouse.get_pos()
        hit_box = pg.Rect((0, 0), (const.NODE_CIRCLE_RADIUS+25, const.NODE_CIRCLE_RADIUS+25))

        queue: deque[Node] = deque([root])

        while queue:
            node = queue.popleft()
            hit_box.center = node.coordinates

            if hit_box.collidepoint(mouse_pos):
                hovered_node = node
                node_outline_clr = theme.NODE_OUTLINE_HIGHLIGHT_CLR
                display_data_clr = theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR
            else:
                node_outline_clr = theme.NODE_OUTLINE_CLR
                display_data_clr = theme.NODE_DISPLAY_DATA_CLR

            self._draw_lines(node)
            self._draw_circles(node, node_outline_clr)

            if self.visibility_dict[Visibility.NODE_DATA_FIELD]:
                self._draw_node_data(node, display_data_clr)

            if node.is_leaf():
                continue

            for child in node.children:
                queue.append(child)

        return hovered_node

    def _view_segment(self, x: int, y: int, hovered_node: Node) -> int:
        theme = self.current_theme

        data_clr = theme.NODE_DISPLAY_DATA_CLR
        highlight_data_clr = theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR

        text_to_render: list[str] = ["[", f"{hovered_node.low}", "; ", f"{hovered_node.high}", "]"]
        font_for_each_text: list[pg.font.Font] = [self.tree_properties_font, self.tree_properties_font, self.tree_properties_font, self.tree_properties_font, self.tree_properties_font]
        color_for_each_text: list[pg.Color] = [data_clr, highlight_data_clr, data_clr, highlight_data_clr, data_clr]

        text_surf_and_rect: list[tuple[pg.Surface, pg.Rect]] = []

        for font, text, color in zip(font_for_each_text, text_to_render, color_for_each_text):
            text_surf_and_rect.insert(0, self.render_text(font, text, color))

        for idx in range(len(text_surf_and_rect)):
            if idx == 0:
                text_surf_and_rect[0][1].topright = (x, y)
                continue

            text_surf_and_rect[idx][1].midright = text_surf_and_rect[idx-1][1].midleft

        for surf, rect in text_surf_and_rect:
            window.screen.blit(surf, rect)

        return text_surf_and_rect[0][1].bottom

    def _view_ID(self, x: int, y: int, hovered_node: Node):
        theme = self.current_theme

        ID_text, ID_rect = self.render_text(self.tree_properties_font, "ID: ", theme.NODE_DISPLAY_DATA_CLR)
        ID_dat_text, ID_dat_rect = self.render_text(self.tree_properties_font, f"{hovered_node.ID}", theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR)

        ID_dat_rect.topright = (x, y)
        ID_rect.midright = ID_dat_rect.midleft

        window.screen.blit(ID_text, ID_rect)
        window.screen.blit(ID_dat_text, ID_dat_rect)

    def _draw_circles(self, node: Node, outline_clr: pg.Color):
        theme = self.current_theme
        pg.draw.circle(window.screen, theme.NODE_FILLINGS_CLR, node.coordinates, const.NODE_CIRCLE_RADIUS-const.LINE_THICKNESS)

        for depth in range(const.NODE_CIRCLE_RADIUS-const.LINE_THICKNESS, const.NODE_CIRCLE_RADIUS):
            gfxdraw.aacircle(window.screen, *node.coordinates, depth, outline_clr)
            gfxdraw.aacircle(window.screen, *node.coordinates, depth, outline_clr)

    def _draw_lines(self, node: Node):
        theme = self.current_theme

        if node.is_leaf():
            return

        pg.draw.line(
            window.screen,
            theme.LINE_CLR,
            node.coordinates,
            node.left.coordinates,
            const.LINE_THICKNESS,
        )

        pg.draw.line(
            window.screen,
            theme.LINE_CLR,
            node.coordinates,
            node.right.coordinates,
            const.LINE_THICKNESS,
        )

    def _draw_node_data(self, node: Node, display_data_clr: pg.Color):
        node_display_data, node_display_data_rect = self.render_text(self.node_data_font, f"{node.data}", display_data_clr)
        node_display_data_rect.center = node.coordinates
        window.screen.blit(node_display_data, node_display_data_rect)
