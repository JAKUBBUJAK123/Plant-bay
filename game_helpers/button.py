import pygame
import random

class Button:
    """A simple button class."""
    def __init__(self , x, y , width, height, text :str, button_color: tuple  ,button_hover_color:tuple, text_color: tuple , font_size: int, sound_path: str = "music/sound_effects/click.wav"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.Font("assets/fonts/pixelFont.ttf", font_size)
        self.is_hovered = False
        self.button_hover_color = button_hover_color
        self.sound_path = sound_path


    def draw(self, screen:pygame.Surface):
        if hasattr(self, "image") and self.image is not None:
            screen.blit(self.image, self.rect)
        elif self.button_color is not None:
            # Choose color based on hover state
            color = self.button_hover_color if self.is_hovered else self.button_color
            pygame.draw.rect(screen, color, self.rect, border_radius=5)
        # Draw text if needed
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def update(self,dt:int):
        pass
    def is_clicked(self, mouse_pos: tuple) -> bool:
        """Check if the button is clicked."""
        clicked= self.rect.collidepoint(mouse_pos)
        return clicked

    def play_click_sound(self):
        click_sound = pygame.mixer.Sound(self.sound_path)
        click_sound.set_volume(0.1)
        click_sound.play()
    