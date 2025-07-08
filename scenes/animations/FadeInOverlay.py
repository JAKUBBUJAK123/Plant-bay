import pygame

class FaseInOverlay:
    def __init__(self, width, height, color=(0, 0, 0), max_alpha=180, fade_speed=3):
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.base_color = color
        self.max_alpha = max_alpha
        self.fade_speed = fade_speed
        self.alpha = 0

    def reset(self):
        self.alpha = 0

    def update(self, dt):
        if self.alpha < self.max_alpha:
            self.alpha = min(self.max_alpha, self.alpha + self.fade_speed * (dt / 16))

    def draw(self, screen):
        self.surface.fill((*self.base_color, int(self.alpha)))
        screen.blit(self.surface, (0, 0))