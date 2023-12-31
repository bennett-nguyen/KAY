from typing import List, Tuple, Dict

import pygame as pg
from pygame import gfxdraw

import src.preload.system.ds as ds
import src.preload.system.constants as const
from src.preload.business_objects.node import Node
from src.preload.business_objects.theme import Theme
from src.preload.business_objects.app_ui import AppUI
from src.preload.system.app_type import VisibilityField



class View:
    def __init__(self):
        self.current_theme: Theme
        self.visibility_dict: Dict[VisibilityField, bool]

        self.CC_FONT = pg.font.Font("./fonts/CascadiaCode/CascadiaCode-Regular.ttf", 27)
        self.CM_FONT = pg.font.Font("./fonts/CM/cmunrm.ttf", 50)
        self.CM_ITALIC_FONT = pg.font.Font("./fonts/CM/cmunti.ttf", 50)

    def request_theme(self, theme: Theme):
        self.current_theme = theme

    def request_visibility(self, visibility_dict: Dict[VisibilityField, bool]):
        self.visibility_dict = visibility_dict

    def render_text(self, font: pg.font.Font, text: str, color: pg.Color) -> Tuple[pg.Surface, pg.Rect]:
        surf = font.render(text, True, color)
        rect = surf.get_rect()

        return (surf, rect)

    def mouse_hover_node(self, node: Node) -> Tuple[bool, Node]:
        mouse_pos = pg.mouse.get_pos()
        hit_box = pg.Rect((0, 0), (const.NODE_CIRCLE_RADIUS+25, const.NODE_CIRCLE_RADIUS+25))
        hit_box.center = node.coordinates

        if hit_box.collidepoint(mouse_pos):
            return (True, node)

        if node.is_leaf():
            return (False, node)

        for child in node.children:
            is_hovered, queried_node = self.mouse_hover_node(child)
            if not is_hovered:
                continue

            return (is_hovered, queried_node)

        return (False, node)

    def view_app_ui(self, app_ui: AppUI):
        if self.visibility_dict[const.DISPLAY_BOTTOM_BAR]:
            app_ui.theme_selection_ui.UI.show()
            app_ui.cmd_textbox_ui.UI.show()
        else:
            app_ui.theme_selection_ui.UI.hide()
            app_ui.cmd_textbox_ui.UI.hide()
            app_ui.message_box_ui.UI.hide()

        app_ui.gui_manager.draw_ui(ds.screen)

    def view_hovered_node_info(self, hovered_node: Tuple[bool, Node]):
        if not self.visibility_dict[const.VIEW_NODE_INFO_FIELD]:
            return

        is_hovered, queried_node = hovered_node

        if not is_hovered:
            return

        x, y = (const.WIDTH - const.X_OFFSET, const.Y_OFFSET)
        segment_rect_bounding_box_bottom = self._view_segment(x, y, queried_node)

        y = segment_rect_bounding_box_bottom + const.LINE_SPACING
        self._view_ID(x, y, queried_node)

    def view_array(self, array: List[int], hovered_node: Tuple[bool, Node]):
        if not self.visibility_dict[const.VIEW_ARRAY_FIELD]:
            return

        x, y = (const.X_OFFSET, const.Y_OFFSET)
        theme = self.current_theme

        for (idx, element) in enumerate(array):
            is_hovered, queried_node = hovered_node
            data_color = theme.NODE_DISPLAY_DATA_CLR
            if is_hovered and queried_node.low <= idx <= queried_node.high:
                data_color = theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR

            text, rect = self.render_text(self.CM_FONT, f"{element}", data_color)
            rect.topleft = (x, y)

            ds.screen.blit(text, rect)
            x = rect.right + const.ELEMENT_SPACING

            if x >= const.MAX_X_PER_LINE:
                x = const.X_OFFSET
                y = rect.bottom + const.LINE_SPACING

    def draw_tree(self, node: Node, hovered_node: Tuple[bool, Node]):
        theme = self.current_theme
        is_hovered, queried_node = hovered_node

        node_outline_clr = theme.NODE_OUTLINE_CLR
        display_data_clr = theme.NODE_DISPLAY_DATA_CLR

        if is_hovered and queried_node is node:
            node_outline_clr = theme.NODE_OUTLINE_HIGHLIGHT_CLR
            display_data_clr = theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR

        self._draw_lines(node)
        self._draw_circles(node, node_outline_clr)

        if self.visibility_dict[const.VIEW_NODE_DATA_FIELD]:
            self._draw_node_data(node, display_data_clr)

        if node.is_leaf():
            return

        for child in node.children:
            self.draw_tree(child, hovered_node)

    def _view_segment(self, x: int, y: int, hovered_node: Node) -> int:
        theme = self.current_theme

        data_clr = theme.NODE_DISPLAY_DATA_CLR
        highlight_data_clr = theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR

        text_to_render: List[str] = ["[", f"{hovered_node.low}", "; ", f"{hovered_node.high}", "]"]
        font_for_text: List[pg.font.Font] = [self.CM_FONT, self.CM_FONT, self.CM_FONT, self.CM_FONT, self.CM_FONT]
        color_for_text: List[pg.Color] = [data_clr, highlight_data_clr, data_clr, highlight_data_clr, data_clr]

        text_surf_and_rect: List[Tuple[pg.Surface, pg.Rect]] = []

        for font, text, color in zip(font_for_text, text_to_render, color_for_text):
            text_surf_and_rect.insert(0, self.render_text(font, text, color))

        for idx in range(len(text_surf_and_rect)):
            if idx == 0:
                text_surf_and_rect[0][1].topright = (x, y)
                continue

            text_surf_and_rect[idx][1].midright = text_surf_and_rect[idx-1][1].midleft

        for surf, rect in text_surf_and_rect:
            ds.screen.blit(surf, rect)

        return text_surf_and_rect[0][1].bottom

    def _view_ID(self, x: int, y: int, hovered_node: Node):
        theme = self.current_theme

        ID_text, ID_rect = self.render_text(self.CM_FONT, "ID: ", theme.NODE_DISPLAY_DATA_CLR)
        ID_dat_text, ID_dat_rect = self.render_text(self.CM_FONT, f"{hovered_node.ID}", theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR)

        ID_dat_rect.topright = (x, y)
        ID_rect.midright = ID_dat_rect.midleft

        ds.screen.blit(ID_text, ID_rect)
        ds.screen.blit(ID_dat_text, ID_dat_rect)

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
        node_display_data, node_display_data_rect = self.render_text(self.CC_FONT, f"{node.data}", display_data_clr)
        node_display_data_rect.center = node.coordinates
        ds.screen.blit(node_display_data, node_display_data_rect)
