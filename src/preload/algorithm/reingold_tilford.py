from typing import Dict

import src.preload.system.constants as const
from src.preload.tree.node import Node
from src.preload.system.app_type import ContourType


# Implementation of the Reingold-Tilford algorithm for drawing trees
# Designed specifically for drawing full binary trees


def calculate_node_position(root: Node):
    """Calculate the position of nodes in a tree structure.

    This function computes the preliminary x-coordinates for each node starting from the root and then calculates the final coordinates based on those preliminary values. It ensures that the nodes are positioned correctly for rendering in a visual representation of the tree.

    Args:
        root (Node): The root node of the tree for which to calculate positions.
    """
    _compute_prelim_x(root)
    _compute_final_coordinates(root, 0)


def move_node_by_delta_pos(node: Node, delta_x: int, delta_y: int):
    """Move a node and its children by specified delta values.

    This function updates the position of a given node by adding the specified delta values to its x and y coordinates. If the node has children, it recursively moves each child by the same delta values.

    Args:
        node (Node): The node to move.
        delta_x (int): The change in the x-coordinate.
        delta_y (int): The change in the y-coordinate.
    """
    node.x += delta_x
    node.y += delta_y

    if node.is_leaf():
        return

    for child in node.children:
        move_node_by_delta_pos(child, delta_x, delta_y)


def _compute_prelim_x(node: Node):
    """Compute the preliminary x-coordinate for a node in a tree.

    This function calculates the preliminary x-coordinate for a given node based on its position relative to its siblings and children. It ensures that the x-coordinates are set correctly for rendering the tree structure visually, taking into account the distances between nodes.

    Args:
        node (Node): The node for which to compute the preliminary x-coordinate.
    """
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
        return

    node.preliminary_x = node.previous_sibling.preliminary_x \
        + const.SIBLING_DISTANCE + const.NODE_DISTANCE
    node.modifier = node.preliminary_x - mid
    _check_for_conflicts(node)


def _compute_final_coordinates(node: Node, mod_sum: float):
    """Compute the final coordinates for a node in a tree structure.

    This function updates the final x and y coordinates of a node based on its preliminary x value and depth in the tree. It also propagates any modifications to the coordinates down to the node's children, ensuring that the entire tree is positioned correctly for rendering.

    Args:
        node (Node): The node for which to compute the final coordinates.
        mod_sum (float): The cumulative modifier to adjust the x-coordinate.
    """
    node.preliminary_x += mod_sum
    mod_sum += node.modifier
    node.modifier = 0

    node.x = int(node.preliminary_x * const.SCALE)
    node.y = int((node.depth + const.DEPTH_OFFSET) * const.VERTICAL_SCALE)

    if node.is_leaf():
        return

    for child in node.children:
        _compute_final_coordinates(child, mod_sum)



def _check_for_conflicts(node: Node):
    """Check and resolve conflicts in node positioning within the tree.

    This function evaluates the positioning of a node relative to its previous sibling to ensure that the minimum required distance between them is maintained. If a conflict is detected, it adjusts the node's preliminary x-coordinate and modifier accordingly to resolve the overlap.

    Args:
        node (Node): The node to check for positioning conflicts.
    """
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
        if distance + shift_value >= min_distance:
            continue

        shift_value = max(min_distance - distance, shift_value)

    if shift_value == 0:
        return

    node.preliminary_x += shift_value
    node.modifier += shift_value


def _get_contour(node: Node, mod_sum: float, values: Dict[int, float], side: ContourType):
    """Retrieve the contour values for a node in the tree.

    This function populates a dictionary with the contour values of a node based on its position and depth, either from the left or right side. It recursively processes the node's children to ensure that all relevant contour values are captured, adjusting for any modifiers as necessary.

    Args:
        node (Node): The node for which to compute contour values.
        mod_sum (float): The cumulative modifier to adjust the contour values.
        values (Dict[int, float]): A dictionary to store the contour values indexed by depth.
        side (ContourType): Specifies whether to compute the left or right contour.

    Raises:
        ValueError: If 'side' is not one of the accepted values (left or right).
    """
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
