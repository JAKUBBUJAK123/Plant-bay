import pygame
from game_helpers.button import Button
from game_helpers.sound_with_pith import play_sound_with_pitch
from scenes.animations.FadeInOverlay import FaseInOverlay


class Options_scene:
    def __init__(self, screen:pygame.Surface, game_manager):
        self.screen = screen
        self.game_manager = game_manager
        self.music_volume = 1.0
        self.sound_effects_volume = 1.0
        self.cancel_button = Button((self.screen.get_width() - 100) // 2,(self.screen.get_height())//2 + 110,100 ,30, "cancel" , (135, 148, 138) , (86, 94, 88) , (255,255,255), 24)
        self.save_button = Button((self.screen.get_width() - 100) // 2,(self.screen.get_height()+20)//2 + 60,100 ,30, "save" , (34, 140, 21) ,(24, 92, 16), (255,255,255) , 24)
    
        #animation
        self.fadeInOverlayAnimation = FaseInOverlay(self.screen.get_width(), self.screen.get_height(),(0,0,0), 180, 3)

    def change_music_volume(self, volume):
        self.music_volume = volume

    def change_sound_effects_volume(self, volume):
        self.sound_effects_volume = volume

    def update(self, dt):
        self.fadeInOverlayAnimation.update(dt)
        # Button hover logic
        mouse_pos = pygame.mouse.get_pos()
        self.cancel_button.is_hovered = self.cancel_button.rect.collidepoint(mouse_pos)
        self.save_button.is_hovered = self.save_button.rect.collidepoint(mouse_pos)


    def draw(self):
        self.fadeInOverlayAnimation.draw(self.screen)

        # Draw popup
        popup_width = self.screen.get_width() * 0.6
        popup_height = self.screen.get_height() * 0.5
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.screen, (30, 30, 50), popup_rect, border_radius=10)
        pygame.draw.rect(self.screen, (60, 60, 90), popup_rect, 3, border_radius=10)

        # Title
        font_title = pygame.font.Font('assets/fonts/pixelFont.ttf', 32)
        title_surface = font_title.render("Options", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, popup_y + 50))
        self.screen.blit(title_surface, title_rect)

        #sound
        font_text = pygame.font.Font('assets/fonts/pixelFont.ttf', 16)
        sound_surface = font_text.render("sound volume" , True , (255,255,255))
        sound_surface_rect = sound_surface.get_rect(center=(self.screen.get_width()//2 , popup_y+ 120) )
        self.screen.blit(sound_surface,sound_surface_rect)
                
        sound_effects_surface = font_text.render("sound effects volume" , True , (255,255,255))
        sound_effects_surface_rect = sound_surface.get_rect(center=(self.screen.get_width()//2 - 35 , popup_y+ 180) )
        self.screen.blit(sound_effects_surface,sound_effects_surface_rect)

        # Draw buttons
        self.cancel_button.draw(self.screen)
        self.save_button.draw(self.screen)


    def handle_event(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.cancel_button.is_clicked(event.pos):
                self.cancel_button.play_click_sound()
                self.fadeInOverlayAnimation.reset()
                self.game_manager.change_state(self.game_manager.GAME_STATE_STARTING_SCREEN)
            elif self.save_button.is_clicked(event.pos):
                self.save_button.play_click_sound()