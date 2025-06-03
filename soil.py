import pygame
from seed import Seed

class Soil:
    def __init__(self , x: int, y:int , size:int, image_path:str, default_color: tuple):
        self.image = pygame.image.load(image_path).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (size, size))

        self.rect = self.image.get_rect(topleft=(x, y)) 
        self.original_image = self.image 
        self.default_color = default_color 
        self.current_color = default_color 

        self.is_planted = False
        self.planted_seed = None
        self.multiplier = 1.0

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

        if self.is_planted:
            s = pygame.Surface(self.rect.size, pygame.SRCALPHA) # Create a transparent surface
            s.fill(self.current_color + (100,)) # Fill with color + alpha (transparency)
            screen.blit(s, self.rect)

    def set_color(self, color: tuple[int, int, int]):
        """Changes the current display color of the soil (e.g., when planted)."""
        self.current_color = color

    def reset_color(self):
        """Resets the soil to its default color."""
        self.current_color = self.default_color

    def plant_seed(self, seed_object:Seed):
        self.is_planted = True
        self.planted_seed  = seed_object

    def reset_soil(self):
        """Resets the soil to its initial state."""
        self.is_planted = False
        self.planted_seed = None
        self.current_color = self.default_color
        