import os
import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from EmotionEngine.EmEngine import EmEngine

from EmotionEngine.sound.EmSound import EmSound


class EmSoundsManager:
    def __init__(self, engine_ref: "EmEngine") -> None:
        self.__engine_ref = engine_ref

    def load_sound(self, sound_path: str) -> EmSound:
        engine_sounds_directory = self.__engine_ref.get_sounds_directory()
        sound_object = pygame.mixer.Sound(
            os.path.join(engine_sounds_directory, sound_path)
        )
        return EmSound(sound_object=sound_object)
