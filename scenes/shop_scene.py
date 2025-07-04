import pygame
from game_helpers.button import Button
from game_objects.player import Player
from game_objects.seed import Seed
import random
from game_objects.soil_upgrade import SoilUpgrade
from game_helpers.tilemap_generator import TilemapGenerator
from tilesets.background_tileset import TILE_SIZE, Shop_tiles, SHOP_MAP
from game_helpers.json_loader import load_json_file

class ShopScene:
    """Represents the Shop scene of the game.
    Players are redirected here when they win a round.
    """
    def __init__(self , screen: pygame.Surface , game_menager , player:Player , shop_item_size: tuple =(80,80)):
        self.screen = screen
        self.game_manager = game_menager
        self.player = player
        self.font_title = pygame.font.Font("assets/fonts/pixelFont.ttf", 74)
        self.font_text =pygame.font.Font("assets/fonts/pixelFont.ttf", 30)
        self.background_color = (100, 100, 150)
        self.tilemap = TilemapGenerator(SHOP_MAP, TILE_SIZE, Shop_tiles)

       #--- Shop Items ---
        self.shop_item_size = shop_item_size
        self.products_on_display = []
        self.num_product_slots = 3
        self.roll_cost = 10
        
        #--- Coin Image ---
        self.coin_image = pygame.image.load("assets/animated_coins.png").convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, (30, 30))

        #--- Shop items available---
        self.available_shop_items = {
            "seed": {"class": Seed, "image": "assets/seeds/seed.png", "base_value": 10, "price_multiplier": 3},
            "watering_can": {"class": SoilUpgrade, "image": "assets/upgrades/watering_can.png", "name": "Watering Can", "effect_value": 1, "base_price": 75}
        }

        #--Shop UI---
        self.next_round_button = Button(20 , self.screen.get_height() - 70 , 180 , 50 ,
                                        "Next Round", (50,150,50),(0, 200, 0) ,(255,255,255), 24)
        self.roll_button = Button(20 , self.screen.get_height() - 140 , 180 , 50 ,
                                        "Roll", (150,50,50), (200, 80, 80),(255,255,255), 24, "music/sound_effects/money-spend.mp3")
        self.generate_products()


    def generate_products(self):
        """Generates random products for the shop."""

        self.products_on_display.clear()
        seed_y_start = self.screen.get_height() // 2 - self.shop_item_size[1] // 2 - 90
        x_padding = 50
        total_width_needed = (self.num_product_slots * self.shop_item_size[0]) + \
                             ((self.num_product_slots - 1) * x_padding)
        start_x = (self.screen.get_width() - total_width_needed) // 2

        #load products
        all_seeds = load_json_file('seed_list.json')
        all_upgrades = load_json_file('upgrades_list.json')

        shop_items = []
        for seed_data in all_seeds.values():
            shop_items.append(('seed', seed_data))
        for upgrade_data in all_upgrades.values():
            shop_items.append(('upgrade', upgrade_data))

        chosen_items = random.choices(shop_items, k=self.num_product_slots)

        for i, (item_type, item_data) in enumerate(chosen_items):
            item_x = start_x + (i * (self.shop_item_size[0] + x_padding))
            if item_type == "seed":
                product = Seed.load_seed(item_data, x=item_x, y=seed_y_start)
                product.price = product.value * 3
                
            elif item_type == "upgrade":
                product = SoilUpgrade.load_upgrades(item_data, x=item_x, y=seed_y_start)
                product.price = 75

            product.start_shaking(100 , 5)
            self.products_on_display.append(product)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                #--- Handle Buying Products ---
                for i, product_on_display in enumerate(self.products_on_display):
                    if hasattr(product_on_display, "buy_button") and product_on_display.buy_button.is_clicked(mouse_pos):
                        if self.player.get_coins() >= product_on_display.price:
                            self.player.remove_coins(product_on_display.price)
                            if isinstance(product_on_display, Seed):
                                self.player.add_seed(
                                    Seed(0, 0, product_on_display.image_path, product_on_display.name, value=product_on_display.value ,description=product_on_display.description)
                                )
                            elif isinstance(product_on_display, SoilUpgrade):
                                self.player.add_upgrade(
                                    SoilUpgrade(0, 0, product_on_display.image_path, product_on_display.name,
                                                upgrade_effect=product_on_display.upgrade_effect,
                                                effect_value=product_on_display.effect_value ,description=product_on_display.description)
                                )
                            print(f"Bought {product_on_display.name} for {product_on_display.price} coins.")
                            product_on_display.buy_button.play_click_sound()
                            self.products_on_display.pop(i)
                        else:
                            print("Not enough coins!")
                        break
            # --- Handle Roll Button ---
                if self.roll_button.is_clicked(mouse_pos):
                    if self.game_manager.player.get_coins() >= self.roll_cost:
                        self.game_manager.player.remove_coins(self.roll_cost)
                        self.generate_products()
                        self.roll_button.play_click_sound()
                        print("Shop rolled!")
                    else:
                        print("Not enough coins to roll the shop!")
                # --- Handle Next Round Button ---
                if self.next_round_button.is_clicked(mouse_pos):
                    self.game_manager.change_state(self.game_manager.GAME_STATE_PLAYING)
                    self.next_round_button.play_click_sound()
                    self.game_manager.round_manager.next_round()


    def draw(self):
        self.tilemap.draw(self.screen)

        title_surface = self.font_title.render("The Seed Shop", True, (7, 22, 105))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # Draw player coin
        coin_x =  30
        coin_y = self.screen.get_height() //2 -100
        self.screen.blit(self.coin_image, (coin_x, coin_y))
        coins_text = self.font_text.render(f"x {self.game_manager.player.get_coins()}", True, (255, 255, 0))
        self.screen.blit(coins_text, (coin_x +50, coin_y  + 5))

        # Draw shop products
        for product in self.products_on_display:
            product.draw(self.screen)

            buy_button_width = 100
            buy_button_height = 30
            buy_button_x = product.rect.centerx - buy_button_width // 2
            buy_button_y = product.rect.bottom + 30

            product.buy_button = Button(
                buy_button_x,
                buy_button_y,
                buy_button_width,
                buy_button_height,
                f"Buy ({product.price}$)",
                (0, 90, 0),
                (0, 150, 0),
                (255, 255, 255),
                24,
                "music/sound_effects/money-spend.mp3"
            )
            product.buy_button.draw(self.screen)



        # Draw control buttons
        self.roll_button.draw(self.screen)
        self.next_round_button.draw(self.screen)

    def update(self , dt):
        buttons = [self.roll_button, self.next_round_button]
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.is_hovered = button.rect.collidepoint(mouse_pos)

        # --- Item Popup ---
        for product in self.products_on_display:
            product.update_hoover_screen(mouse_pos)
            product.update(dt)
            
        #--- buttons ---
        self.roll_button.update(dt)
        self.next_round_button.update(dt)