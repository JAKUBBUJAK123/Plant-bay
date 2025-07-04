import pygame
import random
from game_objects.soil import Soil
class SoilUpgrade:
    """
    Class to handle soil upgrades in a game."""
    def __init__(self , x , y, image_path:str, name , target_size = (50,50) ,description="simple 2x multiplier", upgrade_effect = "multiplier_boost", effect_value = 1):
        """
        Initializes a SoilUpgrade object.

        Args:
            x (int): The x-coordinate for drawing (can be dummy for inventory).
            y (int): The y-coordinate for drawing (can be dummy for inventory).
            image_path (str): The file path to the upgrade image asset.
            name (str): The name of the upgrade (e.g., "Watering Can").
            target_size (tuple[int, int]): The desired width and height to scale the image to.
            upgrade_effect (str): The type of effect this upgrade applies (e.g., "multiplier_boost").
            effect_value (int): The value of the effect (e.g., how much to boost multiplier).
        """
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, target_size)
        self.name = name
        self.upgrade_effect = upgrade_effect
        self.rect = self.image.get_rect(topleft=(x, y))
        self.effect_value = effect_value
        self.original_x = x
        self.original_y = y

        self.is_hovered = False
        self.description = description
        self.popup_font = pygame.font.Font("assets/fonts/pixelFont.ttf", 14)

    
    @classmethod
    def load_upgrades(cls ,data:dict , x =0 , y =0):
        return cls(
            x,
            y,
            data['image'],
            data['name'],
            data['size'],
            data['description'],
            data['upgrade_effect'],
            data['effect_value']
        )


    def draw(self, screen:pygame.Surface):
        """
        Draws the upgrade image on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the upgrade on.
        """
        screen.blit(self.image, self.rect.topleft)


        self.draw_popup_pos(screen)

    def update(self, dt: int):
        # for soil in self.soils:
        #     soil.update(dt)

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

    def update_position(self, new_x, new_y):
        """
        Updates the position of the upgrade.

        Args:
            x (int): The new x-coordinate.
            y (int): The new y-coordinate.
        """
        self.rect.x = new_x
        self.rect.y = new_y

    
    def reset_position(self):
        """
        Resets the position of the upgrade to its original coordinates.
        """
        self.rect.x = self.original_x
        self.rect.y = self.original_y


    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        """Checks if the mouse position is over the item's bounding box."""
        return self.rect.collidepoint(mouse_pos)
    

    def apply_effect(self, target_soil:Soil , soils_list=None):
        """
        Applies the upgrade effect to the target soil.

        Args:
            target_soil (Soil): The soil object to apply the effect to.
        """
        if self.upgrade_effect == "multiplier_boost":
            target_soil.multiplier *= self.effect_value
            target_soil.is_upgraded = True
            target_soil.upgraded_color = (66, 135, 245) 

        elif self.upgrade_effect == "evil_soil":
            target_soil.is_evil = True
            target_soil.multiplier *= self.effect_value
            target_soil.is_upgraded = True
            target_soil.upgraded_color = (120, 0, 0)

        elif self.upgrade_effect == "clover":
            target_soil.is_upgraded = True
            target_soil.is_clover = True
            target_soil.upgraded_color = (0,200,0)

        elif self.upgrade_effect == "holy_soil":
            target_soil.is_holy = True
            target_soil.is_upgraded = True
            target_soil.upgraded_color = (229, 232, 153)
            idx = soils_list.index(target_soil)
            #Left
            if idx > 0:
                left_soil = soils_list[idx - 1]
                left_soil.multiplier *= self.effect_value
            # Right neighbor
            if idx < len(soils_list) - 1:
                right_soil = soils_list[idx + 1]
                right_soil.multiplier *= self.effect_value
        
        elif self.upgrade_effect == "rune_change":
            target_soil.is_upgraded = True
            target_soil.upgraded_color = (232, 147, 35)

        elif self.upgrade_effect == "even_soil":
            target_soil.is_upgraded = True
            target_soil.upgraded_color = (240, 137, 219)
            for index, soil in enumerate(soils_list):
                if index %2 ==0:
                    soil.multiplier *=self.effect_value

        elif self.upgrade_effect == "odd_soil":
            target_soil.is_upgraded = True
            target_soil.upgraded_color = (226, 255, 153)
            for index, soil in enumerate(soils_list):
                if index %2 !=0:
                    soil.multiplier *=self.effect_value

        elif self.upgrade_effect == "remove_upgrade":
            target_soil.is_upgraded = False
            target_soil.is_evil = False
            target_soil.is_clover = False
            target_soil.is_holy = False
            target_soil.upgraded_color = None
        self.play_sound()
    def update_hoover_screen(self , mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw_popup_pos(self , screen):
        if self.is_hovered:
            
            name_surface = self.popup_font.render(self.name, True, (255, 255, 0))
            desc_surface = self.popup_font.render(self.description, True, (255, 255, 255))

            padding = 5
            spacing = 2 

            popup_width = max(name_surface.get_width(), desc_surface.get_width()) + 2 * padding
            popup_height = name_surface.get_height() + spacing + desc_surface.get_height() + 2 * padding

            popup_x = self.rect.centerx - popup_width // 2
            popup_y = self.rect.top - popup_height - 5

            if popup_x < 0:
                popup_x = 0
            if popup_x + popup_width > screen.get_width():
                popup_x = screen.get_width() - popup_width

            popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
            pygame.draw.rect(screen, (30, 30, 30), popup_rect, border_radius=5)
            pygame.draw.rect(screen, (100, 100, 100), popup_rect, 1, border_radius=5)

            screen.blit(name_surface, (popup_x + padding, popup_y + padding))
            screen.blit(desc_surface, (popup_x + padding, popup_y + padding + name_surface.get_height() + spacing))

    def start_shaking(self, duration: int, intensity: int):
        """Starts the shaking effect on the soil."""
        self.is_shaking = True
        self.shake_duration = duration
        self.shake_intensity = intensity
        self.shake_timer = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0

    def play_sound(self, path:str ="music/sound_effects/soil-upgrade.wav"):
        click_sound = pygame.mixer.Sound(path)
        click_sound.set_volume(0.1)
        click_sound.play()
