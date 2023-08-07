import src.preload.system.constants as const
from typing import Union, Tuple


class Node:
    def __init__(self):
        self.left: Union[Node, None] = None
        self.right: Union[Node, None] = None
        self.parent: Union[Node, None] = None

        self.data: int = 0
        self.low: int = 0
        self.high: int = 0

        self.x: int = 0
        self.y: int = 0

        self.depth: int = 0
        self.modifier: float = 0.0
        self.preliminary_x: float = 0.0
        self.ID: int = 0

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
