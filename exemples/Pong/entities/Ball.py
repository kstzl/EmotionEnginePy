import pygame
import random
import math

from EmotionEngine.collisions.AABB import AABB
from EmotionEngine.entity.EmEntity import EmEntity
from EmotionEngine.entity.EmEntitiesManager import EmEntitiesManager
from EmotionEngine.types.EmVector2 import EmVector2
from EmotionEngine.sound.EmSound import EmSound


class Ball(EmEntity):
    def __init__(self, creation_data: dict) -> None:
        super().__init__(creation_data)

        self.angle_degrees = 0

        self.default_speed = int(creation_data["default_speed"])
        self.max_speed = int(creation_data["max_speed"])

        self.speed = self.default_speed
        self.size = 10

        self.left_paddle: EmEntity = None
        self.right_paddle: EmEntity = None

        self.bounce_paddle_sound: EmSound = None
        self.bounce_wall_sound: EmSound = None
        self.throw_sound: EmSound = None

        self.set_frozen(True)

    def reset_speed(self):
        self.speed = self.default_speed

    def increment_speed(self):
        if self.speed < self.max_speed:
            self.speed *= 1.1
            print(self.speed)

    def on_begin_play(self):
        helper = self.retrieve_helper()

        self.bounce_paddle_sound = helper.retrieve_sounds_manager().load_sound(
            "se_bounce_paddle.wav"
        )

        self.bounce_wall_sound = helper.retrieve_sounds_manager().load_sound(
            "se_bounce_wall.wav"
        )

        self.throw_sound = helper.retrieve_sounds_manager().load_sound("se_throw.wav")

        self.set_ball_position_to_center()

        entities_manager: EmEntitiesManager = helper.retrieve_entities_manager()

        self.left_paddle = entities_manager.get_entity_by_name("LeftPaddle")
        self.right_paddle = entities_manager.get_entity_by_name("RightPaddle")

    def on_draw(self, surface: pygame.display):
        pygame.draw.circle(
            surface, (255, 255, 255), self.get_pos().to_tuple(), self.size
        )

    def on_tick(self, dt: float):
        self.process_ball_collisions()

        angle_rads = math.radians(self.angle_degrees)
        velocity_vector = (
            EmVector2(math.cos(angle_rads), math.sin(angle_rads)) * self.speed
        )

        self.set_pos(self.get_pos() + velocity_vector)

    def process_ball_collisions(self):
        if self.collide_with(self.left_paddle):
            self.angle_degrees = 180 - self.angle_degrees
            self.get_pos().x += self.size // 2
            self.increment_speed()
            self.bounce_paddle_sound.play()

        if self.collide_with(self.right_paddle):
            self.angle_degrees = 180 - self.angle_degrees
            self.get_pos().x -= self.size // 2
            self.increment_speed()
            self.bounce_paddle_sound.play()

        if (
            self.get_pos().y - self.size <= 0
            or self.get_pos().y + self.size
            >= self.retrieve_helper().get_window_height()
        ):
            self.angle_degrees = -self.angle_degrees
            self.bounce_wall_sound.play()

    def set_ball_position_to_center(self):
        helper = self.retrieve_helper()

        x_center = helper.get_window_width() // 2
        y_center = helper.get_window_height() // 2

        self.set_pos(EmVector2(x_center, y_center))

    def throw_ball(self):
        self.angle_degrees = random.uniform(-45, 45) * random.choice([-1, 1])
        self.set_frozen(False)
        self.set_ball_position_to_center()
        self.throw_sound.play()

    def get_bounding_box(self) -> AABB:
        return AABB(-self.size, -self.size, self.size, self.size)


expose_entity("Ball", Ball)
