import pygame as pg
import preload.ds as ds
import preload.constants as const
from preload.segment_tree import Node

_LEFT = "left"
_RIGHT = "right"

# side: "left" || "right"

class Visualizer:
    def __init__(self, host, tree: Node):
        self.host = host

        self.view_scale = 1
        self.SCALE = 200
        self.PRELIM_X_OFFSET = 1
        self.DEPTH_OFFSET = 1
        self.VERTICAL_SCALE = 100
        
        self.LINE_THICKNESS = 4
        self.NODE_CIRCLE_RADIUS = 20

        self._calculate_node_position(tree)


    def draw(self, node: Node):
        if not node.is_leaf():
            pg.draw.line(ds.screen, "Black", node.coordinates, node.left.coordinates, self.LINE_THICKNESS)
            pg.draw.line(ds.screen, "Black", node.coordinates, node.right.coordinates, self.LINE_THICKNESS)
        
        pg.draw.circle(ds.screen, "Black", node.coordinates, self.NODE_CIRCLE_RADIUS)
        pg.draw.circle(ds.screen, "White", node.coordinates, self.NODE_CIRCLE_RADIUS-self.LINE_THICKNESS)

        if node.is_leaf():
            return

        for child in node.children:
            self.draw(child)


    def _calculate_node_position(self, root: Node):
        self._compute_prelim_x(root)
        self._compute_final_coordinates(root, 0)


    def _compute_prelim_x(self, node: Node):
        if node.is_leaf():
            if node.is_left_node():
                node._preliminary_x = 0
            else:
                node._preliminary_x = node.previous_sibling._preliminary_x \
                                    + const.SIBLING_DISTANCE + const.NODE_SIZE 
            
            return

        for child in node.children:
            self._compute_prelim_x(child)

        left_child = node.left
        right_child = node.right

        mid = float((left_child._preliminary_x + right_child._preliminary_x) / 2)

        if node.is_left_node():
            node._preliminary_x = mid
        else:
            node._preliminary_x = node.parent.left._preliminary_x \
                                + const.SIBLING_DISTANCE + const.NODE_SIZE 
            node._modifier = node._preliminary_x - mid

        if not node.is_left_node():
            self._check_for_conflicts(node)


    def _compute_final_coordinates(self, node: Node, mod_sum: float):
        node._preliminary_x += mod_sum + self.PRELIM_X_OFFSET
        mod_sum += node._modifier

        if not node.is_leaf():
            for child in node.children:
                self._compute_final_coordinates(child, mod_sum)

        node.x = node._preliminary_x * self.SCALE
        node.y = (node.depth + self.DEPTH_OFFSET) * self.VERTICAL_SCALE


    def _check_for_conflicts(self, node: Node):
        min_distance: float = const.TREE_DISTANCE + const.NODE_SIZE
        shift_value: float = 0.0

        node_contour: dict[int, float] = {}
        self._get_contour(node, 0, node_contour, _LEFT)

        sibling = node.previous_sibling
        sibling_contour: dict[int, float] = {}
        self._get_contour(sibling, 0, sibling_contour, _RIGHT)

        for level in range(
            node.depth+1, 
            min(
                max(node_contour.keys()),
                max(sibling_contour.keys())
            )+1
        ):
            distance = node_contour[level] - sibling_contour[level]
            if distance + shift_value < min_distance:
                shift_value = max(min_distance - distance, shift_value)

        if shift_value > 0:
            node._preliminary_x += shift_value
            node._modifier += shift_value

    def _get_contour(self, node: Node, mod_sum: float, values: dict[int, float], side: str):
        side = side.lower()

        if side not in [_LEFT, _RIGHT]:
            raise ValueError("'side' only accepts either 2 values: 'left' or 'right'.")

        _fn = min if side == _LEFT else max

        if node.depth not in values:
            values[node.depth] = node._preliminary_x + mod_sum
        else:
            values[node.depth] = _fn(values[node.depth], node._preliminary_x + mod_sum)

        mod_sum += node._modifier

        if node.is_leaf():
            return

        for child in node.children:
            self._get_contour(child, mod_sum, values, side)
