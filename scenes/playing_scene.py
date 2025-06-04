# scenes/playing_scene.py
import pygame
from button import Button
from game_objects.soil import Soil


TEXT_COLOR = (255, 255, 255)
BG_COLOR = (0, 128, 0)

class PlayingScene:
    """
    Manages the drawing and event handling for the main game playing screen.
    """
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game_manager = game_manager


        self.play_hand_button = None # This will be set by GameInitializer

        # Fonts (can be passed from game_manager or defined here if specific)
        self.font_score = pygame.font.Font(None, 30)

    def handle_event(self, event):
        """Handles events specific to the playing scene (e.g., button clicks)."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.play_hand_button and self.play_hand_button.is_clicked(event.pos):
                self.game_manager.round_manager.play_hand()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.play_hand_button.is_hovered = self.play_hand_button.rect.collidepoint(mouse_pos)
        for soil in self.game_manager.soils:
            soil.update(self.game_manager.clock.get_time())

    def draw(self):
        """Draws elements specific to the PLAYING state."""
        self.screen.fill(BG_COLOR) # Ensure background is drawn

        # Draw soil plots
        for soil in self.game_manager.soils:
            soil.draw(self.screen)

        # Draw seeds in hand
        for seed in self.game_manager.seeds_in_hand:
            seed.draw(self.screen)

        # Draw UI elements
        if self.play_hand_button:
            self.play_hand_button.draw(self.screen)

        # Draw player's coins
        coins_text = self.font_score.render(f"Coins: {self.game_manager.player.get_coins()}", True, (255, 255, 0))
        self.screen.blit(coins_text, (30, 70))

        # Draw Score Goal
        score_goal_text = self.font_score.render(f"Goal: {self.game_manager.score_goal}", True, TEXT_COLOR)
        self.screen.blit(score_goal_text, (30, self.screen.get_height() // 2 - 50))

        # Draw Current Score
        current_score_text = self.font_score.render(f"Score: {self.game_manager.current_score}", True, TEXT_COLOR)
        self.screen.blit(current_score_text, (30, self.screen.get_height() // 2))

        # Draw Predicted Score
        predicted_score_text = self.font_score.render(f"Predicted: {self.game_manager.predicted_score}", True, TEXT_COLOR)
        self.screen.blit(predicted_score_text, (30, self.screen.get_height() // 2 + 30))
