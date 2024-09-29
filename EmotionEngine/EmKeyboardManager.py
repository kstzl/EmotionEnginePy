import pygame


class EmKeyboardManager:
    """
    A manager class for handling keyboard input in the game.

    This class provides functionality to check if specific keys are pressed
    during the game loop.
    """

    def is_key_pressed(self, key: any):
        """
        Checks if a specific key is currently pressed.

        Args:
            key (any): The key to check. This can be a pygame constant (e.g.,
                        pygame.K_SPACE, pygame.K_a) representing the desired key.

        Returns:
            bool: True if the specified key is pressed, False otherwise.
        """
        keys = pygame.key.get_pressed()
        return keys[key]
