import pygame
from game_helpers.button import Button

class StartingScene:
    def __init__(self , screen:pygame.Surface, game_menager):
        self.screen = screen
        self.game_manager = game_menager
        self.background_image = pygame.image.load("assets/backgrounds/backgroundLogo.jpg").convert_alpha()
        self.logo_image = pygame.image.load("assets/logos/logo.png").convert_alpha()
        self.logo_image = pygame.transform.scale(self.logo_image, (120,120))
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width() , self.screen.get_height()) )
        self.font_title = pygame.font.Font("assets/fonts/pixelFont.ttf", 74)
        self.button = Button((self.screen.get_width()-150)//2 ,self.screen.get_height() - 150,150,50, "Play" ,(34, 140, 21) ,(24, 92, 16), (255,255,255) , 24)
        self.options_button = Button((self.screen.get_width()-120)//2 ,self.screen.get_height() - 90,120,50, "Options" , (235, 12, 30), (158, 27, 37) , (255,255,255) , 24)
        self.stats_button = Button((self.screen.get_width()-130) ,self.screen.get_height() - 60,120,50, "Stats" ,(16, 171, 199) ,(22, 129, 148), (255,255,255) , 24)


    def draw(self):
        #background
        self.screen.blit(self.background_image,(0,0))
        #logo
        logo_rect = self.logo_image.get_rect(center=(self.screen.get_width()//2,100))
        self.screen.blit(self.logo_image, logo_rect)
        #text
        title_surface = self.font_title.render("Plant Bay", True, (7, 22, 105))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_surface, title_rect)
        #buttons
        self.button.draw(self.screen)
        self.options_button.draw(self.screen)
        self.stats_button.draw(self.screen)

    def update(self, dt):
        buttons = [self.button, self.options_button, self.stats_button]
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.is_hovered = button.rect.collidepoint(mouse_pos)

        self.button.update(dt)
        self.options_button.update(dt)
        self.stats_button.update(dt)


    def handle_event(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if self.button.is_clicked(mouse_pos):
                    self.button.play_click_sound()
                    self.game_manager.change_state(self.game_manager.GAME_STATE_PLAYING)
                    

                elif self.options_button.is_clicked(mouse_pos):
                    self.button.play_click_sound()
                
                elif self.stats_button.is_clicked(mouse_pos):
                    self.button.play_click_sound()
