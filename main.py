# main.py
import pygame
import sys
# Import refactored components
from game_objects.player import Player
from button import Button

# Import scenes
from scenes.shop_scene import ShopScene
from scenes.inventory_scene import InventoryScene
from scenes.playing_scene import PlayingScene 
from scenes.lose_scene import LoseScene 

# Import game logic and initialization helpers
from game_logic import GameRoundManager
from game_initializer import GameInitializer

# --- Global Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_TITLE = "Botanic Game"
FPS = 60
BG_COLOR = (0, 128, 0)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 150, 50)
BUTTON_HOVER_COLOR = (70, 170, 70)

#--- Game State Constants---
GAME_STATE_PLAYING = "PLAYING"
GAME_STATE_SHOP = "SHOP"
GAME_STATE_LOSE = "LOSE"
GAME_STATE_INVENTORY = "INVENTORY"


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        # --- Game States ---
        self.current_game_state = GAME_STATE_PLAYING
        self.previous_state = GAME_STATE_PLAYING
        self.GAME_STATE_PLAYING = GAME_STATE_PLAYING
        self.GAME_STATE_SHOP = GAME_STATE_SHOP
        self.GAME_STATE_LOSE = GAME_STATE_LOSE
        self.GAME_STATE_INVENTORY = GAME_STATE_INVENTORY
    
        # --- Fonts ---
        self.font_welcome = pygame.font.Font(None, 36)
        self.font_hello_botany = pygame.font.Font(None, 48)
        self.font_score = pygame.font.Font(None, 30)
        self.font_game_over = pygame.font.Font(None, 100)

        # --- Game Variables ---
        self.current_score = 0
        self.score_goal = 10
        self.predicted_score = 0
        self.round_number = 1

        # ---Player Objects ---
        self.player = Player(initial_seeds_count=10, initial_coins=100, inital_upgrades=1)

        # --- Game Objects ---
        self.soils = []
        self.seeds_in_hand = [] 
        self.upgrades_in_hand = []

        # ---Drag and Drop State---
        self.dragging_item = False
        self.dragged_item = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # --- UI Elements ---
        #Backpack
        self.backpack_icon_button = Button(
            x=SCREEN_WIDTH - 70, y =SCREEN_HEIGHT -70,
            width=50, height=50,
            text="",
            button_color=(255,255,255),
            text_color=(255,255,255),
            font_size=1
        )
        self.backpack_icon_button.image = pygame.image.load("assets/backpack.png").convert_alpha()
        self.backpack_icon_button.image = pygame.transform.scale(self.backpack_icon_button.image, (50, 50))

        # --- Scene Managers ---
        self.shop_scene = ShopScene(self.screen, self , self.player, shop_item_size=(80, 80)) 
        self.inventory_scene = InventoryScene(self.screen, self.player, self)
        self.playing_scene = PlayingScene(self.screen, self)
        self.lose_scene = LoseScene(self.screen, self)

        # --- Helper Managers ---
        self.game_initializer = GameInitializer(self)
        self.round_manager = GameRoundManager(self)

        # --- Initial Game Setup ---
        self.game_initializer.initialize_game_objects()
        self.game_initializer.initialize_ui_elements()

        # --- Start First Round ---
        self.round_manager.start_new_round()
        self.round_manager.calculate_predicted_score()


    def handle_events(self):
        """Handles all Pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.backpack_icon_button.is_clicked(event.pos):
                    if self.current_game_state == self.GAME_STATE_INVENTORY:
                        self.change_state(self.previous_game_state)
                    else:
                        self.previous_game_state = self.current_game_state
                        self.change_state(self.GAME_STATE_INVENTORY)
                    continue

            if self.current_game_state == self.GAME_STATE_PLAYING:
                self.playing_scene.handle_event(event)
            elif self.current_game_state == self.GAME_STATE_SHOP:
                self.shop_scene.handle_event(event)
            elif self.current_game_state == self.GAME_STATE_INVENTORY:
                self.inventory_scene.handle_event(event)
            elif self.current_game_state == self.GAME_STATE_LOSE:
                self.lose_scene.handle_event(event)

            # --- Unified Drag & Drop Handling---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos

                if self.current_game_state == self.GAME_STATE_PLAYING:
                    for seed in self.seeds_in_hand:
                        if seed.is_clicked((mouse_x, mouse_y)):
                            self.dragging_item = True
                            self.dragged_item = seed
                            self.drag_offset_x = mouse_x - self.dragged_item.rect.x
                            self.drag_offset_y = mouse_y - self.dragged_item.rect.y
                            break
                elif self.current_game_state == self.GAME_STATE_INVENTORY:
                    for upgrade in self.player.get_backpack_upgrades():
                        if upgrade.is_clicked((mouse_x, mouse_y)):
                            self.dragging_item = True
                            self.dragged_item = upgrade
                            self.drag_offset_x = mouse_x - self.dragged_item.rect.x
                            self.drag_offset_y = mouse_y - self.dragged_item.rect.y
                            self.change_state(self.GAME_STATE_PLAYING)
                            break

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.dragging_item and self.dragged_item is not None:
                    self.round_manager.handle_item_drop(self.dragged_item, event.pos)

                    self.dragging_item = False
                    self.dragged_item = None
                    self.drag_offset_x = 0
                    self.drag_offset_y = 0

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_item and self.dragged_item is not None:
                    mouse_x, mouse_y = event.pos
                    new_x = mouse_x - self.drag_offset_x
                    new_y = mouse_y - self.drag_offset_y
                    self.dragged_item.update_position(new_x, new_y)


    def update(self):
        """Updates game logic based on the current game state."""
        if self.current_game_state == self.GAME_STATE_PLAYING:
            self.playing_scene.update()
            self.round_manager.calculate_predicted_score()

        elif self.current_game_state == self.GAME_STATE_SHOP:
            self.shop_scene.update() 

        elif self.current_game_state == self.GAME_STATE_INVENTORY:
            self.inventory_scene.update()
        elif self.current_game_state == self.GAME_STATE_LOSE:
            self.lose_scene.update()


    def draw(self):
        """Draws elements on the screen based on the current game state."""
        self.screen.fill(BG_COLOR)

        if self.current_game_state == self.GAME_STATE_PLAYING:
            self.playing_scene.draw()

        elif self.current_game_state == self.GAME_STATE_SHOP:
            self.shop_scene.draw()

        elif self.current_game_state == self.GAME_STATE_INVENTORY:
            self.inventory_scene.draw()

        elif self.current_game_state == self.GAME_STATE_LOSE:
            self.lose_scene.draw()

        if self.current_game_state in [self.GAME_STATE_PLAYING, self.GAME_STATE_SHOP ,self.GAME_STATE_INVENTORY]:
            self.backpack_icon_button.draw(self.screen)

        if self.dragged_item is not None and self.dragging_item:
            self.dragged_item.draw(self.screen)

        pygame.display.flip()


    def change_state(self, new_state: str):
        """Changes the current game state."""
        self.current_game_state = new_state

    def run(self):
        """Main game loop."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

# --- Main execution block ---
if __name__ == "__main__":

    game = Game()
    game.run()