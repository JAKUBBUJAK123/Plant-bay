import pygame
from game_helpers.button import Button

SCREEN_WIDTH = 832
SCREEN_HEIGHT = 640


class RoundWonScene():
    def __init__(self , game_manager , screen):
        self.game_manager = game_manager;
        self.screen = screen

        self.font_title = pygame.font.Font('assets/fonts/pixelFont.ttf' , 24)
        self.font_text = pygame.font.Font('assets/fonts/pixelFont.ttf' , 20)

        # Popup dimensions
        self.popup_width = SCREEN_WIDTH * 0.6
        self.popup_height = SCREEN_HEIGHT * 0.5
        self.popup_x = (SCREEN_WIDTH - self.popup_width) // 2
        self.popup_y = (SCREEN_HEIGHT - self.popup_height) // 2
        self.popup_rect = pygame.Rect(self.popup_x, self.popup_y, self.popup_width, self.popup_height)

        # Popup background (for fade-in)
        self.overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay_color = (61, 189, 42, 0) # Start fully transparent

        # Animation properties
        self.fade_speed = 3 # Alpha units per frame (adjust for slower/faster)
        self.max_alpha = 150 # Max transparency for overlay (0-255)
        self.title_scale = 0.7 # Start small for pop-in effect
        self.title_scale_speed = 0.01 # How fast title scales in
        self.title_max_scale = 1.2 # Max scale for bounce
        self.title_min_scale = 1.0 # Normal scale
        self.is_scaling_up = True
        self.animation_duration = 1000 # Total duration for initial pop-in (milliseconds)
        self.start_animation_time = pygame.time.get_ticks()

        #shop button
        button_width = 150
        button_height = 50
        button_x = self.popup_x + (self.popup_width - button_width) // 2
        button_y = self.popup_y + self.popup_height - button_height - 30
        self.go_to_shop_button = Button(
            button_x, button_y, button_width, button_height,
            "Go to Shop", (50,150,50), (70, 170, 70), (255,255,255), 20,
        )

    def reset_animation(self):
        self.overlay_color = (0, 0, 0, 0)
        self.title_scale = 0.5
        self.is_scaling_up = True
        self.start_animation_time = pygame.time.get_ticks()

    def handle_event(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.go_to_shop_button.is_clicked(event.pos):
                self.game_manager.change_state(self.game_manager.GAME_STATE_SHOP)
                self.game_manager.shop_scene.generate_products()
                self.game_manager.current_score = 0

    def update(self, dt: int):
        """Updates animation and button hover state."""
        mouse_pos = pygame.mouse.get_pos()
        self.go_to_shop_button.is_hovered = self.go_to_shop_button.rect.collidepoint(mouse_pos)

        # Fade-in overlay
        current_alpha = self.overlay_color[3]
        if current_alpha < self.max_alpha:
            new_alpha = min(self.max_alpha, current_alpha + self.fade_speed * (dt / 16)) # Scale by dt for smooth fade
            self.overlay_color = (self.overlay_color[0], self.overlay_color[1], self.overlay_color[2], int(new_alpha))

        # Title Pop-in/Pulsing animation
        elapsed_time = pygame.time.get_ticks() - self.start_animation_time
        if elapsed_time < self.animation_duration:
            # Initial pop-in
            progress = min(1.0, elapsed_time / (self.animation_duration / 2)) # Fast initial pop
            self.title_scale = 0.5 + (self.title_min_scale - 0.5) * progress
        else:
            # Gentle pulsing after initial pop-in
            if self.is_scaling_up:
                self.title_scale += self.title_scale_speed * (dt / 16)
                if self.title_scale >= self.title_max_scale:
                    self.title_scale = self.title_max_scale
                    self.is_scaling_up = False
            else:
                self.title_scale -= self.title_scale_speed * (dt / 16)
                if self.title_scale <= self.title_min_scale:
                    self.title_scale = self.title_min_scale
                    self.is_scaling_up = True


    def draw(self):
        """Draws the round won popup."""
        self.overlay_surface.fill(self.overlay_color)
        self.screen.blit(self.overlay_surface, (0, 0))
        
        pygame.draw.rect(self.screen, (30, 30, 50), self.popup_rect, border_radius=10)
        pygame.draw.rect(self.screen, (60, 60, 90), self.popup_rect, 3, border_radius=10) 

        # "Round Won!" Title
        title_text = "Round Won!"
        title_surface_original = self.font_title.render(title_text, True, (50,150,50))

        # Scale the title surface
        scaled_width = int(title_surface_original.get_width() * self.title_scale)
        scaled_height = int(title_surface_original.get_height() * self.title_scale)
        title_surface_scaled = pygame.transform.scale(title_surface_original, (scaled_width, scaled_height))

        title_rect = title_surface_scaled.get_rect(center=(SCREEN_WIDTH // 2, self.popup_y + 80))
        self.screen.blit(title_surface_scaled, title_rect)

        #Score and Coins Earned
        score_text = self.font_text.render(f"Score: {self.game_manager.current_score}", True, (255,255,255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, self.popup_y + 150))
        self.screen.blit(score_text, score_rect)

        coins_earned_text = self.font_text.render(f"Coins Earned: {self.game_manager.coins_per_round}", True, (255, 255, 0))
        coins_earned_rect = coins_earned_text.get_rect(center=(SCREEN_WIDTH // 2, self.popup_y + 190))
        self.screen.blit(coins_earned_text, coins_earned_rect)

        self.go_to_shop_button.draw(self.screen)

