import pygame as pg
import src.preload.system.ds as ds
import src.preload.system.constants as const
from pygame import gfxdraw
from src.preload.business_objects.node import Node
from src.preload.business_objects.theme import Theme


class View:
    def __init__(self):
        self.current_theme: Theme = None

        self.CC_FONT = pg.font.Font("./fonts/CascadiaCode.ttf", 27)
        self.CM_FONT = pg.font.Font("./fonts/cmunrm.ttf", 50)
        self.CM_ITALIC_FONT = pg.font.Font("./fonts/cmunti.ttf", 50)


    def request_theme(self, theme: Theme):
        self.current_theme = theme


    def render_text(self, font: pg.font.Font, text: str, color: pg.Color) -> tuple[pg.Surface, pg.Rect]:
        surf = font.render(text, True, color)
        rect = surf.get_rect()

        return (surf, rect)


    def mouse_hover_node(self, node: Node) -> tuple[bool, Node]:
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


    def view_hovered_node_info(self, hovered_node: tuple[bool, Node]):
        theme = self.current_theme
        is_hovered, queried_node = hovered_node
        
        if not is_hovered:
            return

        x, y = (const.WIDTH - const.X_OFFSET, const.Y_OFFSET)
        l_text, l_rect = self.render_text(self.CM_ITALIC_FONT, f"{queried_node.low}", theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR)
        h_text, h_rect = self.render_text(self.CM_ITALIC_FONT, f"{queried_node.high}", theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR)

        lh_sec_1, lh_rect_1 = self.render_text(self.CM_FONT, "[", theme.NODE_DISPLAY_DATA_CLR)
        lh_sec_2, lh_rect_2 = self.render_text(self.CM_FONT, "; ", theme.NODE_DISPLAY_DATA_CLR)
        lh_sec_3, lh_rect_3 = self.render_text(self.CM_FONT, "]", theme.NODE_DISPLAY_DATA_CLR)

        lh_rect_3.topright = (x, y)
        h_rect.midright = lh_rect_3.midleft
        lh_rect_2.midright = h_rect.midleft
        l_rect.midright = lh_rect_2.midleft
        lh_rect_1.midright = l_rect.midleft

        y = lh_rect_1.bottom + const.LINE_SPACING
        ID_text, ID_rect = self.render_text(self.CM_ITALIC_FONT, "ID: ", theme.NODE_DISPLAY_DATA_CLR)
        ID_dat_text, ID_dat_rect = self.render_text(self.CM_ITALIC_FONT, f"{queried_node.ID}", theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR)

        ID_dat_rect.topright = (x, y)
        ID_rect.midright = ID_dat_rect.midleft

        ds.screen.blit(lh_sec_1, lh_rect_1)
        ds.screen.blit(lh_sec_2, lh_rect_2)
        ds.screen.blit(lh_sec_3, lh_rect_3)
        ds.screen.blit(l_text, l_rect)
        ds.screen.blit(h_text, h_rect)

        ds.screen.blit(ID_text, ID_rect)
        ds.screen.blit(ID_dat_text, ID_dat_rect)


    def view_array(self, array: list[int], hovered_node: tuple[bool, Node]):
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


    def draw_tree(self, node: Node, hovered_node: tuple[bool, Node]):
        theme = self.current_theme
        is_hovered, queried_node = hovered_node

        node_outline_clr = theme.NODE_OUTLINE_CLR
        display_data_clr = theme.NODE_DISPLAY_DATA_CLR
        
        if is_hovered and queried_node is node:
            node_outline_clr = theme.NODE_OUTLINE_HIGHLIGHT_CLR
            display_data_clr = theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR

        self._draw_lines(node)
        self._draw_circles(node, node_outline_clr)
        self._draw_node_data(node, display_data_clr)

        if node.is_leaf():
            return

        for child in node.children:
            self.draw_tree(child, hovered_node)


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
