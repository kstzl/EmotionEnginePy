import os

from EmotionEngine.EmEngine import EmEngine

if __name__ == "__main__":
    current_directory = dir_path = os.path.dirname(os.path.realpath(__file__))

    engineInstance = EmEngine(
        working_directory=current_directory,
        entities_directory="entities",
        levels_directory="levels"
    )

    engineInstance.initialize()
    engineInstance.load_level("./level0.yaml")