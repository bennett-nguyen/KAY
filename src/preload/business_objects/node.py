import src.preload.system.constants as const
from typing import Union, Tuple


class Node:
    def __init__(self):
        self.left: Node
        self.right: Node
        self.parent: Node

        self.data: int
        self.low: int
        self.high: int

        self.x: int
        self.y: int

        self.depth: int
        self.modifier: float
        self.preliminary_x: float
        self.ID: int

    def init_child(self):
        self.left = Node()
        self.right = Node()

        self.left.parent = self.right.parent = self

    def construct(self, low: int, high: int, ID: int) -> None:
        self.depth = const.ROOT_DEPTH if self.is_root() else self.parent.depth + 1
        self.ID = ID

        self.low = low
        self.high = high

    @property
    def children(self) -> Tuple['Node', 'Node']:
        return (self.left, self.right)

    @property
    def previous_sibling(self) -> Union[None, 'Node']:
        return None if self.is_root() or self.is_left_node() \
            else self.parent.left

    @property
    def coordinates(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def is_root(self) -> bool:
        return self.parent is None

    def is_left_node(self) -> bool:
        try:
            return self is self.parent.left
        except AttributeError:
            return True
