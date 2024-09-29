from typing import Tuple
from dataclasses import dataclass

from EmotionEngine.types.EmVector2 import EmVector2


@dataclass
class AABB:
    """
    Representation of an Axis-Aligned Bounding Boxes (AABB) and its utility functions
    """

    left: float
    bottom: float
    right: float
    top: float

    @property
    def top_right(self):
        """
        Returns the top-right corner of the bounding box as an EmVector2 instance.

        The top-right corner is defined by the `right` and `top` edges of the bounding box.

        Returns:
            EmVector2: A 2D vector representing the top-right corner (right, top).
        """
        return EmVector2(self.right, self.top)

    @property
    def bottom_left(self):
        """
        Returns the bottom-left corner of the bounding box as an EmVector2 instance.

        The bottom-left corner is defined by the `left` and `bottom` edges of the bounding box.

        Returns:
            EmVector2: A 2D vector representing the bottom-left corner (left, bottom).
        """
        return EmVector2(self.left, self.bottom)

    def intersects(self, other: "AABB") -> bool:
        """
        Checks whether this bounding box intersects with another AABB.

        Two bounding boxes intersect if they overlap on both the x-axis and y-axis.
        This method uses the edges of the bounding boxes to determine if there is any overlap.

        Args:
            other (AABB): Another axis-aligned bounding box to check for intersection.

        Returns:
            bool: True if the bounding boxes intersect, False otherwise.
        """
        return not (
            self.top_right.x < other.bottom_left.x
            or self.bottom_left.x > other.top_right.x
            or self.top_right.y < other.bottom_left.y
            or self.bottom_left.y > other.top_right.y
        )

    def to_tuple(self) -> Tuple[float, float, float, float]:
        """
        Converts the bounding box to a tuple of its edges.

        The tuple is returned in the form: (left, bottom, right, top).

        Returns:
            Tuple[float, float, float, float]: A tuple representing the edges of the bounding box.
        """
        return (self.left, self.bottom, self.right, self.top)
