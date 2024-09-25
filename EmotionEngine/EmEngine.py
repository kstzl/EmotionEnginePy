import os
import yaml
import pygame

import importlib
import importlib.util

from typing import List

from EmotionEngine.entity.EmEntitiesManager import EmEntitiesManager
from EmotionEngine.entity.EmEntitiesFactory import EmEntityFactory
from EmotionEngine.EmWindowManager import EmWindowManager
from EmotionEngine.entity.EmEntity import EmEntity
from EmotionEngine.entity.EmEntityHelper import EmEntityHelper

# Initialize pygame
pygame.init()
pygame.mixer.init()


class EmEngine:
    def __init__(
        self,
        working_directory: str,
        window_width: int = 600,
        window_height: int = 600,
    ) -> None:

        self.__working_directory = working_directory
        self.__entities_directory = os.path.join(working_directory, "entities")
        self.__levels_directory = os.path.join(working_directory, "levels")

        self.__entities_factory = EmEntityFactory()
        self.__entities_manager = EmEntitiesManager()
        self.__window_manager = EmWindowManager(
            width=window_width, height=window_height
        )

        self.__clock = pygame.time.Clock()
        self.__running = False

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
                entity.on_tick(dt)

            self.__window_manager.fill_screen((0, 0, 0))

            current_surface = self.__window_manager.get_screen_surface()

            for entity in instanciated_entities:
                entity.on_draw(current_surface)

            for entity_a in instanciated_entities:

                at_least_one_collision = False

                for entity_b in instanciated_entities:
                    if entity_a is not entity_b:
                        if entity_a.collide_with(entity_b):
                            at_least_one_collision = True

                bbox = entity_a.get_bounding_box()

                x = entity_a.get_pos().x
                y = entity_a.get_pos().y

                pygame.draw.rect(
                    current_surface,
                    (255, 0, 0) if at_least_one_collision else (150, 0, 0),
                    (
                        x + bbox.left,
                        y + bbox.bottom,
                        bbox.right,
                        bbox.top,
                    ),
                    2,
                )

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
