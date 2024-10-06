import os

from EmotionEngine.EmEngine import EmEngine

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.realpath(__file__))

    engineInstance = EmEngine(
        working_directory=current_directory,
        window_width=1100,
        window_height=700,
        game_title="Emotion Pong",
    )

    engineInstance.initialize()
    engineInstance.load_level("level0.emlvl")

    engineInstance.main_loop()
