from typing import Tuple
from dataclasses import dataclass

from EmotionEngine.types.EmVector2 import EmVector2


@dataclass
class AABB:
    left: float
    bottom: float
    right: float
    top: float

    @property
    def top_right(self):
        return EmVector2(self.right, self.top)

    @property
    def bottom_left(self):
        return EmVector2(self.left, self.bottom)

    def intersects(self, other: "AABB") -> bool:
        return not (
            self.top_right.x < other.bottom_left.x
            or self.bottom_left.x > other.top_right.x
            or self.top_right.y < other.bottom_left.y
            or self.bottom_left.y > other.top_right.y
        )

    def to_tuple(self) -> Tuple[float, float, float, float]:
        return (self.left, self.bottom, self.right, self.top)
