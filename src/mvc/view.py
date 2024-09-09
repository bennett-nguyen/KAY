from typing import Optional
from collections import deque

import pygame as pg
from pygame import gfxdraw

from src.core import pygame_window
from src.core.utils import VisibilityEnum, const
from src.core.tree_utils import Node
from src.core.dataclasses import Theme

class View:
    """
    Handles the rendering and display of the application's user interface. This
    class manages themes, visibility settings, and the graphical representation
    of the segment tree, allowing for dynamic updates and visual feedback based
    on user interactions.
    """

    def __init__(self):
        self.current_theme: Theme
        self.visibility_dict: dict[VisibilityEnum, bool]
        self.node_data_font = pg.font.Font("./fonts/JetBrainsMonoNL-Regular.ttf", 27)
        self.tree_properties_font = pg.font.Font("./fonts/JetBrainsMonoNL-Regular.ttf", 40)

    def request_theme(self, theme: Theme):
        """
        Requests to change the current theme of the view. This method updates the
        view's theme to the specified theme, allowing for dynamic visual changes
        in the user interface.

        Args:
            theme (Theme): The new theme to be applied to the view.
        """

        self.current_theme = theme

    def request_visibility(self, visibility_dict: dict[VisibilityEnum, bool]):
        """
        Requests to update the visibility settings of the view. This method sets the
        visibility of various UI elements based on the provided dictionary, allowing
        for dynamic control over what is displayed in the user interface.

        Args:
            visibility_dict (dict[VisibilityEnum, bool]): A dictionary that maps visibility
            fields to their corresponding visibility states.
        """

        self.visibility_dict = visibility_dict

    def render_text(self, font: pg.font.Font, text: str, color: pg.Color) -> tuple[pg.Surface, pg.Rect]:
        """
        Renders text using the specified font and color, returning the rendered surface
        and its rectangle. This method creates a graphical representation of the text
        that can be displayed on the screen.

        Args:
            font (pg.font.Font): The font to be used for rendering the text.
            text (str): The text string to be rendered.
            color (pg.Color): The color of the text.

        Returns:
            tuple[pg.Surface, pg.Rect]: A tuple containing the rendered text surface
            and its bounding rectangle.
        """
        
        surf = font.render(text, True, color)
        rect = surf.get_rect()

        return (surf, rect)

    def view_hovered_node_info(self, hovered_node: Optional[Node]):
        """
        Displays information about the currently hovered node if visibility settings
        allow it. This method checks the visibility of the node information field and,
        if visible, renders the relevant details of the hovered node on the screen.

        Args:
            hovered_node (Optional[Node]): The node currently being hovered over, or
            None if no node is hovered.
        """

        if not self.visibility_dict[VisibilityEnum.NODE_INFO_FIELD] \
                or hovered_node is None:
            return

        x, y = (pygame_window.window_width - const.X_OFFSET, const.Y_OFFSET)
        segment_rect_bounding_box_bottom = self._view_segment(x, y, hovered_node)

        y = segment_rect_bounding_box_bottom + const.LINE_SPACING
        self._view_ID(x, y, hovered_node)

    def view_array(self, array: list[int], hovered_node: Optional[Node]):
        """
        Renders the elements of the segment tree's array in the user interface. This 
        method checks the visibility settings and displays each element with appropriate
        colors, highlighting the any element that is within the hovered node's boundary
        if applicable.

        Args:
            array (list[int]): The list of integers to be displayed.
            hovered_node (Optional[Node]): The node currently being hovered over, which
            may affect the display color of the elements.
        """

        if not self.visibility_dict[VisibilityEnum.ARRAY_FIELD]:
            return

        x, y = (const.X_OFFSET, const.Y_OFFSET)
        theme = self.current_theme

        for (idx, element) in enumerate(array):
            data_color = theme.NODE_DISPLAY_DATA_CLR
            if hovered_node is not None and hovered_node.low <= idx <= hovered_node.high:
                data_color = theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR

            text, rect = self.render_text(self.tree_properties_font, f"{element}", data_color)
            rect.topleft = (x, y)

            pygame_window.screen.blit(text, rect)
            x = rect.right + const.ELEMENT_SPACING

            if x >= const.MAX_X_PER_LINE:
                x = const.X_OFFSET
                y = rect.bottom + const.LINE_SPACING

    def draw_tree(self, root: Node) -> Optional[Node]:
        """
        Draws the tree structure starting from the specified root node. This method
        visually represents the nodes and their connections, highlighting the hovered
        node and displaying data if visibility settings allow it. Returns the hovered
        node it found during the drawing process.

        Args:
            root (Node): The root node of the tree to be drawn.

        Returns:
            Optional[Node]: The node that is currently hovered over, or None if no node is hovered.
        """

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

            if self.visibility_dict[VisibilityEnum.NODE_DATA_FIELD]:
                self._draw_node_data(node, display_data_clr)

            if node.is_leaf():
                continue

            for child in node.children:
                queue.append(child)

        return hovered_node

    def _view_segment(self, x: int, y: int, hovered_node: Node) -> int:
        """
        Displays the segment information for the hovered node. This method renders
        the low and high values of the hovered node in a formatted manner, using
        appropriate colors and fonts based on the current theme.

        Args:
            x (int): The x-coordinate for positioning the segment display.
            y (int): The y-coordinate for positioning the segment display.
            hovered_node (Node): The node currently being hovered over, whose segment
            information will be displayed.

        Returns:
            int: The bottom coordinate of the rendered segment display.
        """

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
            pygame_window.screen.blit(surf, rect)

        return text_surf_and_rect[0][1].bottom

    def _view_ID(self, x: int, y: int, hovered_node: Node):
        """
        Displays the ID of the currently hovered node in the user interface. This method
        renders the ID label and its corresponding value, positioning them according to
        the specified coordinates and applying the current theme's colors.

        Args:
            x (int): The x-coordinate for positioning the ID display.
            y (int): The y-coordinate for positioning the ID display.
            hovered_node (Node): The node currently being hovered over, whose ID will be displayed.
        """

        theme = self.current_theme

        ID_text, ID_rect = self.render_text(self.tree_properties_font, "ID: ", theme.NODE_DISPLAY_DATA_CLR)
        ID_dat_text, ID_dat_rect = self.render_text(self.tree_properties_font, f"{hovered_node.ID}", theme.NODE_DISPLAY_DATA_HIGHLIGHT_CLR)

        ID_dat_rect.topright = (x, y)
        ID_rect.midright = ID_dat_rect.midleft

        pygame_window.screen.blit(ID_text, ID_rect)
        pygame_window.screen.blit(ID_dat_text, ID_dat_rect)

    def _draw_circles(self, node: Node, outline_clr: pg.Color):
        """
        Draws filled and outlined circles representing a specified node in the user 
        interface. This method uses the current theme's colors to render the circles,
        visually representing the node's position and enhancing its appearance.

        Args:
            node (Node): The node for which the circles are to be drawn.
            outline_clr (pg.Color): The color used for the outline of the circles.
        """

        theme = self.current_theme
        pg.draw.circle(pygame_window.screen, theme.NODE_FILLINGS_CLR, node.coordinates, const.NODE_CIRCLE_RADIUS-const.LINE_THICKNESS)

        for depth in range(const.NODE_CIRCLE_RADIUS-const.LINE_THICKNESS, const.NODE_CIRCLE_RADIUS):
            gfxdraw.aacircle(pygame_window.screen, *node.coordinates, depth, outline_clr)
            gfxdraw.aacircle(pygame_window.screen, *node.coordinates, depth, outline_clr)

    def _draw_lines(self, node: Node):
        """
        Draws lines connecting the specified node to its children in the user interface.
        This method visually represents the relationships between nodes in the tree 
        structure, enhancing the overall clarity of the tree's layout.

        Args:
            node (Node): The node for which the connecting lines to its children will be drawn.
        """

        theme = self.current_theme

        if node.is_leaf():
            return

        pg.draw.line(
            pygame_window.screen,
            theme.LINE_CLR,
            node.coordinates,
            node.left.coordinates,
            const.LINE_THICKNESS,
        )

        pg.draw.line(
            pygame_window.screen,
            theme.LINE_CLR,
            node.coordinates,
            node.right.coordinates,
            const.LINE_THICKNESS,
        )

    def _draw_node_data(self, node: Node, display_data_clr: pg.Color):
        """
        Displays the data value of the specified node in the user interface. This method
        renders the node's data at the node's coordinates using the specified color, 
        ensuring that the information is visually accessible.

        Args:
            node (Node): The node whose data value will be displayed.
            display_data_clr (pg.Color): The color used for rendering the node's data.
        """

        node_display_data, node_display_data_rect = self.render_text(self.node_data_font, f"{node.data}", display_data_clr)
        node_display_data_rect.center = node.coordinates
        pygame_window.screen.blit(node_display_data, node_display_data_rect)