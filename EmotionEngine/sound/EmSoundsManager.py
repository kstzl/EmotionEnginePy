import os
import pygame

from typing import TYPE_CHECKING
from EmotionEngine.sound.EmSound import EmSound

if TYPE_CHECKING:
    from EmotionEngine.EmEngine import EmEngine


class EmSoundsManager:
    """
    A manager class responsible for loading and handling sound objects within the engine.

    This class provides methods to load sound files from a specified directory and
    manage their playback through the Pygame mixer.
    """

    def __init__(self, engine_ref: "EmEngine") -> None:
        self.__engine_ref = engine_ref

    def load_sound(self, sound_path: str) -> EmSound:
        """
        Loads a sound file from the game's sounds directory and returns an
        EmSound instance that wraps the Pygame sound object.

        Args:
            sound_path (str): The relative path to the sound file to load,
            relative to the game's sounds directory.

        Returns:
            EmSound: An instance of EmSound representing the loaded sound.
        """
        game_sounds_directory = self.__engine_ref.get_sounds_directory()
        sound_object = pygame.mixer.Sound(
            os.path.join(game_sounds_directory, sound_path)
        )
        return EmSound(sound_object=sound_object)
