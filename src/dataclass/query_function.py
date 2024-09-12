from typing import Callable
from dataclasses import dataclass

@dataclass(slots=True, unsafe_hash=True, frozen=True)
class QueryFunction:
    """Represents a query function with its associated metadata.

    This class encapsulates the details of a query function, including its
    name, description, the function itself, and a value indicating an invalid
    query result. It is designed to provide a structured way to manage query
    functions within the application.

    Attributes:
        name (str): The name of the query function.
        description (str): A brief description of what the query function does.
        fn (Callable[[int, int], int]): The actual function that performs the query operation.
        invalid_query_val (int): The value returned when the query is invalid.
    """

    name: str
    description: str
    fn: Callable[[int, int], int]
    invalid_query_val: int