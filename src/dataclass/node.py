from src.utils import const

from typing import Optional

class Node:
    """
    Represents a node in a segment tree, containing references to its children,
    parent, and various properties related to its position and data. This class
    provides methods to initialize child nodes, construct the node with specific
    values, and determine its relationships within the tree.
    """

    __slots__ = (
        "left", "right", "parent",
        "low", "high",
        "x", "y",
        "preliminary_x", "modifier", "depth",
        "data", "ID",
        "lazy_data",
        "x_offset", "y_offset",
        "original_x", "original_y",
        "x", "y"
    )

    def __init__(self):
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.parent: Optional[Node] = None

        self.data: int = 0
        self.lazy_data: int = 0
        self.low: int = 0
        self.high: int = 0

        self.original_x: int = 0
        self.original_y: int = 0

        self.x_offset: int = 0
        self.y_offset: int = 0

        self.x: int = 0
        self.y: int = 0

        self.depth: int = 0
        self.modifier: float = 0.0
        self.preliminary_x: float = 0.0
        self.ID: int = 0

    def init_children(self):
        """
        Initializes the left and right child nodes of the current node. This method
        creates new Node instances for both children and sets their parent reference
        to the current node.
        """

        self.left = Node()
        self.right = Node()

        self.left.parent = self.right.parent = self

    def construct(self, low: int, high: int, ID: int) -> None:
        """
        Constructs the node with specified bounds and a unique identifier. This 
        method sets the depth of the node based on its position in the tree and 
        assigns the provided low and high values along with the node's ID.

        Args:
            low (int): The lower bound value associated with the node.
            high (int): The upper bound value associated with the node.
            ID (int): A unique identifier for the node.
        """

        self.depth = const.ROOT_DEPTH if self.is_root() else self.parent.depth + 1
        self.ID = ID

        self.low = low
        self.high = high

    @property
    def children(self) -> tuple['Node', 'Node']:
        """
        Returns the left and right children of the node as a tuple. This property
        provides a convenient way to access the child nodes without directly 
        referencing the attributes.

        Returns:
            tuple[Node, Node]: A tuple containing the left and right child nodes.
        """

        return (self.left, self.right)

    @property
    def previous_sibling(self) -> Optional['Node']:
        """
        Returns the previous sibling of the node, if applicable. This property 
        checks if the node is the root or a left child; if so, it returns None,
        otherwise it returns the left sibling from the parent.

        Returns:
            Optional[Node]: The previous sibling node, or None if there is no sibling.
        """

        return None if self.is_root() or self.is_left_node() \
            else self.parent.left

    @property
    def coordinates(self) -> tuple[int, int]:
        """
        Returns the current coordinates of the node as a tuple. This property 
        provides a convenient way to access the x and y position of the node.

        Returns:
            tuple[int, int]: A tuple containing the x and y coordinates of the node.
        """

        return (self.x, self.y)

    def is_leaf(self) -> bool:
        """
        Determines whether the node is a leaf node. A leaf node is defined as a 
        node that does not have any children, meaning both the left and right 
        child references are None.

        Returns:
            bool: True if the node is a leaf, False otherwise.
        """

        return self.left is None and self.right is None

    def is_root(self) -> bool:
        """
        Determines whether the node is the root of the tree. A root node is defined
        as a node that does not have a parent, meaning its parent reference is None.

        Returns:
            bool: True if the node is the root, False otherwise.
        """

        return self.parent is None

    def is_left_node(self) -> bool:
        """
        Determines whether the node is the left child of its parent. This method 
        checks if the current node is equal to the left child of its parent; if 
        the parent does not exist, it assumes the node is a left node.

        Returns:
            bool: True if the node is a left child, False otherwise.
        """

        try:
            return self is self.parent.left
        except AttributeError:
            return True
