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
        self.is_upgraded = False
        self.upgraded_color = None
        self.is_evil = False
        self.is_clover = False
        self.is_holy = False

        self.flat_bonus = 1
        self.crit_chance = 0.0
        self.return_chance = 0.0

        self.next_plant_buff: dict | None = None

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

        #text popup
        self.popup_font = pygame.font.Font("assets/fonts/pixelFont.ttf", 14)
        self.is_hovered = False
        

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        self.draw_popup_pos(screen)

        if self.is_upgraded and self.upgraded_color:
            overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            overlay.fill((*self.upgraded_color, 100))
            screen.blit(overlay, self.rect.topleft)

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
        if not self.is_planted:
            self.is_planted = True
            self.planted_seed  = seed_object
            self.play_sound()

    def harvest_seed(self, player=None) :
        if self.is_planted and self.planted_seed:
            base_value = self.planted_seed.value
            current_value = base_value * self.flat_bonus
            harvested_value = current_value * self.multiplier

            effect = getattr(self.planted_seed, "on_harvest_effect", {})
            retrigger_count = 1
            if effect:
                if effect.get("type") == "retrigger":
                    retrigger_count = effect.get("value", 0)

            total_value = 0
            for i in range(retrigger_count):
                if effect and effect.get("type") != "retrigger":
                    if effect.get("type") == "add_coins" and player is not None:
                        coins_to_add = effect.get("value", 0)
                        player.add_coins(coins_to_add)
                    elif effect.get("type") == "self_duplicate_chance" and player is not None:
                        if random.random() < effect.get("value", 0):
                            player.add_seed(self.planted_seed)
                total_value += harvested_value

            return total_value
        return 0
    
    def predict_harvest_value(self):
        if self.is_planted and self.planted_seed:
            base_value = self.planted_seed.value
            current_value = base_value * self.flat_bonus
            predicted_value = current_value * self.multiplier
            return predicted_value
        return 0

    def calculate_synergy_bonus(self, soils, index):
        seed = self.planted_seed
        synergy = getattr(seed, "synergy_effect", {})
        bonus = 0
        if synergy:
            if synergy.get("type") == "adjacent_same_type_value_boost":
                if index < len(soils) - 1:
                    neighbor = soils[index + 1]
                    if neighbor.is_planted and neighbor.planted_seed and neighbor.planted_seed.seed_type == seed.seed_type:
                        bonus += synergy.get("value", 0)
            elif synergy.get("type") == "adjacent_type_value_boost":
                target_type = synergy.get("target_seed_type")
                per_match = synergy.get("bonus_per_match", 0)
                for neighbor_idx in [index-1, index+1]:
                    if 0 <= neighbor_idx < len(soils):
                        neighbor = soils[neighbor_idx]
                        if neighbor.is_planted and neighbor.planted_seed and neighbor.planted_seed.seed_type == target_type:
                            bonus += per_match
        return bonus

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
        
    def update_hoover_screen(self , mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def play_sound(self):
        click_sound = pygame.mixer.Sound("music/sound_effects/plant.wav")
        click_sound.set_volume(0.1)
        click_sound.play()

    def draw_popup_pos(self , screen):
        if self.is_hovered:
            
            text_surface = self.popup_font.render(f'{self.multiplier}X multi', True, (255, 255, 255))

            
            padding = 5
            popup_width = text_surface.get_width() + 2 * padding
            popup_height = text_surface.get_height() + 2 * padding

            
            popup_x = self.rect.centerx - popup_width // 2
            popup_y = self.rect.top - popup_height - 5

            if popup_x < 0:
                popup_x = 0
            if popup_x + popup_width > screen.get_width():
                popup_x = screen.get_width() - popup_width

            popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
            pygame.draw.rect(screen, (30, 30, 30), popup_rect, border_radius=5) 
            pygame.draw.rect(screen, (100, 100, 100), popup_rect, 1, border_radius=5) 

            screen.blit(text_surface, (popup_x + padding, popup_y + padding))