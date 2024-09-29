import pygame


class EmSound:
    """
    A class representing a sound object that can be played or stopped using Pygame's
    mixer functionality.

    This class wraps the Pygame sound object to provide simple playback controls.
    """

    def __init__(self, sound_object: pygame.mixer.Sound) -> None:
        """
        Initializes the EmSound with a Pygame sound object.

        Args:
            sound_object (pygame.mixer.Sound): The Pygame sound object to manage.
        """
        self.__sound_object = sound_object

    def play(self):
        """
        Plays the sound associated with this EmSound instance.
        """
        self.__sound_object.play()

    def stop(self):
        """
        Stops the playback of the sound associated with this EmSound instance.
        """
        self.__sound_object.stop()
