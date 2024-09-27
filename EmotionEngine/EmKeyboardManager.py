import pygame


class EmKeyboardManager:
    def is_key_pressed(self, key: any):
        keys = pygame.key.get_pressed()
        return keys[key]
