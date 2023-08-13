from typing import Dict
from src.preload.system.app_type import ContourType
from src.preload.business_objects.node import Node
import src.preload.system.constants as const


# Implementation of the Reingold-Tilford algorithm for drawing trees
# Designed specifically for drawing complete binary trees


def calculate_node_position(root: Node):
    _compute_prelim_x(root)
    _compute_final_coordinates(root, 0)


def move_node_by_delta_pos(node: Node, delta_x: int, delta_y: int):
    node.x += delta_x
    node.y += delta_y

    if node.is_leaf():
        return

    for child in node.children:
        move_node_by_delta_pos(child, delta_x, delta_y)


def _compute_prelim_x(node: Node):
    if node.is_leaf():
        if node.is_left_node():
            node.preliminary_x = 0
        else:
            node.preliminary_x = node.previous_sibling.preliminary_x \
                + const.SIBLING_DISTANCE + const.NODE_DISTANCE

        return

    for child in node.children:
        _compute_prelim_x(child)

    left_child = node.left
    right_child = node.right

    mid = float((left_child.preliminary_x + right_child.preliminary_x) / 2)

    if node.is_left_node():
        node.preliminary_x = mid
    else:
        node.preliminary_x = node.previous_sibling.preliminary_x \
            + const.SIBLING_DISTANCE + const.NODE_DISTANCE
        node.modifier = node.preliminary_x - mid

    if not node.is_left_node():
        _check_for_conflicts(node)


def _compute_final_coordinates(node: Node, mod_sum: float):
    node.preliminary_x += mod_sum
    mod_sum += node.modifier
    node.modifier = 0

    if not node.is_leaf():
        for child in node.children:
            _compute_final_coordinates(child, mod_sum)

    node.x = int(node.preliminary_x * const.SCALE)
    node.y = int((node.depth + const.DEPTH_OFFSET) * const.VERTICAL_SCALE)


def _check_for_conflicts(node: Node):
    min_distance: float = const.TREE_DISTANCE + const.NODE_DISTANCE
    shift_value: float = 0.0

    node_contour: Dict[int, float] = {}
    _get_contour(node, 0, node_contour, const.CONTOUR_LEFT)

    sibling = node.previous_sibling
    sibling_contour: Dict[int, float] = {}
    _get_contour(sibling, 0, sibling_contour, const.CONTOUR_RIGHT)

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
        node.preliminary_x += shift_value
        node.modifier += shift_value


def _get_contour(node: Node, mod_sum: float, values: Dict[int, float], side: ContourType):
    if side not in [const.CONTOUR_LEFT, const.CONTOUR_RIGHT]:
        raise ValueError("'side' only accepts either 2 values: 'left' or 'right'.")

    if node.depth not in values:
        values[node.depth] = node.preliminary_x + mod_sum
    else:
        fn = min if side == const.CONTOUR_LEFT else max
        values[node.depth] = fn(values[node.depth], node.preliminary_x + mod_sum)

    mod_sum += node.modifier

    if node.is_leaf():
        return

    for child in node.children:
        _get_contour(child, mod_sum, values, side)
