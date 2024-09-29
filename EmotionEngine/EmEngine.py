import os
import yaml
import pygame

import importlib
import importlib.util

from typing import List

from EmotionEngine.entity.EmEntitiesManager import EmEntitiesManager
from EmotionEngine.entity.EmEntitiesFactory import EmEntityFactory
from EmotionEngine.entity.EmEntity import EmEntity
from EmotionEngine.entity.EmEntityHelper import EmEntityHelper
from EmotionEngine.EmWindowManager import EmWindowManager
from EmotionEngine.EmKeyboardManager import EmKeyboardManager
from EmotionEngine.sound.EmSoundsManager import EmSoundsManager
from EmotionEngine.text.EmFontsManager import EmFontsManager

# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()


class EmEngine:
    def __init__(
        self,
        working_directory: str,
        window_width: int = 600,
        window_height: int = 600,
    ) -> None:

        self.__entities_directory = os.path.join(working_directory, "entities")
        self.__levels_directory = os.path.join(working_directory, "levels")
        self.__sounds_directory = os.path.join(working_directory, "sounds")
        self.__fonts_directory = os.path.join(working_directory, "fonts")

        self.__entities_factory = EmEntityFactory()
        self.__entities_manager = EmEntitiesManager()
        self.__window_manager = EmWindowManager(
            width=window_width, height=window_height
        )
        self.__keyboard_manager = EmKeyboardManager()
        self.__sounds_manager = EmSoundsManager(engine_ref=self)
        self.__fonts_manager = EmFontsManager(engine_ref=self)

        self.__clock = pygame.time.Clock()
        self.__running = False

    def get_sounds_directory(self) -> str:
        return self.__sounds_directory

    def get_fonts_directory(self) -> str:
        return self.__fonts_directory

    def log(self, *text: str):
        print("[EmotionEngine]", *text)

    def initialize(self):
        # Loading entities classes
        self.__execute_entities_modules()

        # self.__screen =

        # Load Textures
        # Load Sounds

    def main_loop(self):
        self.__running = True

        for entity in self.__entities_manager.get_all_instanciated_entities():
            entity.on_begin_play()

        while self.__running:
            dt = self.__clock.tick(60)

            self.__process_window_events()

            instanciated_entities: List[EmEntity] = (
                self.__entities_manager.get_all_instanciated_entities()
            )

            for entity in instanciated_entities:
                if not entity.is_frozen():
                    entity.on_tick(dt)

            self.__window_manager.fill_screen((0, 0, 0))

            current_surface = self.__window_manager.get_screen_surface()

            for entity in instanciated_entities:
                entity.on_draw(current_surface)

            pygame.display.flip()

    def load_level(self, level_name: str):
        # Load Level
        self.log(f"Loading level : {level_name}")

        full_level_path = os.path.join(self.__levels_directory, level_name)

        with open(full_level_path, "r", encoding="UTF-8") as level_file:
            yaml_data = yaml.safe_load(level_file)

            for entity_data in yaml_data["entities"]:
                entity_name: str = entity_data["name"]
                entity_class: str = entity_data["class"]

                self.log(f"Creating '{entity_name}' entity ...")
                self.__spawn_entity(entity_class, entity_name, entity_data)

    def __spawn_entity(self, _class: str, entity_name: str, creation_data: dict):
        entity_instance: EmEntity = self.__entities_factory.instantiate_class_by_name(
            _class, creation_data
        )

        new_helper = EmEntityHelper(
            window_manager=self.__window_manager,
            entities_manager=self.__entities_manager,
            keyboard_manager=self.__keyboard_manager,
            sounds_manager=self.__sounds_manager,
            fonts_manager=self.__fonts_manager,
        )

        entity_instance.set_entity_id(self.__entities_manager.count())
        entity_instance.set_entity_name(entity_name)
        entity_instance.set_helper(new_helper)

        self.__entities_manager.append(new_entity=entity_instance)

    def __process_window_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

    def __callback_expose_entity(self, class_name: str, _class: any):
        self.log(f"Registered '{class_name}' class ({_class})")
        self.__entities_factory.register_class(class_name=class_name, _class=_class)

    def __execute_python_module(self, module_name: str, module_path: str):
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)

        module.expose_entity = self.__callback_expose_entity

        self.log(f"Executing '{module_name}' module ...")
        spec.loader.exec_module(module)

    def __execute_entities_modules(self):
        self.log(
            f"Loading modules from entities directory : {self.__entities_directory}"
        )

        for python_file in os.listdir(self.__entities_directory):
            full_file_path = os.path.join(self.__entities_directory, python_file)

            if not os.path.isfile(full_file_path):
                return

            file_name = python_file.split(".")[0]
            file_ext = python_file.split(".")[1]

            if file_ext == "py":
                self.log(f"Entity module found '{file_name}' ({python_file})")
                self.__execute_python_module(f"entities.{file_name}", full_file_path)
