class Node:
    def __init__(self):
        self.left: Node = None
        self.right: Node = None
        self.parent: Node = None
        self.data: int = None
        self.depth: int = 0

        self.x: int = 0
        self.y: int = 0

        self.modifier: float = 0.0
        self.preliminary_x: float = 0.0
        self.ID = 0

    def init_child(self):
        self.left = Node()
        self.right = Node()

        self.left.parent = self.right.parent = self

    @property
    def children(self):
        return (self.left, self.right)

    @property
    def previous_sibling(self):
        return None if self.parent is None or self.is_left_node() \
            else self.parent.left

    @property
    def coordinates(self) -> tuple[int, int]:
        return (self.x, self.y)

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def is_left_node(self) -> bool:
        try:
            return self is self.parent.left
        except AttributeError:
            return True
