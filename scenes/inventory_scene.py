import pygame
from game_objects.player import Player
from game_objects.seed import Seed
from button import Button
from game_objects.soil_upgrade import SoilUpgrade

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
        s = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        s.fill(self.background_color)
        self.screen.blit(s, (0, 0))

        # Draw title
        title_surface = self.font_title.render("Backpack Inventory", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(title_surface, title_rect)

        # Draw coins (for consistency)
        coins_text = self.font_item.render(f"Coins: {self.game_manager.player.get_coins()}", True, (255, 255, 0))
        self.screen.blit(coins_text, (50, 50))

        # --- Display Seeds ---
        seeds_label = self.font_item.render("Seeds:", True, (255, 255, 255))
        self.screen.blit(seeds_label, (50, 150))

        seed_x_start = 50
        seed_y_start = 190
        x_offset = self.item_slot_size + 10 # Spacing
        y_offset = self.item_slot_size + 30 # Spacing for text below

        current_x = seed_x_start
        current_y = seed_y_start
        max_items_per_row = (self.screen.get_width() - seed_x_start * 2) // x_offset

        for i, seed in enumerate(self.game_manager.player.get_backpack_seeds()):
            seed.update_position(current_x, current_y)
            seed.draw(self.screen)

            current_x += x_offset
            if (i + 1) % max_items_per_row == 0:
                current_x = seed_x_start
                current_y += y_offset

        # --- Display Upgrades ---
        upgrades_label = self.font_item.render("Upgrades:", True, (255, 255, 255))

        upgrades_y_start = current_y + y_offset + 30 if self.game_manager.player.get_backpack_seed_count() > 0 else seed_y_start + y_offset + 30
        self.screen.blit(upgrades_label, (50, upgrades_y_start))

        current_x = seed_x_start # Reset x for upgrades
        current_y = upgrades_y_start + 40 # Start drawing upgrades below label

        for i, upgrade in enumerate(self.game_manager.player.get_backpack_upgrades()):
            upgrade.update_position(current_x, current_y)
            upgrade.draw(self.screen) # Draw the upgrade image and name

            current_x += x_offset
            if (i + 1) % max_items_per_row == 0:
                current_x = seed_x_start
                current_y += y_offset
