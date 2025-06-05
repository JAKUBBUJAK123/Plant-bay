import pygame
import os

class TilemapGenerator:
    def __init__(self, tile_map: list[list[int]], tile_size: int, tile_types: dict):
        self.tile_map = tile_map
        self.tile_size = tile_size
        self.tiles = {}

        self.load_tiles(tile_types)

    def load_tiles(self, tile_types: dict):
        """Loads all unique tile images from specified paths."""
        for tile_id, filename in tile_types.items():
            image = pygame.image.load(filename).convert_alpha()
            self.tiles[tile_id] = pygame.transform.scale(image, (self.tile_size, self.tile_size))

    def draw(self, screen: pygame.Surface):
        """Draws the tilemap onto the given screen."""
        for row_idx, row in enumerate(self.tile_map):
            for col_idx, tile_id in enumerate(row):
                if tile_id in self.tiles:
                    tile_image = self.tiles[tile_id]
                    screen.blit(tile_image, (col_idx * self.tile_size, row_idx * self.tile_size))