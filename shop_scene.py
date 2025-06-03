import pygame
from button import Button
from player import Player
from seed import Seed
import random
from soil_upgrade import SoilUpgrade

class ShopScene:
    """Represents the Shop scene of the game.
    Players are redirected here when they win a round.
    """
    def __init__(self , screen: pygame.Surface , game_menager , player:Player , shop_item_size: tuple =(80,80)):
        self.screen = screen
        self.game_manager = game_menager
        self.font_title = pygame.font.Font(None, 74)
        self.font_text = pygame.font.Font(None, 36)
        self.background_color = (100, 100, 150)

        #--- Shop Items ---
        self.shop_item_size = shop_item_size
        self.products_on_display = []
        self.num_product_slots = 3
        self.roll_cost = 10

        #--- Shop items available---
        self.available_shop_items = {
            "seed": {"class": Seed, "image": "assets/seed.jpg", "base_value": 10, "price_multiplier": 3},
            "watering_can": {"class": SoilUpgrade, "image": "assets/watering_can.png", "name": "Watering Can", "effect_value": 1, "base_price": 75}
        }

        #--Shop UI---
        self.next_round_button = Button(20 , self.screen.get_height() - 70 , 180 , 50 , 
                                        "Next Round", (50,150,50), (255,255,255), 24)
        self.roll_button = Button(20 , self.screen.get_height() - 140 , 180 , 50 ,
                                        "Roll", (150,50,50), (255,255,255), 24)
        #backpack
        self.backpack_icon_image = pygame.image.load("assets/backpack.png").convert_alpha()
        self.backpack_icon_image = pygame.transform.scale(self.backpack_icon_image, (60, 60))
        self.backpack_icon_rect = self.backpack_icon_image.get_rect()
        self.backpack_icon_rect.x = self.screen.get_width() - self.backpack_icon_rect.width - 20
        self.backpack_icon_rect.y = self.screen.get_height() - self.backpack_icon_rect.height - 20
        self.generate_products()


    def generate_products(self):
        """Generates random products for the shop."""

        self.products_on_display.clear()
        seed_y_start = self.screen.get_height() // 2 - self.shop_item_size[1] // 2 - 50
        x_padding = 50
        total_width_needed = (self.num_product_slots * self.shop_item_size[0]) + \
                             ((self.num_product_slots - 1) * x_padding)
        start_x = (self.screen.get_width() - total_width_needed) // 2

        for i in range(self.num_product_slots):
            item_type = random.choice(list(self.available_shop_items.keys()))
            item_info = self.available_shop_items[item_type]

            item_x = start_x + (i * (self.shop_item_size[0] + x_padding))

            if item_type == "seed":
                value = random.randint(item_info["base_value"], item_info["base_value"] * 3)
                price = value * item_info["price_multiplier"]
                product = Seed(
                    item_x, seed_y_start,
                    item_info["image"],
                    f"Seed {value}", # Name based on value
                    target_size=self.shop_item_size,
                    value=value
                )
                product.price = price
            elif item_type == "watering_can":
                price = item_info["base_price"]
                product = SoilUpgrade(
                    item_x, seed_y_start,
                    item_info["image"],
                    item_info["name"],
                    target_size=self.shop_item_size,
                    upgrade_effect=item_info["effect_value"]
                )
                product.price = price # Add price attribute to upgrade object

            self.products_on_display.append(product)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                #--- Handle Buying Products ---
                for i, seed_on_display in enumerate(self.products_on_display):
                    if hasattr(seed_on_display, "buy_button_rect") and seed_on_display.buy_button_rect.collidepoint(mouse_pos):
                        if self.game_manager.player.get_coins() >= seed_on_display.price:
                            self.game_manager.player.remove_coins(seed_on_display.price)
                            # Add to backpack depending on type
                            if isinstance(seed_on_display, Seed):
                                self.game_manager.player.add_seed(
                                    Seed(0, 0, seed_on_display.image_path, seed_on_display.name, value=seed_on_display.value)
                                )
                            elif isinstance(seed_on_display, SoilUpgrade):
                                self.game_manager.player.add_upgrade(
                                    SoilUpgrade(0, 0, seed_on_display.image_path, seed_on_display.name,
                                                upgrade_effect=seed_on_display.upgrade_effect,
                                                effect_value=getattr(seed_on_display, "effect_value", 1))
                                )
                            print(f"Bought {seed_on_display.name} for {seed_on_display.price} coins.")
                            self.products_on_display.pop(i) # Remove item from shop display
                        else:
                            print("Not enough coins!")
                        break
            # --- Handle Roll Button ---
                if self.roll_button.is_clicked(mouse_pos):
                    if self.game_manager.player.get_coins() >= self.roll_cost:
                        self.game_manager.player.remove_coins(self.roll_cost)
                        self.generate_products()
                        print("Shop rolled!")
                    else:
                        print("Not enough coins to roll the shop!")
                # --- Handle Next Round Button ---
                if self.next_round_button.is_clicked(mouse_pos):
                    self.game_manager.change_state(self.game_manager.GAME_STATE_PLAYING)
                    self.game_manager._next_round()

                # --- Handle Backpack Icon Click ---
                if self.backpack_icon_rect.collidepoint(mouse_pos):
                    self.game_manager.change_state(self.game_manager.GAME_STATE_INVENTORY)

    def draw(self):
        self.screen.fill(self.background_color)

        title_surface = self.font_title.render("The Seed Shop", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_surface, title_rect)
        
        coins_text = self.font_text.render(f"Coins: {self.game_manager.player.get_coins()}", True, (255, 255, 0))
        self.screen.blit(coins_text, (50, 50))

        # Draw shop products
        for product in self.products_on_display:
            product.draw(self.screen)

            buy_button_width = 70
            buy_button_height = 25
            buy_button_x = product.rect.centerx - buy_button_width // 2
            buy_button_y = product.rect.bottom + 30

            buy_button = Button(
                buy_button_x,
                buy_button_y,
                buy_button_width,
                buy_button_height,
                f"Buy ({product.price}$)",
                (0, 90, 0),
                (255, 255, 255),
                24
            )
            buy_button.draw(self.screen)
            # Store the button rect for click detection
            product.buy_button_rect = buy_button.rect


        # Draw control buttons
        self.roll_button.draw(self.screen)
        self.next_round_button.draw(self.screen)

        # Draw Backpack Icon (top right)
        self.screen.blit(self.backpack_icon_image, self.backpack_icon_rect)

    def update(self):
        pass