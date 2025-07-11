import pygame
import random

class Seed:
    """
    Represents a single seed in the player's hand/deck.
    Now uses an image asset.
    """
    def __init__(self, x: int, y: int, image_path: str, name: str = "Basic Seed", target_size: tuple[int, int] = (50, 50) , 
                value: int = 10 , description: str = "A generic seed.", seed_type: str = "basic",
                on_harvest_effect: dict = None, synergy_effect: dict = None):
        """
        Initializes a Seed object.

        Args:
            x (int): The x-coordinate of the top-left corner of the seed's bounding box.
            y (int): The y-coordinate of the top-left corner of the seed's bounding box.
            image_path (str): The file path to the seed image asset.
            name (str): The name of the seed.
            target_size (tuple[int, int]): The desired width and height to scale the image to.
        """
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, target_size)

        self.name = name
        self.value = value
        self.rect = self.image.get_rect(topleft=(x, y))

        self.description = description
        self.popup_font = pygame.font.Font("assets/fonts/pixelFont.ttf", 14)

        self.seed_type = seed_type
        self.on_harvest_effect = on_harvest_effect or {}
        self.synergy_effect = synergy_effect or {}

        # Store original position for snapping back
        self.original_x = x
        self.original_y = y

        self.is_hovered = False


    @classmethod
    def load_seed(cls, data: dict, x: int = 0, y: int = 0):
        return cls(
            x,
            y,
            data['image'],
            data['name'],
            data['size'],
            data['value'],
            data['description'],
            data['seed_type'],
            data.get('on_harvest_effect', {}),
            data.get('synergy_effect', {})
        )

    def draw(self, screen: pygame.Surface):
        """
        Draws the seed using its image asset with its name on the given Pygame screen.

        Args:
            screen (pygame.Surface): The Pygame surface to draw on.
        """
        # Draw the seed image
        screen.blit(self.image, self.rect)

        #Draw popup
        self.draw_popup_pos(screen)

    def update(self , dt):
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


    def reset_position(self):
        """Resets the seed to its original spawning position."""
        self.rect.x = self.original_x
        self.rect.y = self.original_y

    def update_position(self, new_x: int, new_y: int):
        """Updates the seed's top-left position."""
        self.rect.x = new_x
        self.rect.y = new_y

    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        """Checks if the mouse position is over the seed's bounding box."""
        return self.rect.collidepoint(mouse_pos)
    
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