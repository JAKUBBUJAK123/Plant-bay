import pygame
from game_objects.seed import Seed
import random
from game_effects.particles import ParticleSystem

class Soil:
    def __init__(self , x: int, y:int , size:int, image_path:str, default_color: tuple):
        self.image = pygame.image.load(image_path).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (size, size))

        self.rect = self.image.get_rect(topleft=(x, y)) 
        self.original_image = self.image 
        self.original_image_path = image_path
        self.default_color = default_color 
        self.current_color = default_color 
        self.current_image_path = image_path

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

        #Particles
        self.particle_system = ParticleSystem()


    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        self.particle_system.draw(screen)

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

        # Update particles
        self.particle_system.update()

    def spawn_particles(self , count: int , color):
        """Spawns particles at the soil's current position."""
        self.particle_system.emit(self.rect.centerx, self.rect.centery ,count, color)

    def set_color(self, color: tuple[int, int, int]):
        """Changes the current display color of the soil (e.g., when planted)."""
        self.current_color = color

    def set_image(self, image_path: str):
        """Sets a new image for the soil."""
        img = pygame.image.load(image_path).convert_alpha()
        img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
        self.image = img
        self.current_image_path = image_path

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
        self.set_image(self.original_image_path)

    def start_shaking(self, duration: int, intensity: int):
        """Starts the shaking effect on the soil."""
        self.is_shaking = True
        self.shake_duration = duration
        self.shake_intensity = intensity
        self.shake_timer = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        