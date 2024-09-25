from typing import List

from EmotionEngine.entity.EmEntity import EmEntity


class EmEntitiesManager:
    def __init__(self) -> None:
        self.__instanciated_entities: List[EmEntity] = []

    def append(self, new_entity: EmEntity):
        self.__instanciated_entities.append(new_entity)

    def count(self) -> int:
        return len(self.__instanciated_entities)

    def get_all_instanciated_entities(self) -> List[EmEntity]:
        return self.__instanciated_entities

    def get_entity_by_name(self, query_entity_name: str) -> EmEntity:
        result: EmEntity = None

        for entity in self.__instanciated_entities:
            if entity.get_entity_name() == query_entity_name:
                result = entity
                break

        return result
