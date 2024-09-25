import pygame

from EmotionEngine.collisions.AABB import AABB
from EmotionEngine.entity.EmEntity import EmEntity
from EmotionEngine.types.EmVector2 import EmVector2


class Ball(EmEntity):
    def __init__(self, creation_data: dict) -> None:
        super().__init__(creation_data)

        self.velocity = EmVector2(0.5, 0.3)
        self.speed = 0.5

        self.size = 25

        self.frozen = False

    def on_begin_play(self):
        helper = self.get_helper()

        x_center = helper.get_window_width() // 2
        y_center = helper.get_window_height() // 2

        self.set_pos(EmVector2(x_center, y_center))

    def on_draw(self, surface: pygame.display):
        pygame.draw.circle(
            surface, (255, 255, 255), self.get_pos().to_tuple(), self.size
        )

    def on_tick(self, dt: float):
        x, y = pygame.mouse.get_pos()

        self.set_pos(EmVector2(x, y))

        return
        if not self.frozen:
            helper = self.get_helper()
            x = self.get_pos().x
            y = self.get_pos().y
            w = helper.get_window_width()
            h = helper.get_window_height()

            if x <= self.size or x >= w - self.size:
                self.flip_x_vel()

            if y <= self.size or y >= h - self.size:
                self.flip_y_vel()

            self.set_pos(self.get_pos() + self.velocity * dt * self.speed)

    def get_bounding_box(self) -> AABB:
        return AABB(-self.size, -self.size, self.size, self.size)

    def flip_x_vel(self):
        self.velocity.x *= -1

    def flip_y_vel(self):
        self.velocity.y *= -1


expose_entity("Ball", Ball)
