import glob
import os

import importlib
import importlib.util

class EmEngine:
    def __init__(self, working_directory: str, entities_directory: str, levels_directory: str) -> None:
        self.__working_directory = working_directory
        self.__entities_directory = entities_directory
        self.__levels_directory = levels_directory

    def log(self, *text: str):
        print(f"[EmEngine]", *text)

    def initialize(self):
        # Loading entities classes
        self.__execute_entities_modules()
        
        # Load Textures
        # Load Sounds
        pass

    def load_level(self, level_name: str):
        # Load Level
        pass

    def get_path_from_working_directory(self, path: str):
        return f"{self.__working_directory}/{path}"

    def __execute_python_module(self, module_name: str, module_path: str):
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)

        self.log(f"Executing '{module_name}' module ...")
        spec.loader.exec_module(module)

    def __execute_entities_modules(self):
        full_entities_directory = self.get_path_from_working_directory(self.__entities_directory)
        self.log(f"Loading modules from entities directory : {full_entities_directory}")

        for python_file in os.listdir(full_entities_directory):
            full_file_path = os.path.join(full_entities_directory, python_file)

            if os.path.isfile(full_file_path) == False:
                return
            
            file_name = python_file.split(".")[0]
            file_ext = python_file.split(".")[1]

            if file_ext == "py":
                self.log(f"Entity module found '{file_name}' ({python_file})")
                self.__execute_python_module(f"entities.{file_name}", full_file_path)