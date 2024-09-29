import math

from typing import Tuple
from dataclasses import dataclass


@dataclass
class EmVector2:
    """
    A class representing a 2D vector with x and y components.

    This class provides various vector operations such as addition, subtraction,
    multiplication by a scalar, and magnitude calculation.
    """

    x: float
    y: float

    def to_tuple(self) -> Tuple[float, float]:
        """
        Converts the vector to a tuple representation.

        Returns:
            Tuple[float, float]: A tuple containing the x and y components of the vector.
        """
        return (self.x, self.y)

    def __sub__(self, other):
        """Vector subtraction."""
        return EmVector2(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """Vector addition."""
        return EmVector2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        """Multiplication of a vector by a scalar."""

        if isinstance(scalar, int) or isinstance(scalar, float):
            return EmVector2(self.x * scalar, self.y * scalar)
        raise NotImplementedError("Can only multiply EmVector2 by a scalar")

    def __rmul__(self, scalar):
        """Reflected multiplication so vector * scalar also works."""
        return self.__mul__(scalar)

    def __neg__(self):
        """Negation of the vector (invert through origin.)"""
        return EmVector2(-self.x, -self.y)

    def __truediv__(self, scalar):
        """True division of the vector by a scalar."""
        return EmVector2(self.x / scalar, self.y / scalar)

    def __mod__(self, scalar):
        """One way to implement modulus operation: for each component."""
        return EmVector2(self.x % scalar, self.y % scalar)

    def __abs__(self):
        """Absolute value (magnitude) of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def __str__(self) -> str:
        return f"EmVector2({self.x}, {self.y})"

    def __repr__(self) -> str:
        return self.__str__()
