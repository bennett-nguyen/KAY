from typing import Optional, Any
from collections import deque
from math import atan2, cos, degrees, radians, sin

import pygame as pg
from pygame import gfxdraw

from src.window import pygame_window
from src.utils import VisibilityEnum, CommandRequestFields, const
from src.dataclass import Theme, Node

class Rendering:
    """
    Handles the rendering of the user interface for the application.

    This class manages the visual representation of various UI elements,
    including themes, visibility settings, and node information. It provides
    methods to render text, draw tree structures, and display node data
    dynamically based on user interactions.
    """

    def __init__(self):
        self.current_theme: Theme
        self.visibility_dict: dict[VisibilityEnum, bool]
        self.node_data_font = pg.font.Font("./fonts/JetBrainsMonoNL-Regular.ttf", 27)
        self.tree_properties_font = pg.font.Font("./fonts/JetBrainsMonoNL-Regular.ttf", 40)

        
        self.visibility_dict: dict[VisibilityEnum, bool] = {
            VisibilityEnum.ARRAY_FIELD: True,
            VisibilityEnum.NODE_DATA_FIELD: True,
            VisibilityEnum.NODE_INFO_FIELD: True
        }

        self.command_request_data: dict[CommandRequestFields, Any] = {
            CommandRequestFields.HIGHLIGHT_RANGE_LOW: -1,
            CommandRequestFields.HIGHLIGHT_RANGE_HIGH: -1,
        }

    def request_theme(self, theme: Theme):
        """
        Requests to change the current theme of the view. This method updates the
        view's theme to the specified theme, allowing for dynamic visual changes
        in the user interface.

        Args:
            theme (Theme): The new theme to be applied to the view.
        """

        self.current_theme = theme

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
        """Draws the tree structure starting from the specified root node.

        This method visually represents the nodes and their connections,
        highlighting the hovered node and displaying data if visibility settings
        allow it. It traverses the tree and renders each node, returning the
        currently hovered node if applicable.
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
            elif self.should_highlight_range(node):
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

    def should_highlight_range(self, node: Node):
        """Determines if the specified node falls within the highlight range.

        This method checks if the node's range is within the current command
        request's highlight boundaries (from highlight-range). It returns a boolean
        indicating whether the node should be highlighted based on the defined low
        and high values.
        """

        c_low = self.command_request_data[CommandRequestFields.HIGHLIGHT_RANGE_LOW]
        c_high = self.command_request_data[CommandRequestFields.HIGHLIGHT_RANGE_HIGH]

        return c_low <= node.low and node.high <= c_high

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

        for depth in range(const.NODE_CIRCLE_RADIUS-const.CIRCLE_OUTLINE_THICKNESS, const.NODE_CIRCLE_RADIUS):
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

        self._draw_antialiased_thick_line(
            node.coordinates,
            node.left.coordinates,
            theme.LINE_CLR,
            const.LINE_THICKNESS
        )
        
        self._draw_antialiased_thick_line(
            node.coordinates,
            node.right.coordinates,
            theme.LINE_CLR,
            const.LINE_THICKNESS
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

    def _draw_antialiased_thick_line(self, point_start: tuple[int, int], point_end: tuple[int, int], line_color: pg.Color, line_thickness: float):
        """
        Draw an antialiased polygon that resembles a line.

        The idea behind this algorithm can be found here: https://stackoverflow.com/a/30599392
        This function implements the more readable solution that's also in the same post: https://stackoverflow.com/a/67509308

        Summary:
        - Define the center point of the polygon from the starting point and ending point of the line.
        - Find the slope of the line.
        - Using the slope and the shape parameters to calculate the coordinates of the box ends.
        - Draw a polygon using those coordinates and finally fill it.

        Args:
            point_start (tuple[int, int]): The starting point of the line
            point_end (tuple[int, int]): The ending point of the line
            line_color (pg.Color): The color of the line
            line_thickness (float): The thickness of the line
        """

        slope = degrees(atan2(point_start[1] - point_end[1], point_start[0] - point_end[0]))

        vertices = [
            self._move(slope-90, line_thickness, point_start),
            self._move(slope+90, line_thickness, point_start),
            self._move(slope+90, line_thickness, point_end),
            self._move(slope-90, line_thickness, point_end)
        ]

        gfxdraw.aapolygon(pygame_window.screen, vertices, line_color)
        gfxdraw.filled_polygon(pygame_window.screen, vertices, line_color)

    def _move(self, rotation: float, steps: int, position: tuple[int, int]) -> tuple[float, float]:
        xPosition = cos(radians(rotation)) * steps + position[0]
        yPosition = sin(radians(rotation)) * steps + position[1]
        return (xPosition, yPosition)
