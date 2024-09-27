import pygame

from EmotionEngine.types.EmVector2 import EmVector2
from EmotionEngine.entity.EmEntityHelper import EmEntityHelper
from EmotionEngine.collisions.AABB import AABB


class EmEntity:
    def __init__(self, creation_data: dict) -> None:
        self.__entity_id: int = None
        self.__entity_name: str = None
        self.__helper: EmEntityHelper = None
        self.__pos = EmVector2(0, 0)
        self.__frozen = False

    def set_entity_id(self, new_entity_id: int):
        assert self.__entity_id is None
        self.__entity_id = new_entity_id

    def set_entity_name(self, new_name: str):
        assert self.__entity_name is None
        self.__entity_name = new_name

    def get_entity_name(self) -> str:
        assert self.__entity_name is not None
        return self.__entity_name

    def set_helper(self, new_helper: EmEntityHelper):
        assert self.__helper is None
        self.__helper = new_helper

    def retrieve_helper(self) -> EmEntityHelper:
        assert self.__helper is not None
        return self.__helper

    def set_pos(self, new_pos: EmVector2):
        self.__pos = new_pos

    def get_pos(self) -> EmVector2:
        return self.__pos

    def on_begin_play(self):
        pass

    def on_tick(self, dt: float):
        pass

    def on_draw(self, surface: pygame.display):
        pass

    def get_bounding_box(self) -> AABB:
        return AABB(0, 0, 0, 0)

    def get_positioned_bounding_box(self) -> AABB:
        pos = self.get_pos()
        bbox = self.get_bounding_box()

        return AABB(
            pos.x + bbox.left,
            pos.y + bbox.bottom,
            pos.x + bbox.right,
            pos.y + bbox.top,
        )

    def collide_with(self, other: "EmEntity"):
        a = self.get_positioned_bounding_box()
        b = other.get_positioned_bounding_box()

        return a.intersects(b)

    def is_frozen(self) -> bool:
        return self.__frozen

    def set_frozen(self, new_frozen: bool):
        self.__frozen = new_frozen
