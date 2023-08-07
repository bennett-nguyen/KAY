from typing import Callable
from src.preload.business_objects.node import Node

from typing import List


class SegmentTree:
    def __init__(self, arr: List[int], invalid_query_val: int, query_fn: Callable[[int, int], int], update_fn: Callable[[int, int], int]):
        self.arr = arr
        self.length = len(arr)
        self.root = Node()

        self._query_fn = query_fn
        self._update_fn = update_fn
        self._INVALID_QUERY = invalid_query_val
        self._build(self.root, 0, self.length-1)

    def query(self, q_low: int, q_high: int) -> int:
        return self._query(q_low, q_high, self.root, 0, self.length-1)

    def update(self, pos: int, val: int) -> None:
        self._update(pos, val, self.root, 0, self.length-1)

    def _build(self, node: Node, low: int, high: int, ID: int = 1) -> None:
        node.construct(low, high, ID)

        if low == high:
            node.data = self.arr[low]
            return

        node.init_child()

        mid = (low+high)//2
        self._build(node.left, low, mid, 2*ID)
        self._build(node.right, mid+1, high, 2*ID+1)

        self._update_current_node(node)

    def _update(self, pos: int, val: int, node: Node, low: int, high: int) -> None:
        if low == high:
            node.data = val
            return

        mid = (low+high)//2
        if pos <= mid:
            self._update(pos, val, node.left, low, mid)
        else:
            self._update(pos, val, node.right, mid+1, high)

        self._update_current_node(node)

    def _query(self, q_low: int, q_high: int, node: Node, low: int, high: int) -> int:
        if self._query_is_invalid(q_low, q_high, low, high):
            return self._INVALID_QUERY
        if self._query_is_within_range(q_low, q_high, low, high):
            return node.data

        mid = (low+high)//2
        left_child = self._query(q_low, q_high, node.left, low, mid)
        right_child = self._query(q_low, q_high, node.right, mid+1, high)

        return self._query_fn(left_child, right_child)

    def _query_is_invalid(self, q_low: int, q_high: int, low: int, high: int) -> bool:
        return low > high or low > q_high or high < q_low

    def _query_is_within_range(self, q_low: int, q_high: int, low: int, high: int) -> bool:
        return q_low <= low and high <= q_high

    def _update_current_node(self, node: Node) -> None:
        node.data = self._update_fn(node.left.data, node.right.data)
