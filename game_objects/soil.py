import pygame
from game_objects.seed import Seed
import random

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

        #Shaking properties
        self.is_shaking = False
        self.shake_duration = 0 
        self.shake_intensity = 0 
        self.shake_offset_x = 0 
        self.shake_offset_y = 0
        self.shake_timer = 0 
        self.original_x = x 
        self.original_y = y

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

        if self.is_planted:
            s = pygame.Surface(self.rect.size, pygame.SRCALPHA) # Create a transparent surface
            s.fill(self.current_color + (100,)) # Fill with color + alpha (transparency)
            screen.blit(s, self.rect)

    def update(self, dt: int):
        #Shaking logic
        if self.is_shaking:
            self.shake_timer += dt
            if self.shake_timer >= self.shake_duration:
                self.is_shaking = False
                self.shake_offset_x = 0
                self.shake_offset_y = 0
                self.rect.topleft = (self.original_x, self.original_y)
            else:
                current_intensity = self.shake_intensity * (1 - self.shake_timer / self.shake_duration)
                self.shake_offset_x = random.uniform(-current_intensity, current_intensity)
                self.shake_offset_y = random.uniform(-current_intensity, current_intensity)
                self.rect.topleft = (self.original_x + self.shake_offset_x, self.original_y + self.shake_offset_y)


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

    def start_shaking(self, duration: int, intensity: int):
        """Starts the shaking effect on the soil."""
        self.is_shaking = True
        self.shake_duration = duration
        self.shake_intensity = intensity
        self.shake_timer = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        