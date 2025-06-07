import pygame
from game_objects.player import Player
from game_objects.seed import Seed
from game_helpers.button import Button
from game_objects.soil_upgrade import SoilUpgrade
from game_helpers.tilemap_generator import TilemapGenerator
from tilesets.background_tileset import TILE_SIZE, Backpack_tiles, BACKPACK_MAP 

class InventoryScene:
    def __init__(self , screen:pygame.Surface, player: Player , game_manager):
        self.screen = screen
        self.game_manager = game_manager
        self.player = player

        self.background_color = (50,50,80,200)
        self.font_title = pygame.font.Font("assets/fonts/pixelFont.ttf", 60)
        self.font_item = pygame.font.Font("assets/fonts/pixelFont.ttf", 24)
        self.close_button_text_color = (255, 255, 255)

        self.coin_image = pygame.image.load("assets/animated_coins.png").convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, (30, 30))

        self.grid_start_x = 100
        self.grid_start_y = 150
        self.item_slot_size = 64
        self.slot_padding = 10
        self.cols = 5

        self.upgrades = self.game_manager.player.get_backpack_upgrades()
        self.seeds = self.game_manager.player.get_backpack_seeds()

        self.tilemap = TilemapGenerator(BACKPACK_MAP, TILE_SIZE, Backpack_tiles)
    def handle_event(self, event:pygame.event.Event):
        """Handle events for the inventory scene."""
        pass


    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for seed in self.seeds:
            seed.update_hoover_screen(mouse_pos)

        for upgrade in self.upgrades:
            upgrade.update_hoover_screen(mouse_pos)



    def draw(self):
        """Draw the inventory scene."""
        self.tilemap.draw(self.screen)

        # Draw title
        title_surface = self.font_title.render("Backpack Inventory", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(title_surface, title_rect)

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

        current_x = seed_x_start
        current_y = upgrades_y_start + 40

        for i, upgrade in enumerate(self.game_manager.player.get_backpack_upgrades()):
            upgrade.update_position(current_x, current_y)
            upgrade.draw(self.screen) # Draw the upgrade image and name

            current_x += x_offset
            if (i + 1) % max_items_per_row == 0:
                current_x = seed_x_start
                current_y += y_offset
