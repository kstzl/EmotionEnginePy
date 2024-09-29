from typing import List

from EmotionEngine.entity.EmEntity import EmEntity


class EmEntitiesManager:
    """
    A manager class responsible for handling a collection of instantiated entities.

    This class allows for adding new entities, retrieving them by name,
    and querying the total number of entities in the system.
    """

    def __init__(self) -> None:
        self.__instanciated_entities: List[EmEntity] = []

    def append(self, new_entity: EmEntity):
        """
        Adds a new entity to the manager's collection of instantiated entities.

        Args:
            new_entity (EmEntity): The entity to be added to the collection.
        """
        self.__instanciated_entities.append(new_entity)

    def count(self) -> int:
        """
        Returns the total number of instantiated entities managed by this instance.

        Returns:
            int: The number of entities currently managed.
        """
        return len(self.__instanciated_entities)

    def get_all_instanciated_entities(self) -> List[EmEntity]:
        """
        Retrieves the list of all instantiated entities managed by this instance.

        Returns:
            List[EmEntity]: A list of all entities currently managed.
        """
        return self.__instanciated_entities

    def get_entity_by_name(self, query_entity_name: str) -> EmEntity:
        """
        Finds and returns an entity by its name.

        Iterates through the list of entities and returns the one that matches
        the provided name. If no entity is found with the given name, it returns None.

        Args:
            query_entity_name (str): The name of the entity to search for.

        Returns:
            EmEntity: The entity matching the provided name, or None if not found.
        """
        result: EmEntity = None

        for entity in self.__instanciated_entities:
            if entity.get_entity_name() == query_entity_name:
                result = entity
                break

        return result
