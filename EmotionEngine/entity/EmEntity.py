import pygame

from EmotionEngine.types.EmVector2 import EmVector2
from EmotionEngine.entity.EmEntityHelper import EmEntityHelper
from EmotionEngine.collisions.AABB import AABB


class EmEntity:
    """
    A class representing an entity in the system, encapsulating its creation data,
    unique identifiers, positional information, and behavior such as collision detection.

    This class provides methods for managing the entity's state, including setting
    its ID, name, position, and handling interactions like movement, drawing, and collision.
    """

    def __init__(self, creation_data: dict) -> None:
        self.__creation_data = creation_data
        self.__entity_id: int = None
        self.__entity_name: str = None
        self.__helper: EmEntityHelper = None
        self.__pos = EmVector2(0, 0)
        self.__frozen = False

    def retrieve_creation_data(self) -> dict:
        """
        Retrieves the entity's creation data.

        Returns:
            dict: A dictionary containing the entity's creation parameters.
        """
        return self.__creation_data

    def set_entity_id(self, new_entity_id: int):
        """
        Sets the entity's unique ID if it hasn't been set already.

        Args:
            new_entity_id (int): The unique identifier for the entity.
        """
        assert self.__entity_id is None
        self.__entity_id = new_entity_id

    def set_entity_name(self, new_name: str):
        """
        Sets the entity's name if it hasn't been set already.

        Args:
            new_name (str): The name to assign to the entity.
        """
        assert self.__entity_name is None
        self.__entity_name = new_name

    def get_entity_name(self) -> str:
        """
        Retrieves the entity's name.

        Returns:
            str: The name of the entity.

        Raises:
            AssertionError: If the entity name has not been set.
        """
        assert self.__entity_name is not None
        return self.__entity_name

    def set_helper(self, new_helper: EmEntityHelper):
        """
        Assigns a helper object to the entity, if it hasn't been assigned already.

        Args:
            new_helper (EmEntityHelper): The helper object to assign to the entity.
        """
        assert self.__helper is None
        self.__helper = new_helper

    def retrieve_helper(self) -> EmEntityHelper:
        """
        Retrieves the entity's helper object.

        Returns:
            EmEntityHelper: The helper associated with the entity.

        Raises:
            AssertionError: If the helper has not been set.
        """
        assert self.__helper is not None
        return self.__helper

    def set_pos(self, new_pos: EmVector2):
        """
        Sets the entity's position.

        Args:
            new_pos (EmVector2): The new position to assign to the entity.
        """
        self.__pos = new_pos

    def retrieve_pos(self) -> EmVector2:
        """
        Retrieves the entity's current position.

        Returns:
            EmVector2: The entity's current position as a 2D vector.
        """
        return self.__pos

    def on_begin_play(self):
        """
        A method that is called when the entity begins its gameplay.

        This method can be overridden to define custom behavior at the start of the game.
        """

    def on_tick(self, dt: float):
        """
        A method called every frame to update the entity.

        Args:
            dt (float): The time delta since the last frame.
        """

    def on_draw(self, surface: pygame.display):
        """
        A method called to draw the entity on the provided surface.

        Args:
            surface (pygame.display): The surface to draw the entity onto.
        """

    def get_bounding_box(self) -> AABB:
        """
        Returns the entity's axis-aligned bounding box (AABB).

        This method can be overridden to provide a specific bounding box for the entity.

        Returns:
            AABB: The entity's bounding box.
        """
        return AABB(0, 0, 0, 0)

    def get_positioned_bounding_box(self) -> AABB:
        """
        Returns the entity's bounding box, adjusted by its current position.

        Combines the entity's position with its local bounding box to get the
        positioned bounding box in world coordinates.

        Returns:
            AABB: The positioned bounding box of the entity.
        """
        pos = self.retrieve_pos()
        bbox = self.get_bounding_box()

        return AABB(
            pos.x + bbox.left,
            pos.y + bbox.bottom,
            pos.x + bbox.right,
            pos.y + bbox.top,
        )

    def collide_with(self, other: "EmEntity"):
        """
        Checks if this entity's bounding box collides with another entity's bounding box.

        Args:
            other (EmEntity): The other entity to check for collision with.

        Returns:
            bool: True if the two entities' bounding boxes intersect, False otherwise.
        """
        a = self.get_positioned_bounding_box()
        b = other.get_positioned_bounding_box()

        return a.intersects(b)

    def is_frozen(self) -> bool:
        """
        Checks whether the entity is currently frozen. When frozen, the `on_tick` method
        is not called, indicating that the entity is not updating over time.

        Returns:
            bool: True if the entity is frozen and `on_tick` is not called, False otherwise.
        """
        return self.__frozen

    def set_frozen(self, new_frozen: bool):
        """
        Sets the frozen state of the entity. If frozen, the `on_tick` method will not be called,
        effectively pausing the entity's update logic.

        Args:
            new_frozen (bool): The new frozen state to assign to the entity.
        """
        self.__frozen = new_frozen
