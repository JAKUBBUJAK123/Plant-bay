# scenes/lose_scene.py
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TEXT_COLOR = (255, 255, 255)

class LoseScene:
    """
    Manages the drawing and event handling for the game over/lose screen.
    """
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game_manager = game_manager

        # Fonts
        self.font_game_over = pygame.font.Font(None, 100)
        self.font_score = pygame.font.Font(None, 30)

    def handle_event(self, event):
        """Handles events specific to the lose scene (currently nothing actionable like a retry button)."""
        pass

    def update(self):
        """Updates logic for the lose scene."""
        pass # No dynamic updates for lose screen currently

    def draw(self):
        """Draws the game over/lose screen."""
        self.screen.fill((0, 0, 0)) # Black background for game over

        game_over_text = self.font_game_over.render("GAME OVER!", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(game_over_text, game_over_rect)

        # Use game_manager.current_score for final score
        final_score_text = self.font_score.render(f"Final Score: {self.game_manager.current_score}", True, TEXT_COLOR)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(final_score_text, final_score_rect)