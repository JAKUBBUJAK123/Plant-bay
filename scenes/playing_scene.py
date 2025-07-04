# scenes/playing_scene.py
import pygame
from game_helpers.button import Button
from game_objects.soil import Soil
from game_helpers.tilemap_generator import TilemapGenerator
from tilesets.background_tileset import TILE_SIZE , Main_tiles, GAME_MAP

TEXT_COLOR = (255, 255, 255)
BG_COLOR = (0, 128, 0)

class PlayingScene:
    """
    Manages the drawing and event handling for the main game playing screen.
    """
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game_manager = game_manager

        self.tilemap_generator = TilemapGenerator(GAME_MAP ,TILE_SIZE , Main_tiles)
        self.play_hand_button = None

        # Fonts (can be passed from game_manager or defined here if specific)
        self.font_score = pygame.font.Font("assets/fonts/pixelFont.ttf", 30)

        #---coin ---
        self.coin_image = pygame.image.load("assets/animated_coins.png").convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, (30, 30))


    def handle_event(self, event):
        """Handles events specific to the playing scene (e.g., button clicks)."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.play_hand_button and self.play_hand_button.is_clicked(event.pos):
                self.game_manager.round_manager.play_hand()
                self.play_hand_button.play_click_sound()

    def update(self ,dt):
        mouse_pos = pygame.mouse.get_pos()
        self.play_hand_button.is_hovered = self.play_hand_button.rect.collidepoint(mouse_pos)
        self.play_hand_button.update(dt)
        for soil in self.game_manager.soils:
            soil.update(self.game_manager.clock.get_time())

        # --- Item Popup ---
        for seed in self.game_manager.seeds_in_hand:
            seed.update_hoover_screen(mouse_pos)

        for soil in self.game_manager.soils:
            soil.update_hoover_screen(mouse_pos)


    def draw(self):
        """Draws elements specific to the PLAYING state."""
        self.tilemap_generator.draw(self.screen)


        # Draw soil plots
        for soil in self.game_manager.soils:
            soil.draw(self.screen)

        # Draw seeds in hand
        for seed in self.game_manager.seeds_in_hand:
            seed.draw(self.screen)

        # Draw UI elements
        if self.play_hand_button:
            self.play_hand_button.draw(self.screen)

        # Draw Score Goal
        score_goal_text = self.font_score.render(f"Goal: {self.game_manager.score_goal}", True, TEXT_COLOR)
        self.screen.blit(score_goal_text, (30, self.screen.get_height() // 2 - 50))

        # Draw Current Score
        current_score_text = self.font_score.render(f"Score: {self.game_manager.current_score}", True, TEXT_COLOR)
        self.screen.blit(current_score_text, (30, self.screen.get_height() // 2))

        # Draw Predicted Score
        predicted_score_text = self.font_score.render(f"Predicted: {self.game_manager.predicted_score}", True, TEXT_COLOR)
        self.screen.blit(predicted_score_text, (30, self.screen.get_height() // 2 + 30))

        # Draw coins
        coin_x =  30
        coin_y = self.screen.get_height() //2 -100
        self.screen.blit(self.coin_image, (coin_x, coin_y))
        coins_text = self.font_score.render(f"x {self.game_manager.player.get_coins()}", True, (255, 255, 0))
        self.screen.blit(coins_text, (coin_x +50, coin_y  + 5))

