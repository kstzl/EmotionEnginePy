import pygame


class EmSound:
    def __init__(self, sound_object: pygame.mixer.Sound) -> None:
        self.__sound_object = sound_object

    def play(self):
        self.__sound_object.play()

    def stop(self):
        self.__sound_object.stop()
