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

# Initialize pygame and its subsystems
pygame.init()
pygame.mixer.init()
pygame.font.init()


class EmEngine:
    """
    Main engine class that manages game entities, levels, and the game loop.
    It initializes and maintains various managers for handling entities,
    sounds, fonts, keyboard input, and the game window.
    """

    def __init__(
        self,
        working_directory: str,
        window_width: int = 600,
        window_height: int = 600,
        game_title: str = "Emotion Engine Application",
    ) -> None:

        # Set directories for resources
        self.__entities_directory = os.path.join(working_directory, "entities")
        self.__levels_directory = os.path.join(working_directory, "levels")
        self.__sounds_directory = os.path.join(working_directory, "sounds")
        self.__fonts_directory = os.path.join(working_directory, "fonts")

        # Initialize pygame clock for managing frame rates
        self.__clock = pygame.time.Clock()
        self.__running = False

        # Is game paused ?
        self.__paused = False

        # Initialize various managers
        self.__entities_factory = EmEntityFactory()
        self.__entities_manager = EmEntitiesManager()
        self.__window_manager = EmWindowManager(
            width=window_width,
            height=window_height,
            title="Emotion Engine Application",
            engine_ref=self,
        )
        self.__keyboard_manager = EmKeyboardManager()
        self.__sounds_manager = EmSoundsManager(engine_ref=self)
        self.__fonts_manager = EmFontsManager(engine_ref=self)

        # Set game title
        self.__window_manager.set_title(game_title)

    def get_entities_directory(self) -> str:
        """Returns the directory where entity files are located."""
        return self.__entities_directory

    def get_levels_directory(self) -> str:
        """Returns the directory where level files are located."""
        return self.__levels_directory

    def get_sounds_directory(self) -> str:
        """Returns the directory where sound files are located."""
        return self.__sounds_directory

    def get_fonts_directory(self) -> str:
        """Returns the directory where font files are located."""
        return self.__fonts_directory

    def log(self, *text: str):
        """Logs messages to the console prefixed with '[EmotionEngine]'."""
        print("[EmotionEngine]", *text)

    def is_game_paused(self) -> bool:
        """
        Checks if the game is currently paused.

        Returns:
            bool: True if the game is paused, False otherwise.
        """
        return self.__paused

    def set_game_paused(self, new_paused: bool):
        """
        Sets the game's paused state.

        Args:
            new_paused (bool): The new paused state for the game.
                            If True, the game is paused; if False, the game is resumed.
        """
        self.__paused = new_paused
        self.__window_manager.update_title()

    def initialize(self):
        """Initializes the engine."""
        self.__execute_entities_modules()

    def main_loop(self):
        """Starts the main game loop, processing events and updating entities."""
        self.__running = True

        # Call on_begin_play for all instantiated entities
        for entity in self.__entities_manager.get_all_instanciated_entities():
            entity.on_begin_play()

        while self.__running:
            dt = self.__clock.tick(60)

            # Handle window events (pygame events)
            self.__process_window_events()

            instanciated_entities: List[EmEntity] = (
                self.__entities_manager.get_all_instanciated_entities()
            )

            # Update all entities that are not frozen (and if the game is not paused)
            if self.is_game_paused():
                self.__window_manager.fill_screen((25, 25, 25))

            else:
                self.__window_manager.fill_screen((0, 0, 0))
                for entity in instanciated_entities:
                    if not entity.is_frozen():
                        entity.on_tick(dt)

            current_surface = self.__window_manager.get_screen_surface()

            # Draw all entities on the current surface
            for entity in instanciated_entities:
                entity.on_draw(current_surface)

            pygame.display.flip()

    def load_level(self, level_name: str):
        """Loads a level by name and spawns its entities based on the level file.

        Args:
            level_name (str): the level name relative to the game's directory
        """
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
        """
        Instantiates and registers a new entity with the factory and manager.

        Args:
            _class (str): The class name of the entity to spawn.
            entity_name (str): The name of the entity.
            creation_data (dict): The data needed to create the entity.
        """
        entity_instance: EmEntity = self.__entities_factory.instantiate_class_by_name(
            _class, creation_data
        )

        # Create a helper for the new entity to manage dependencies
        new_helper = EmEntityHelper(
            window_manager=self.__window_manager,
            entities_manager=self.__entities_manager,
            keyboard_manager=self.__keyboard_manager,
            sounds_manager=self.__sounds_manager,
            fonts_manager=self.__fonts_manager,
        )

        # Set ID, name, and helper for the new entity
        entity_instance.set_entity_id(self.__entities_manager.count())
        entity_instance.set_entity_name(entity_name)
        entity_instance.set_helper(new_helper)

        self.__entities_manager.append(new_entity=entity_instance)

    def __process_window_events(self):
        """
        Processes window events, such as quitting the application.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_game_paused(not self.is_game_paused())

    def __callback_expose_entity(self, class_name: str, _class: any):
        """
        Callback for registering a new entity class with the factory.

        Args:
            class_name (str): The name of the class being registered.
            _class (any): The class object being registered.
        """
        self.log(f"Registered '{class_name}' class ({_class})")
        self.__entities_factory.register_class(class_name=class_name, _class=_class)

    def __execute_python_module(self, module_name: str, module_path: str):
        """
        Executes a Python module located at the given path.

        This method allows dynamic loading and execution of entity modules
        by calling the expose_entity function within the module to register
        the entity class.

        Args:
            module_name (str): The name of the module.
            module_path (str): The file path of the module to execute.
        """
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)

        module.expose_entity = self.__callback_expose_entity

        self.log(f"Executing '{module_name}' module ...")
        spec.loader.exec_module(module)

    def __execute_entities_modules(self):
        """
        Loads and executes all Python modules from the entities directory.

        This method scans the entities directory and imports each Python file
        to register the defined entity classes.
        """
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
