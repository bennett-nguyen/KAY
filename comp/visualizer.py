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
        self.DEPTH_OFFSET = 1
        self.VERTICAL_SCALE = 100

        self._calculate_node_position(tree)

    def draw(self, node: Node):
        pg.draw.circle(ds.screen, "Black", (node.x, node.y), 20, 5)

        if not node.is_leaf():
            pg.draw.line(ds.screen, "Black", (node.x, node.y), (node.left.x, node.left.y), 5)
            pg.draw.line(ds.screen, "Black", (node.x, node.y), (node.right.x, node.right.y), 5)

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
                node.preliminary_x = 1
            else:
                node.preliminary_x = node.parent.left.preliminary_x \
                                    + const.SIBLING_DISTANCE + const.NODE_SIZE 
            
            return

        for child in node.children:
            self._compute_prelim_x(child)

        left_child = node.left
        right_child = node.right

        mid = float((left_child.preliminary_x + right_child.preliminary_x) / 2)

        if node.is_left_node():
            node.preliminary_x = mid
        else:
            node.preliminary_x = node.parent.left.preliminary_x \
                                + const.SIBLING_DISTANCE + const.NODE_SIZE 
            node.modifier = node.preliminary_x - mid

        if not node.is_left_node():
            self._check_for_conflicts(node)

    def _compute_final_coordinates(self, node: Node, mod_sum: float):
        node.preliminary_x += mod_sum
        mod_sum += node.modifier

        if not node.is_leaf():
            for child in node.children:
                self._compute_final_coordinates(child, mod_sum)

        node.x = node.preliminary_x * self.SCALE
        node.y = (node.depth + self.DEPTH_OFFSET) * self.VERTICAL_SCALE

    def _check_for_conflicts(self, node: Node):
        min_distance: float = const.TREE_DISTANCE + const.NODE_SIZE
        shift_value: float = 0.0

        node_contour: dict[int, float] = {}
        self._get_contour(node, 0, node_contour, _LEFT)
        print(node_contour)

        sibling = node.parent.left
        sibling_contour: dict[int, float] = {}
        self._get_contour(sibling, 0, sibling_contour, _RIGHT)
        print(sibling_contour)

        for level in range(node.depth+1, min(len(node_contour), len(sibling_contour))):
            distance = node_contour[level] - sibling_contour[level]
            if distance + shift_value < min_distance:
                shift_value = max(min_distance - distance, shift_value)

        if shift_value > 0:
            node.preliminary_x += shift_value
            node.modifier += shift_value

    def _get_contour(self, node: Node, mod_sum: float, values: dict[int, float], side: str):
        side = side.lower()

        if side not in [_LEFT, _RIGHT]:
            raise ValueError("'side' only accepts either 2 values: 'left' or 'right'.")

        if node.depth not in values:
            values[node.depth] = node.preliminary_x + mod_sum
        else:
            _fn = min if side == _LEFT else max
            values[node.y] = _fn(values[node.depth], node.preliminary_x + mod_sum)

        mod_sum += node.modifier

        if node.is_leaf():
            return

        for child in node.children:
            self._get_contour(child, mod_sum, values, side)
