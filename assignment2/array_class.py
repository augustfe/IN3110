"""
Array class for assignment 2
"""

from itertools import chain
from math import prod


class Array:
    def __init__(self, shape, *values):
        """Initialize an array of 1-dimensionality. Elements can only be of type:

        - int
        - float
        - bool

        Make sure the values and shape are of the correct type.

        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either int, float or boolean.

        Raises:
            TypeError: If "shape" or "values" are of the wrong type.
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """
        # Check if the values are of valid types
        if (
            (not isinstance(shape, tuple))
            and all([isinstance(i, int) for i in shape])
            and all([isinstance(i, (int, float, bool)) for i in values])
        ):
            raise TypeError("Shape or Values are wrong type")

        if not all([type(i) == type(j) for i in values for j in values]):
            raise ValueError("Not all values are the same type")

        # Check that the amount of values corresponds to the shape
        if not prod(shape) == len(values):
            raise ValueError("Shape does not correspond to amount of values")

        # Set class-variables
        self.shape = shape
        self.values = self.set_values(shape, *values)
        self.flat_array = self.flatten()

    def set_values(self, shape, *values):
        """Returns a nested list composed of values arragned according
        to the given shape.

        Goes through the values recursively, in order to create an
        n-dimensional nested list.

        Args:
            shape (tuple): The shape remaining to compose, only uses shape[0] in
                            this recursion.

        Returns:
            lst (list) : The composed nested list
            list(values) : The values corresponding to that layer

        """
        lst = []
        if len(shape) != 1:
            leng = int(len(values) / shape[0])
            for i in range(0, len(values), leng):
                lst += [self.set_values(shape[1:], *values[i : i + leng])]
            return lst
        return list(values)

    def __getitem__(self, key):
        """Returns the indexed value of the array.

        Args:
            key (int): The index to retrieve

        Returns:
            int : The indexed value
        """
        return self.values[key]

    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """
        return f"{self.values}"

    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        if not isinstance(other, (Array, float, int)):
            raise TypeError("'Other' is not array or number")
        if isinstance(other, Array) and (self.shape != other.shape):
            raise ValueError("Shapes do not match")
        if isinstance(self.flat_array[0], bool) or isinstance(other, bool):
            return NotImplemented
        if isinstance(other, (int, float)):
            return Array(self.shape, *[i + other for i in self.flat_array])
        if isinstance(other, Array):
            if isinstance(other.flat_array[0], bool):
                return NotImplemented
            return Array(
                self.shape, *[i + j for i, j in zip(self.flat_array, other.flat_array)]
            )

    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        return self.__add__(other)

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        if isinstance(self.flat_array[0], bool) or isinstance(other, bool):
            return NotImplemented
        return self + -1 * other

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        return (-1 * self).__sub__(-1 * other)

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        if not isinstance(other, (Array, float, int)):
            raise TypeError("'Other' is not array or number")
        if isinstance(other, Array) and (self.shape != other.shape):
            raise ValueError("Shapes do not match")
        if isinstance(self.flat_array[0], bool) or isinstance(other, bool):
            return NotImplemented
        if isinstance(other, (int, float)):
            return Array(self.shape, *[i * other for i in self.flat_array])
        if isinstance(other, Array):
            if isinstance(other.flat_array[0], bool):
                return NotImplemented
            return Array(
                self.shape, *[i * j for i, j in zip(self.flat_array, other.flat_array)]
            )

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        # Hint: this solution/logic applies for all r-methods
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        if not isinstance(other, Array):
            return False
        if self.shape != other.shape:
            return False
        if self.values == other.values:
            return True
        return False

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        if not isinstance(other, (Array, float, int)):
            raise TypeError("'Other' is not array or number")
        if isinstance(other, Array) and (self.shape != other.shape):
            raise ValueError("Shapes do not match")
        if isinstance(other, (float, int)):
            return Array(self.shape, *[i == other for i in self.flat_array])
        if isinstance(other, Array):
            return Array(
                self.shape, *[i == j for i, j in zip(self.flat_array, other.flat_array)]
            )
        pass

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """
        if isinstance(self.values[0], bool):
            raise TypeError("Can't take min_element of a boolean array.")
        return min(self.flat_array)
        pass

    def mean_element(self):
        """Returns the mean value of an array

        Only needs to work for type int and float (not boolean).

        Returns:
            float: the mean value
        """
        if isinstance(self.values[0], bool):
            raise TypeError("Can't take mean of a boolean array.")
        return sum(self.flat_array) / len(self.flat_array)
        pass

    def flatten(self):
        """Flattens the N-dimensional array of values into a 1-dimensional array.
        Returns:
            list: flat list of array values.
        """
        flat_array = self.values
        for _ in range(len(self.shape[1:])):
            flat_array = list(chain(*flat_array))
        return flat_array
