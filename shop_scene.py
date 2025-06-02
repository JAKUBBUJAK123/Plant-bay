import pygame
from button import Button

class ShopScene:
    """Represents the Shop scene of the game.
    Players are redirected here when they win a round.
    """
    def __init__(self , screen: pygame.Surface , game_menager):
        self.screen = screen
        self.game_manager = game_menager
        self.font_title = pygame.font.Font(None, 74)
        self.font_text = pygame.font.Font(None, 36)
        self.background_color = (100, 100, 150)

        self.item_name = "Big seed"
        self.item_price = 100
        self.buy_button = Button(self.screen.get_width() // 2 - 100, 
                                 self.screen.get_height() // 2 + 50, 200,50, "buy" ,
                                   (50, 150, 50), (255, 255, 255), 30)
        
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(f"Buying item {self.item_name} for {self.item_price} coins.")
                self.game_manager.change_state("PLAYING")
                self.game_manager.reset_round()

    def draw(self):
        self.screen.fill(self.background_color)

        title_surface = self.font_title.render("The Seed Shop", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_surface, title_rect)
        
        price_surface = self.font_text.render(f"Price {self.item_price} coins", True, (255, 255, 255))
        price_rect = price_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(price_surface, price_rect)

        self.buy_button.draw(self.screen)

    def update(self):
        pass