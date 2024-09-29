import pygame
import random
import math

from EmotionEngine.collisions.AABB import AABB
from EmotionEngine.entity.EmEntity import EmEntity
from EmotionEngine.types.EmVector2 import EmVector2
from EmotionEngine.sound.EmSound import EmSound


class Ball(EmEntity):
    """
    Represents a ball entity in the game that can bounce off paddles and walls.

    The ball has properties like speed, angle, and size, and it handles its own
    movement and collision detection with paddles and walls.
    """

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

    def on_begin_play(self):
        """
        Prepares the ball entity at the beginning of the game.

        This method loads the sound effects for bouncing and throws, retrieves paddle
        entities, and sets the initial position of the ball.
        """
        helper = self.retrieve_helper()

        sounds_manager = helper.retrieve_sounds_manager()

        self.bounce_paddle_sound = sounds_manager.load_sound("se_bounce_paddle.wav")
        self.bounce_wall_sound = sounds_manager.load_sound("se_bounce_wall.wav")
        self.throw_sound = sounds_manager.load_sound("se_throw.wav")

        entities_manager = helper.retrieve_entities_manager()

        self.left_paddle = entities_manager.get_entity_by_name("LeftPaddle")
        self.right_paddle = entities_manager.get_entity_by_name("RightPaddle")

        self.set_ball_position_to_center()

    def on_draw(self, surface: pygame.display):
        """
        Draws the ball on the specified surface.

        Args:
            surface (pygame.Surface): The surface on which the ball will be drawn.
        """
        pygame.draw.circle(
            surface, (255, 255, 255), self.retrieve_pos().to_tuple(), self.size
        )

    def on_tick(self, dt: float):
        """
        Updates the ball's position and processes collisions on each game tick.

        Args:
            dt (float): The time elapsed since the last frame, used for movement calculations.
        """
        self.process_ball_collisions()

        angle_rads = math.radians(self.angle_degrees)
        velocity_vector = (
            EmVector2(math.cos(angle_rads), math.sin(angle_rads)) * self.speed
        )

        self.set_pos(self.retrieve_pos() + velocity_vector)

    def reset_speed(self):
        """
        Resets the ball's speed to its default speed.
        """
        self.speed = self.default_speed

    def increment_speed(self):
        """
        Increases the ball's speed by 10% up to the maximum speed.
        """
        if self.speed < self.max_speed:
            self.speed *= 1.1

    def process_ball_collisions(self):
        """
        Checks for collisions with paddles and walls, adjusting the ball's
        direction and speed accordingly.
        """
        if self.collide_with(self.left_paddle):
            self.angle_degrees = 180 - self.angle_degrees
            self.retrieve_pos().x += self.size // 2
            self.increment_speed()
            self.bounce_paddle_sound.play()

        if self.collide_with(self.right_paddle):
            self.angle_degrees = 180 - self.angle_degrees
            self.retrieve_pos().x -= self.size // 2
            self.increment_speed()
            self.bounce_paddle_sound.play()

        if (
            self.retrieve_pos().y - self.size <= 0
            or self.retrieve_pos().y + self.size
            >= self.retrieve_helper().get_window_height()
        ):
            self.angle_degrees = -self.angle_degrees
            self.bounce_wall_sound.play()

    def set_ball_position_to_center(self):
        """
        Sets the ball's position to the center of the window.
        """
        helper = self.retrieve_helper()

        x_center = helper.get_window_width() // 2
        y_center = helper.get_window_height() // 2

        self.set_pos(EmVector2(x_center, y_center))

    def throw_ball(self):
        """
        Throws the ball at a random angle and starts its movement.

        The ball is un-frozen and positioned at the center of the window.
        """
        self.angle_degrees = random.uniform(-45, 45) * random.choice([-1, 1])
        self.set_frozen(False)
        self.set_ball_position_to_center()
        self.throw_sound.play()

    def get_bounding_box(self) -> AABB:
        """
        Retrieves the bounding box of the ball for collision detection.

        Returns:
            AABB: An Axis-Aligned Bounding Box representing the ball's position and size.
        """
        return AABB(-self.size, -self.size, self.size, self.size)


expose_entity("Ball", Ball)
