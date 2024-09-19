from collections import deque

from src.window import pygame_window
from src.utils import const, ContourEnum
from src.dataclass import Node, QueryFunction
from src.segment_tree import SegmentTree
from src.exports.query_functions import exported_core_query_functions

class TreeManager:
    """
    Manages the operations and structure of a tree, including loading functions,
    generating node positions, and manipulating tree coordinates. This class
    provides methods to switch query function, move the tree, and compute coordinates
    for rendering.
    """

    def __init__(self, data: list[int]):
        """Initializes the TreeManager with the provided data.

        This constructor sets up the available query functions,
        initializes the current function to "add_f", and creates
        a segment tree using the provided data. It also sets the
        initial zoom level for the tree visualization.

        Args:
            data (list[int]): The list of integers to be used as
            the initial data for the segment tree.
        """

        self.available_functions: dict[str, QueryFunction] = {}
        self.load_functions(exported_core_query_functions)

        self.current_function: QueryFunction = self.available_functions["add_f"]
        self.segment_tree = SegmentTree(data, self.current_function)
        self.zoom_level: float = 1.0

    def generate_node_position(self):
        """Generate the position of nodes in a tree structure.

        This function computes the preliminary x-coordinates for each node starting
        from the root and then calculates the final coordinates based on those 
        preliminary values. It ensures that the nodes are positioned correctly for
        rendering in a visual representation of the tree.
        """

        self._compute_prelim_x(self.segment_tree.root)
        self._compute_final_coordinates(self.segment_tree.root, 0)
        self.compute_transformed_coordinates()

    def center_tree(self):
        """Centers the segment tree in the window.

        This method calculates the horizontal offset needed to position the
        segment tree's root at the center of the window. It then moves the
        tree accordingly and updates the transformed coordinates for rendering.
        """

        delta_x = pygame_window.half_window_width - self.segment_tree.root.x
        self.move_tree_by_delta_pos(delta_x, 0)
        self.compute_transformed_coordinates()

    def switch_function(self, name: str):
        """Switches the current query function to the specified function name.

        This method updates the current function used by the segment tree based
        on the provided name. If the specified function does not exist, an error
        message is printed to inform the user.

        Args:
            name (str): The name of the query function to switch to.
        """

        try:
            self.current_function = self.available_functions[name]
            self.segment_tree.switch_function(self.current_function)
        except KeyError:
            print(f"QueryFunction named <{name}> doesn't exist!")

    def load_functions(self, exported_functions: list[QueryFunction]):
        """
        Loads a list of query functions into the available functions dictionary. If a 
        function already exists, it skips adding it and prints a message indicating
        the function was skipped.

        Args:
            exported_functions (list[QueryFunction]): A list of QueryFunction objects to be loaded.
        """

        for function in exported_functions:
            if function in self.available_functions:
                print(f"QueryFunction <{function.name}> already existed! Skipping...")
                continue

            self.available_functions[function.name] = function

    def move_tree_by_delta_pos(self, delta_x: int, delta_y: int):
        """Move a tree and its children by specified delta values.

        This function adjusts the position of the root node of a tree by adding the
        specified delta values to its x and y coordinates. It then propagates these 
        changes to all child nodes, ensuring that the entire tree is moved consistently.

        Args:
            delta_x (int): The change in the x-coordinate.
            delta_y (int): The change in the y-coordinate.
        """

        queue: deque[Node] = deque([self.segment_tree.root])

        while queue:
            node = queue.popleft()
            node.x_offset += delta_x
            node.y_offset += delta_y

            if node.is_leaf():
                continue

            for child in node.children:
                queue.append(child)

    def compute_transformed_coordinates(self):
        """Compute and update the transformed coordinates of all nodes in the tree.

        This function iterates through each node in the segment tree, applying a 
        zoom factor to the original coordinates and adjusting them with any specified
        offsets. The updated coordinates are stored back in the node, allowing for 
        accurate rendering based on the current zoom level.
        """

        queue: deque[Node] = deque([self.segment_tree.root])

        while queue:
            node = queue.popleft()
            node.x = int(node.original_x * self.zoom_level) + node.x_offset
            node.y = int(node.original_y * self.zoom_level) + node.y_offset

            if node.is_leaf():
                continue

            for child in node.children:
                queue.append(child)

    def _compute_final_coordinates(self, node: Node, mod_sum: float):
        """Compute the final coordinates for a node in a tree structure.

        This function updates the final x and y coordinates of a node based on its
        preliminary x value and depth in the tree. It also propagates any 
        modifications to the coordinates down to the node's children, ensuring that
        the entire tree is positioned correctly for rendering.

        Args:
            node (Node): The node for which to compute the final coordinates.
            mod_sum (float): The cumulative modifier to adjust the x-coordinate.
        """

        node.preliminary_x += mod_sum
        mod_sum += node.modifier
        node.modifier = 0

        node.original_x = int(node.preliminary_x * const.SCALE)
        node.original_y = int((node.depth + const.DEPTH_OFFSET) * const.VERTICAL_SCALE)

        if node.is_leaf():
            return

        for child in node.children:
            self._compute_final_coordinates(child, mod_sum)

    def _compute_prelim_x(self, node: Node):
        """Compute the preliminary x-coordinate for a node in a tree.

        This function calculates the preliminary x-coordinate for a given node based
        on its position relative to its siblings and children. It ensures that the 
        x-coordinates are set correctly for rendering the tree structure visually, 
        taking into account the distances between nodes.

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
            self._compute_prelim_x(child)

        left_child = node.left
        right_child = node.right

        mid = float((left_child.preliminary_x + right_child.preliminary_x) / 2)

        if node.is_left_node():
            node.preliminary_x = mid
            return

        node.preliminary_x = node.previous_sibling.preliminary_x \
            + const.SIBLING_DISTANCE + const.NODE_DISTANCE
        node.modifier = node.preliminary_x - mid
        self._check_for_conflicts(node)

    def _check_for_conflicts(self, node: Node):
        """Check and resolve conflicts in node positioning within the tree.

        This function evaluates the positioning of a node relative to its previous
        sibling to ensure that the minimum required distance between them is 
        maintained. If a conflict is detected, it adjusts the node's preliminary
        x-coordinate and modifier accordingly to resolve the overlap.

        Args:
            node (Node): The node to check for positioning conflicts.
        """

        min_distance: float = const.TREE_DISTANCE + const.NODE_DISTANCE
        shift_value: float = 0.0

        node_contour: dict[int, float] = {}
        self._get_contour(node, 0, node_contour, ContourEnum.LEFT)

        sibling = node.previous_sibling
        sibling_contour: dict[int, float] = {}
        self._get_contour(sibling, 0, sibling_contour, ContourEnum.RIGHT)

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

    def _get_contour(self, node: Node, mod_sum: float, values: dict[int, float], side: ContourEnum):
        """Retrieve the contour values for a node in the tree.

        This function populates a dictionary with the contour values of a node based
        on its position and depth, either from the left or right side. It 
        recursively processes the node's children to ensure that all relevant 
        contour values are captured, adjusting for any modifiers as necessary.

        Args:
            node (Node): The node for which to compute contour values.
            mod_sum (float): The cumulative modifier to adjust the contour values.
            values (dict[int, float]): A dictionary to store the contour values indexed by depth.
            side (ContourEnum): Specifies whether to compute the left or right contour.

        Raises:
            ValueError: If 'side' is not one of the accepted values (left or right).
        """

        if side not in [ContourEnum.LEFT, ContourEnum.RIGHT]:
            raise ValueError("'side' only accepts either 2 values: 'left' or 'right'.")

        if node.depth not in values:
            values[node.depth] = node.preliminary_x + mod_sum
        else:
            fn = min if side == ContourEnum.LEFT else max
            values[node.depth] = fn(values[node.depth], node.preliminary_x + mod_sum)

        mod_sum += node.modifier

        if node.is_leaf():
            return

        for child in node.children:
            self._get_contour(child, mod_sum, values, side)