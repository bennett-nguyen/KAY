from typing import Callable
from dataclasses import dataclass

@dataclass(slots=True, unsafe_hash=True, frozen=True)
class Function:
    """
    Represents a function that can be used for making segment tree queries. This 
    class encapsulates the function's name, the callable itself, and a value to 
    return for invalid queries, providing a structured way to manage functions.

    Attributes:
        name (str): The name of the function.
        fn (Callable[[int, int], int]): The callable function that takes two integers and returns an integer.
        invalid_query_val (int): The value to return when a query is invalid.
    """

    name: str
    fn: Callable[[int, int], int]
    invalid_query_val: int