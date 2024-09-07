from typing import Callable

class Function:
    __slots__ = ("name", "fn", "invalid_query_val")

    def __init__(self, name: str, fn: Callable[[int, int], int], invalid_query_val: int):
        self.name = name
        self.fn = fn
        self.invalid_query_val = invalid_query_val