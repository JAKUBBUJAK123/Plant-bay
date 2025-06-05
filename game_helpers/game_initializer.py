import pygame
from game_objects.soil import Soil
from game_helpers.button import Button

SOIL_SIZE = 80
SOIL_PADDING = 20
SOIL_DEFAULT_COLOR = (139, 69, 19)

class GameInitializer:
    """Handles the initial setup of game objects and static UI elements."""
    def __init__(self , game_manager):
        self.game_manager = game_manager

    def initialize_game_objects(self):
        """Initializes soil plots."""
        total_plots_width = (self.game_manager.round_manager.NUM_SOILS * SOIL_SIZE) + \
                            ((self.game_manager.round_manager.NUM_SOILS - 1) * SOIL_PADDING)
        start_x = (self.game_manager.screen.get_width() - total_plots_width) // 2
        plot_y = SOIL_PADDING + 20

        for i in range(self.game_manager.round_manager.NUM_SOILS):
            x = start_x + (i * (SOIL_SIZE + SOIL_PADDING))
            soil = Soil(x, plot_y, SOIL_SIZE, "assets/soil.png", SOIL_DEFAULT_COLOR)
            self.game_manager.soils.append(soil)

    def initialize_ui_elements(self):
        """Initializes UI elements like the 'Play Hand' button."""
        button_width = 150
        button_height = 50
        button_x = self.game_manager.screen.get_width() - button_width - 30
        button_y = self.game_manager.screen.get_height() // 2 - button_height // 2

        self.game_manager.playing_scene.play_hand_button = Button(
            button_x, button_y, button_width, button_height,
            "Play Hand", (50,150,50), (0, 150, 0),(255,255,255), 24
        )