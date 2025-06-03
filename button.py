import pygame
class Button:
    """A simple button class."""
    def __init__(self , x, y , width, height, text :str, button_color: tuple , text_color: tuple , font_size: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False

    def draw(self, screen:pygame.Surface):
        if hasattr(self, "image") and self.image is not None:
            screen.blit(self.image, self.rect)
        elif self.button_color is not None:
            pygame.draw.rect(screen, self.button_color, self.rect, border_radius=5)
        # Draw text if needed
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos: tuple) -> bool:
        """Check if the button is clicked."""
        return self.rect.collidepoint(mouse_pos)