from src.dataclass import Node
from src.dataclass import QueryFunction 

class SegmentTree:
    """
    Represents a segment tree data structure that allows for efficient range 
    queries and updates on an array. This class provides methods to initialize 
    the tree, perform queries, update values, and rebuild the tree as needed.
    """

    def __init__(self, array: list[int], function_obj: QueryFunction):
        """Initialize a segment tree with the given array and function object.

        This constructor sets up the segment tree by storing the input array and 
        defining the function used for queries. It initializes the root node and 
        builds the segment tree structure based on the provided array.

        Args:
            array (list[int]): The array of integers to be represented in the segment tree.
            function_obj (QueryFunction): An object containing the function used for 
            combining values and the value to return for invalid queries.
        """

        self.array = array
        self.root = Node()

        self._fn = function_obj.fn
        self._INVALID_QUERY = function_obj.invalid_query_val
        self._build(self.root, 0, self.array_length-1)

    @property
    def array_length(self) -> int:
        """Get the length of the underlying array.

        This property returns the number of elements in the array associated with 
        the segment tree. It provides a convenient way to access the size of the 
        array without directly interacting with it.

        Returns:
            int: The length of the array.
        """

        return len(self.array)

    def switch_function(self, function_obj: QueryFunction):
        """
        Switches the function used for queries in the segment tree. This method 
        updates the internal function reference and the value returned for invalid
        queries based on the provided function object.

        Args:
            function_obj (QueryFunction): The new function object containing the function
            for combining values and the value for invalid queries.
        """

        self._fn = function_obj.fn
        self._INVALID_QUERY = function_obj.invalid_query_val

    def query(self, q_low: int, q_high: int) -> int:
        """Retrieve the result of a query on the segment tree for a specified range.

        This function queries the segment tree to compute the aggregate value for 
        the elements within the range defined by `q_low` and `q_high`. It delegates
        the actual querying logic to a private method that handles the specifics of
        the segment tree traversal.

        Args:
            q_low (int): The lower bound of the range to query.
            q_high (int): The upper bound of the range to query.

        Returns:
            int: The result of the query for the specified range.
        """

        return self._query(q_low, q_high, self.root, 0, self.array_length-1)

    def update(self, pos: int, val: int) -> None:
        """Update the value at a specified position in the segment tree.

        This function modifies the value of an element in the segment tree at the
        given position. It delegates the actual update logic to a private method 
        that handles the specifics of the segment tree traversal and value adjustment.

        Args:
            pos (int): The position in the segment tree to update.
            val (int): The new value to set at the specified position.
        """

        self.array[pos] = val
        self._update(pos, val, self.root, 0, self.array_length-1)

    def rebuild(self):
        """Rebuild the segment tree from the current array.

        This function initializes a new root node for the segment tree and constructs
        the tree structure based on the current array. It ensures that the segment 
        tree is updated to reflect any changes in the underlying data.
        """

        self.root = Node()
        self._build(self.root, 0, self.array_length-1)

    def _build(self, node: Node, low: int, high: int, ID: int = 1) -> None:
        """Recursively build the segment tree from the given array.

        This function constructs the segment tree by initializing nodes and setting
        their values based on the specified range. It divides the range into 
        subranges and recursively builds the left and right child nodes, combining
        their values using the specified function.

        Args:
            node (Node): The current node being constructed in the segment tree.
            low (int): The lower index of the range for the current node.
            high (int): The upper index of the range for the current node.
            ID (int, optional): The identifier for the current node. Defaults to 1.
        """

        if self.array_length == 0:
            return

        node.construct(low, high, ID)

        if low == high:
            node.data = self.array[low]
            return

        node.init_children()

        mid = (low+high) // 2
        self._build(node.left, low, mid, 2*ID)
        self._build(node.right, mid+1, high, 2*ID+1)

        node.data = self._fn(node.left.data, node.right.data)

    def _update(self, pos: int, val: int, node: Node, low: int, high: int) -> None:
        """Recursively update the value at a specified position in the segment tree.

        This function modifies the value of a node in the segment tree at the given
        position and updates the relevant parent nodes accordingly. It traverses the
        tree to find the correct node to update based on the specified position and
        ensures that the current node's value is updated after the change.

        Args:
            pos (int): The position in the segment tree to update.
            val (int): The new value to set at the specified position.
            node (Node): The current node being updated in the segment tree.
            low (int): The lower index of the range for the current node.
            high (int): The upper index of the range for the current node.
        """

        if low == high:
            node.data = val
            return

        mid = (low+high) // 2
        if pos <= mid:
            self._update(pos, val, node.left, low, mid)
        else:
            self._update(pos, val, node.right, mid+1, high)

        node.data = self._fn(node.left.data, node.right.data)

    def _query(self, q_low: int, q_high: int, node: Node, low: int, high: int) -> int:
        """Recursively query the segment tree for a specified range.

        This function retrieves the aggregate value for the elements within the 
        range defined by `q_low` and `q_high`. It checks for invalid queries and 
        determines if the current node's range is fully within the query range, 
        returning the node's data if so, or recursively querying the left and right
        children otherwise.

        Args:
            q_low (int): The lower bound of the query range.
            q_high (int): The upper bound of the query range.
            node (Node): The current node being queried in the segment tree.
            low (int): The lower index of the range for the current node.
            high (int): The upper index of the range for the current node.
        """

        if self._is_query_invalid(q_low, q_high, low, high):
            return self._INVALID_QUERY
        if self._is_query_within_range(q_low, q_high, low, high):
            return node.data

        mid = (low+high) // 2
        left_child = self._query(q_low, q_high, node.left, low, mid)
        right_child = self._query(q_low, q_high, node.right, mid+1, high)

        return self._fn(left_child, right_child)

    def _is_query_invalid(self, q_low: int, q_high: int, low: int, high: int) -> bool:
        """Check if the query range is invalid.

        This function determines whether the specified query range is valid by 
        checking if the lower bound exceeds the upper bound or if the query range
        does not overlap with the current range. It returns a boolean indicating 
        the validity of the query.

        Args:
            q_low (int): The lower bound of the query range.
            q_high (int): The upper bound of the query range.
            low (int): The lower index of the current range.
            high (int): The upper index of the current range.

        Returns:
            bool: True if the query range is invalid, otherwise False.
        """

        return low > high or low > q_high or high < q_low

    def _is_query_within_range(self, q_low: int, q_high: int, low: int, high: int) -> bool:
        """Check if the current range is fully within the query range.

        This function determines whether the specified range defined by `low` and 
        `high` is completely contained within the query range defined by `q_low` 
        and `q_high`. It returns a boolean indicating if the current range is within
        the bounds of the query.

        Args:
            q_low (int): The lower bound of the query range.
            q_high (int): The upper bound of the query range.
            low (int): The lower index of the current range.
            high (int): The upper index of the current range.

        Returns:
            bool: True if the current range is within the query range, otherwise False.
        """

        return q_low <= low and high <= q_high
