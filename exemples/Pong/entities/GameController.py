from EmotionEngine.entity.EmEntity import EmEntity
from EmotionEngine.entity.EmEntitiesManager import EmEntitiesManager


class GameController(EmEntity):
    def __init__(self, creation_data: dict) -> None:
        super().__init__(creation_data)

        self.__ball: EmEntity = None
        self.__left_paddle: EmEntity = None
        self.__right_paddle: EmEntity = None

    def on_begin_play(self):
        entities_manager: EmEntitiesManager = self.get_helper().get_entities_manager()

        self.__ball = entities_manager.get_entity_by_name("Ball")
        self.__left_paddle = entities_manager.get_entity_by_name("LeftPaddle")
        self.__right_paddle = entities_manager.get_entity_by_name("RightPaddle")


expose_entity("GameController", GameController)
