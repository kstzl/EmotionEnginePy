import pygame
import random

from EmotionEngine.entity.EmEntity import EmEntity
from EmotionEngine.entity.EmEntitiesManager import EmEntitiesManager

from EmotionEngine.utils.EmTimer import EmTimer
from EmotionEngine.utils.EmAlternator import EmAlternator

from EmotionEngine.sound.EmSound import EmSound
from EmotionEngine.utils.drawing import draw_text_centered
from EmotionEngine.types.EmVector2 import EmVector2


def clamp(value: float, min_value: float, max_value: float):
    """
    Clamps a value between a minimum and maximum value.

    Args:
        value (float): The value to clamp.
        min_value (float): The minimum value.
        max_value (float): The maximum value.

    Returns:
        float: The clamped value.
    """
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    else:
        return value


class GameController(EmEntity):
    """
    Manages the game logic, including player scores, paddle movements, and ball behavior.

    The GameController tracks the state of the game, handles user inputs for the left paddle,
    and controls the right paddle as an AI. It also manages scoring and resets after
    points are scored.
    """

    def __init__(self, creation_data: dict) -> None:
        super().__init__(creation_data)

        self.ball: EmEntity = None
        self.left_paddle: EmEntity = None
        self.right_paddle: EmEntity = None

        self.start_timer = EmTimer(
            delay_ms=1500, callback_on_finished=self.on_game_start
        )

        self.left_player_score = 0
        self.right_player_score = 0

        self.ai_player_rd_seed = 1

        self.point_marked = False

        self.win_sound: EmSound = None
        self.loose_sound: EmSound = None

        self.pong_font = None

        self.left_score_alternator = EmAlternator(delay_ms=50, count=5)
        self.right_score_alternator = EmAlternator(delay_ms=50, count=5)

    def on_begin_play(self):
        """
        Prepares the game controller at the beginning of the game.

        This method starts the timer, loads sounds, and retrieves paddle and ball entities.
        """
        self.start_timer.start()

        helper = self.retrieve_helper()
        sounds_manager = helper.retrieve_sounds_manager()

        self.win_sound = sounds_manager.load_sound("se_win.wav")
        self.loose_sound = sounds_manager.load_sound("se_loose.wav")
        self.emotional_intro_sound = sounds_manager.load_sound("se_emotional_intro.wav")

        self.pong_font = helper.retrieve_fonts_manager().load_font("pong-score.ttf", 80)

        entities_manager: EmEntitiesManager = helper.retrieve_entities_manager()

        self.ball = entities_manager.get_entity_by_name("Ball")
        self.left_paddle = entities_manager.get_entity_by_name("LeftPaddle")
        self.right_paddle = entities_manager.get_entity_by_name("RightPaddle")

        self.emotional_intro_sound.play()

    def on_tick(self, dt: float):
        """
        Updates the game state on each game tick.

        This method updates timers, processes user inputs, and handles ball collisions
        and AI paddle movement.

        Args:
            dt (float): The time elapsed since the last frame, used for movement calculations.
        """
        self.left_score_alternator.update()
        self.right_score_alternator.update()

        self.start_timer.update()

        self.process_user_inputs(dt)

        if self.point_marked is False:
            self.process_ball_collisions()
            self.process_ai_paddle(dt)

    def on_draw(self, surface: pygame.surface.Surface):
        """
        Draws the current game state on the specified surface.

        This method draws player scores and a separator on the screen.

        Args:
            surface (pygame.Surface): The surface on which the game will be drawn.
        """
        helper = self.retrieve_helper()

        xcenter = helper.get_window_width() // 2 + 20
        ycenter = 60

        if self.left_score_alternator.get_visible():
            # Left player score
            draw_text_centered(
                self.pong_font,
                surface,
                str(self.left_player_score),
                (255, 255, 255),
                EmVector2(xcenter - 100, ycenter),
            )

        if self.right_score_alternator.get_visible():
            # Right player score (AI)
            draw_text_centered(
                self.pong_font,
                surface,
                str(self.right_player_score),
                (255, 255, 255),
                EmVector2(xcenter + 100, ycenter),
            )

        # Separator

        sep_count = 30
        window_height = helper.get_window_height()
        sep_height = window_height // sep_count

        for i in range(sep_count + 1):
            separator_rect = pygame.Rect(0, i * sep_height, 1, 10)
            separator_rect.centerx = surface.get_rect().centerx

            pygame.draw.rect(surface, (255, 255, 255), separator_rect)

    def on_game_start(self):
        """
        Starts the game by throwing the ball.

        This method is called after the start timer finishes.
        """
        self.ball.throw_ball()
        self.point_marked = False

    def process_user_inputs(self, dt: float):
        """
        Processes user inputs for controlling the left paddle.

        Args:
            dt (float): The time elapsed since the last frame, used for paddle
            movement calculations.
        """
        if self.point_marked:
            return

        helper = self.retrieve_helper()

        keyboard_manager = helper.retrieve_keyboard_manager()
        window_height = helper.get_window_height()

        new_y = self.left_paddle.retrieve_pos().y

        if keyboard_manager.is_key_pressed(pygame.K_UP):
            new_y -= 0.5 * dt

        elif keyboard_manager.is_key_pressed(pygame.K_DOWN):
            new_y += 0.5 * dt

        new_y = clamp(new_y, 0, window_height - self.left_paddle.h)
        self.left_paddle.retrieve_pos().y = new_y

    def process_ball_collisions(self):
        """
        Checks for ball collisions with the boundaries.

        If the ball goes off-screen, the corresponding player scores a point and sounds are played.
        """
        ball_x = self.ball.retrieve_pos().x

        if ball_x < 0:
            self.loose_sound.play()
            self.right_player_score += 1
            self.right_score_alternator.start()
            self.mark_point()

        elif ball_x > self.retrieve_helper().get_window_width():
            self.win_sound.play()
            self.left_player_score += 1
            self.left_score_alternator.start()
            self.mark_point()

    def process_ai_paddle(self, dt: float):
        """
        Controls the AI paddle's movement based on the ball's position.

        Args:
            dt (float): The time elapsed since the last frame, used for paddle
            movement calculations.
        """
        window_height = self.retrieve_helper().get_window_height()

        new_y = self.right_paddle.retrieve_pos().y

        by = self.ball.retrieve_pos().y - self.right_paddle.h // 2
        s = 0.5 * dt

        diff = abs(new_y - by)

        if diff > 1 + (self.right_paddle.h * self.ai_player_rd_seed):
            if by > new_y:
                new_y += s
            else:
                new_y -= s

        new_y = clamp(new_y, 0, window_height - self.left_paddle.h)

        self.right_paddle.retrieve_pos().y = new_y

    def mark_point(self):
        """
        Marks a point in the game, freezes the ball, and resets its speed.

        This method is called when a player scores.
        """
        self.point_marked = True
        self.ball.set_frozen(True)
        self.ball.reset_speed()
        self.start_timer.start()

        self.ai_player_rd_seed = random.uniform(0.1, 1)


expose_entity("GameController", GameController)
