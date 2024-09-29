from EmotionEngine.entity.EmEntity import EmEntity
from EmotionEngine.entity.EmEntitiesManager import EmEntitiesManager

from EmotionEngine.utils.EmTimer import EmTimer
from EmotionEngine.utils.EmAlternator import EmAlternator

from EmotionEngine.sound.EmSound import EmSound
from EmotionEngine.utils.drawing import draw_text_centered
from EmotionEngine.types.EmVector2 import EmVector2


import pygame
import random


def clamp(value: float, min: float, max: float):
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value


class GameController(EmEntity):
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

    def on_game_start(self):
        self.ball.throw_ball()
        self.point_marked = False

    def on_begin_play(self):
        self.start_timer.start()

        helper = self.retrieve_helper()

        self.win_sound = helper.retrieve_sounds_manager().load_sound("se_win.wav")
        self.loose_sound = helper.retrieve_sounds_manager().load_sound("se_loose.wav")

        self.pong_font = helper.retrieve_fonts_manager().load_font("pong-score.ttf", 80)

        entities_manager: EmEntitiesManager = (
            self.retrieve_helper().retrieve_entities_manager()
        )

        self.ball = entities_manager.get_entity_by_name("Ball")
        self.left_paddle = entities_manager.get_entity_by_name("LeftPaddle")
        self.right_paddle = entities_manager.get_entity_by_name("RightPaddle")

    def process_user_inputs(self, dt: float):
        if self.point_marked:
            return

        keyboard_manager = self.retrieve_helper().retrieve_keyboard_manager()
        window_height = self.retrieve_helper().get_window_height()

        new_y = self.left_paddle.get_pos().y

        if keyboard_manager.is_key_pressed(pygame.K_UP):
            new_y -= 0.5 * dt

        elif keyboard_manager.is_key_pressed(pygame.K_DOWN):
            new_y += 0.5 * dt

        new_y = clamp(new_y, 0, window_height - self.left_paddle.h)
        self.left_paddle.get_pos().y = new_y

    def process_ball_collisions(self):

        ball_x = self.ball.get_pos().x

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

        window_height = self.retrieve_helper().get_window_height()

        new_y = self.right_paddle.get_pos().y

        by = self.ball.get_pos().y - self.right_paddle.h // 2
        s = 0.5 * dt

        diff = abs(new_y - by)

        if diff > 1 + (self.right_paddle.h * self.ai_player_rd_seed):
            if by > new_y:
                new_y += s
            else:
                new_y -= s

        new_y = clamp(new_y, 0, window_height - self.left_paddle.h)

        self.right_paddle.get_pos().y = new_y

    def mark_point(self):
        self.point_marked = True
        self.ball.set_frozen(True)
        self.ball.reset_speed()
        self.start_timer.start()

        self.ai_player_rd_seed = random.uniform(0.1, 1)

    def on_tick(self, dt: float):

        self.left_score_alternator.update()
        self.right_score_alternator.update()

        self.start_timer.update()

        self.process_user_inputs(dt)

        if self.point_marked == False:
            self.process_ball_collisions()
            self.process_ai_paddle(dt)

    def on_draw(self, surface: pygame.surface.Surface):
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

        n = 30
        h = helper.get_window_height()
        sz = h // n

        for i in range(n + 1):
            separator_rect = pygame.Rect(0, i * sz, 1, 10)
            separator_rect.centerx = surface.get_rect().centerx

            pygame.draw.rect(surface, (255, 255, 255), separator_rect)


expose_entity("GameController", GameController)
