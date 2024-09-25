import pygame

from EmotionEngine.entity.EmEntity import EmEntity
from EmotionEngine.collisions.AABB import AABB


class Paddle(EmEntity):
    def __init__(self, creation_data: dict) -> None:
        super().__init__(creation_data)

        self.w = 25
        self.h = 150

        self.paddle_type: str = creation_data["paddle_type"]

    def on_begin_play(self):
        helper = self.get_helper()

        y_center = helper.get_window_height() // 2

        if self.paddle_type == "left":
            self.get_pos().x = 90

        elif self.paddle_type == "right":
            self.get_pos().x = helper.get_window_width() - 30 - self.w

        self.get_pos().y = y_center - self.h // 2

    def on_draw(self, surface: pygame.surface):
        x = self.get_pos().x
        y = self.get_pos().y

        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(x, y, self.w, self.h))

    def get_bounding_box(self) -> AABB:
        return AABB(0, 0, self.w, self.h)


expose_entity("Paddle", Paddle)
