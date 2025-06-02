import pygame
from player import Player
from seed import Seed
from button import Button

class InventoryScene:
    def __init__(self , screen:pygame.Surface, player: Player , game_manager):
        self.screen = screen
        self.game_manager = game_manager
        self.player = player

        self.background_color = (50,50,80,200)
        self.font_title = pygame.font.Font(None, 60)
        self.font_item = pygame.font.Font(None, 24)
        self.close_button_text_color = (255, 255, 255)

        self.grid_start_x = 100
        self.grid_start_y = 150
        self.item_slot_size = 64
        self.slot_padding = 10
        self.cols = 5

    def handle_event(self, event:pygame.event.Event):
        """Handle events for the inventory scene."""
        pass


    def update(self):
        pass


    def draw(self):
        """Draw the inventory scene."""
        self.screen.fill(self.background_color)

        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill(self.background_color)
        self.screen.blit(overlay, (0, 0))

        # Draw inventory title
        title_surface = self.font_title.render("Backpack Inventory", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(title_surface, title_rect)


        # Draw backpack contents in a grid
        for i, seed in enumerate(self.player.backpack_seeds):
            row = i // self.cols
            col = i % self.cols
            x = self.grid_start_x + col * (self.item_slot_size + self.slot_padding)
            y = self.grid_start_y + row * (self.item_slot_size + self.slot_padding)

            # Draw slot background (optional, but good for clarity)
            slot_rect = pygame.Rect(x, y, self.item_slot_size, self.item_slot_size)
            pygame.draw.rect(self.screen, (80, 80, 100), slot_rect, border_radius=3) # Slot background

            # Draw seed image (scaled to slot size)
            scaled_seed_image = pygame.transform.scale(seed.image, (self.item_slot_size - 10, self.item_slot_size - 10)) # Slightly smaller than slot
            seed_image_rect = scaled_seed_image.get_rect(center=slot_rect.center)
            self.screen.blit(scaled_seed_image, seed_image_rect)
