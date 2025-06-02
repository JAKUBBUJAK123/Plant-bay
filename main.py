import pygame
import sys
import random
from soil import Soil
from seed import Seed
from button import Button
from shop_scene import ShopScene
from player import Player
from inventory_scene import InventoryScene

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_TITLE = "Botanic Game"
BG_COLOR = (0, 128, 0)  
TEXT_COLOR = (255, 255, 255)  
BUTTON_COLOR = (50, 150, 50)
BUTTON_HOVER_COLOR = (70, 170, 70)

# Soil properties
SOIL_SIZE = 80
SOIL_PADDING = 20
SOIL_DEFAULT_COLOR = (139, 69, 19)
PLANTED_SOIL_COLOR = (0, 70, 0)
NUM_SOILS = 5

# Seed properties
SEED_IMAGE_SIZE = (40, 40)
SEED_PADDING = 30
DEFAULT_SEED_VALUE = 10
NUM_SEEDS_IN_HAND = 5
NUM_INITIAL_BACKPACK_SEEDS = 10

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # --- Game States ---
        self.GAME_STATE_PLAYING = "PLAYING"
        self.GAME_STATE_SHOP = "SHOP"
        self.GAME_STATE_LOSE = "LOSE"
        self.GAME_STATE_INVENTORY = "INVENTORY"
        self.current_game_state = self.GAME_STATE_PLAYING
        self.previous_state = self.GAME_STATE_PLAYING

        # --- Fonts ---
        self.font_welcome = pygame.font.Font(None, 36)
        self.font_hello_botany = pygame.font.Font(None, 48)
        self.font_score = pygame.font.Font(None, 30)
        self.font_game_over = pygame.font.Font(None, 100)

        # --- Game Variables ---
        self.current_score = 0
        self.score_goal = 200
        self.predicted_score = 0
        self.round_number = 1

        # --- Game Objects ---
        self.player = Player(NUM_INITIAL_BACKPACK_SEEDS)
        self.soils = []
        self.seeds_in_hand = [] 

        # --- UI Elements ---
        self.play_hand_button = None
        #Backpack
        self.backpack_icon_image = pygame.image.load("assets/backpack.png").convert_alpha()
        self.backpack_icon_image = pygame.transform.scale(self.backpack_icon_image, (60, 60))
        self.backpack_icon_rect = self.backpack_icon_image.get_rect()
        self.backpack_icon_rect.x = SCREEN_WIDTH - 60 - 20
        self.backpack_icon_rect.y = SCREEN_HEIGHT - 60 - 20

        # Dragging state
        self.dragging_seed = False
        self.dragged_seed = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # --- Scene Managers ---
        self.shop_scene = ShopScene(self.screen, self , self.player) 
        self.inventory_scene = InventoryScene(self.screen, self.player, self)

        self._initialize_game_objects()
        self._initialize_ui_elements()
        self._draw_hand_from_backpack()
        self.calculate_predicted_score()
        self._start_new_round()

    def _initialize_game_objects(self):
        """Initializes soil plots and initial seeds."""
        # Soils
        total_plots_width = (NUM_SOILS * SOIL_SIZE) + ((NUM_SOILS - 1) * SOIL_PADDING)
        start_x = (SCREEN_WIDTH - total_plots_width) // 2
        plot_y = SOIL_PADDING + 20 # Y position for soils

        for i in range(NUM_SOILS):
            x = start_x + (i * (SOIL_SIZE + SOIL_PADDING))
            soil = Soil(x, plot_y, SOIL_SIZE, "assets/soil.jpg", SOIL_DEFAULT_COLOR)
            self.soils.append(soil)


    def _initialize_ui_elements(self):
        """Initializes UI elements like buttons."""
        button_width = 150
        button_height = 50
        button_x = SCREEN_WIDTH - button_width - 30
        button_y = SCREEN_HEIGHT // 2 - button_height // 2
        self.play_hand_button = Button(button_x, button_y, button_width, button_height,
                                       "Play Hand", BUTTON_COLOR, TEXT_COLOR , 24)
        

    def _generate_new_seeds(self, num_seeds_to_generate, seed_image_size, padding, seed_y):
        """Generates a new set of seeds for the player's hand."""
        new_seeds = []
        seed_area_width = seed_image_size[0]
        total_seeds_width = (num_seeds_to_generate * seed_area_width) + ((num_seeds_to_generate - 1) * padding)
        start_seed_x = (SCREEN_WIDTH - total_seeds_width) // 2

        for i in range(num_seeds_to_generate):
            x = start_seed_x + (i * (seed_area_width + padding))
            new_seed = Seed(x, seed_y, "assets/seed.jpg", f"Seed {i+1}", seed_image_size, value=DEFAULT_SEED_VALUE)
            new_seeds.append(new_seed)
        return new_seeds

    def calculate_predicted_score(self):
        """Calculates the predicted score based on currently planted seeds."""
        self.predicted_score = 0
        for soil in self.soils:
            if soil.is_planted and soil.planted_seed is not None:
                self.predicted_score += soil.planted_seed.value * soil.multiplayer


    def _draw_hand_from_backpack(self):
        """Draws seeds from the player's backpack to their hand."""
        self.seeds_in_hand.clear()
        drawn_seeds = self.player.get_seeds_to_hand(NUM_SEEDS_IN_HAND)

        seed_y = SCREEN_HEIGHT - SEED_IMAGE_SIZE[1] - 50
        seed_area_width = SEED_IMAGE_SIZE[0]
        total_seeds_width = (len(drawn_seeds) * seed_area_width) + ((len(drawn_seeds) - 1) * SEED_PADDING)
        start_seed_x = (SCREEN_WIDTH - total_seeds_width) // 2

        for i, seed in enumerate(drawn_seeds):
            x = start_seed_x + (i * (seed_area_width + SEED_PADDING))
            seed.update_position(x, seed_y)
            seed.original_x = x
            seed.original_y = seed_y
            self.seeds_in_hand.append(seed)


    def handle_events(self):
        """Handles all Pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.current_game_state != self.GAME_STATE_LOSE and \
                   self.backpack_icon_rect.collidepoint(event.pos):
                    if self.current_game_state == self.GAME_STATE_INVENTORY:
                        # If inventory is open, close it
                        self.change_state(self.previous_game_state)
                    else:
                        # If not open, open it and store current state
                        self.previous_game_state = self.current_game_state
                        self.change_state(self.GAME_STATE_INVENTORY)
                    return

            if self.current_game_state == self.GAME_STATE_PLAYING:
                self._handle_playing_events(event)
            elif self.current_game_state == self.GAME_STATE_SHOP:
                self.shop_scene.handle_event(event)
            elif self.current_game_state == self.GAME_STATE_INVENTORY:
                self.inventory_scene.handle_event(event)
            elif self.current_game_state == self.GAME_STATE_LOSE:
                print("Game Over! You lost.")
                pass

    def _handle_playing_events(self, event):
        """Handles events when the game is in the PLAYING state."""

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x , mouse_y = event.pos
                for seed in self.seeds_in_hand:
                    if seed.is_clicked((mouse_x, mouse_y)):
                        self.dragging_seed = True
                        self.dragged_seed = seed
                        self.drag_offset_x = mouse_x - self.dragged_seed.rect.x
                        self.drag_offset_y = mouse_y - self.dragged_seed.rect.y
                        break
                
                if self.play_hand_button.is_clicked((mouse_x, mouse_y)):
                    self._play_hand()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.dragging_seed and self.dragged_seed:
                    dropped_on_soil = False
                    for soil in self.soils:
                        if self.dragged_seed.rect.colliderect(soil.rect) and not soil.is_planted:
                            dropped_on_soil = True
                            soil.plant_seed(self.dragged_seed)
                            soil.set_color(PLANTED_SOIL_COLOR) 
                            self.seeds_in_hand.remove(self.dragged_seed)
                            break

                    if not dropped_on_soil:
                        self.dragged_seed.reset_position()

                    # Reset dragging state
                    self.dragging_seed = False
                    self.dragged_seed = None
                    self.drag_offset_x = 0
                    self.drag_offset_y = 0

        if event.type == pygame.MOUSEMOTION:
            if self.dragging_seed and self.dragged_seed:
                mouse_x, mouse_y = event.pos
                new_x = mouse_x - self.drag_offset_x
                new_y = mouse_y - self.drag_offset_y
                self.dragged_seed.update_position(new_x, new_y)

    def _play_hand(self):
        """Processes the played hand, calculates score, and resets the round."""
        # Score all planted soils
        for soil in self.soils:
            if soil.is_planted and soil.planted_seed is not None:
                self.current_score += soil.planted_seed.value * soil.multiplayer
                print(f"  Scored {soil.planted_seed.value * soil.multiplayer} from {soil.planted_seed.name} on soil (x{soil.multiplayer})")
                soil.reset_soil()

        # Return unplanted seeds to backpack
        self.player.return_seeds_to_backpack(self.seeds_in_hand)
        self.seeds_in_hand.clear()

        if self.current_score >= self.score_goal:
            self.current_score = 0
            self.change_state(self.GAME_STATE_SHOP)
        elif self.current_score < self.score_goal and self.player.is_backpack_empty():
            self.change_state(self.GAME_STATE_LOSE)
            print("You lost! No seeds left in backpack.")
        else:
            self._start_new_round()


    def _next_round(self):
        self.round_number += 1
        self.score_goal += 50
        self._start_new_round()


    def _start_new_round(self):
        """Resets the game state for a new round of play."""
        for soil in self.soils:
            soil.reset_soil()

        self.player.return_seeds_to_backpack(self.seeds_in_hand)
        self._draw_hand_from_backpack()
        self.predicted_score = 0


    def update(self):
        """Updates game logic based on the current game state."""
        if self.current_game_state == self.GAME_STATE_PLAYING:
            self.calculate_predicted_score()
        elif self.current_game_state == self.GAME_STATE_SHOP:
            self.shop_scene.update() 
        elif self.current_game_state == self.GAME_STATE_INVENTORY:
            self.inventory_scene.update()
        elif self.current_game_state == self.GAME_STATE_LOSE:
            pass


    def draw(self):
        """Draws elements on the screen based on the current game state."""
        self.screen.fill(BG_COLOR)

        if self.current_game_state == self.GAME_STATE_PLAYING:
            self._draw_playing_elements()
        elif self.current_game_state == self.GAME_STATE_SHOP:
            self.shop_scene.draw()
        elif self.current_game_state == self.GAME_STATE_INVENTORY:
            self.inventory_scene.draw()
        elif self.current_game_state == self.GAME_STATE_LOSE:
            self._draw_lose_screen()
        if self.current_game_state != self.GAME_STATE_LOSE:
            self.screen.blit(self.backpack_icon_image, self.backpack_icon_rect)

        pygame.display.flip()


    def _draw_lose_screen(self):
        """Draws the game over/lose screen."""
        game_over_text = self.font_game_over.render("GAME OVER!", True, (255, 0, 0)) # Red text
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, game_over_rect)

        score_text = self.font_score.render(f"Final Score: {self.current_score}", True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(score_text, score_rect)


    def _draw_playing_elements(self):
        """Draws elements specific to the PLAYING state."""
        # Draw soil plots
        for soil in self.soils:
            soil.draw(self.screen)

        # Draw seeds
        for seed in self.seeds_in_hand:
            seed.draw(self.screen)

        # Draw UI elements
        self.play_hand_button.draw(self.screen)

        # Draw Score Goal
        score_goal_text = self.font_score.render(f"Goal: {self.score_goal}", True, TEXT_COLOR)
        self.screen.blit(score_goal_text, (30, SCREEN_HEIGHT // 2 - 50))

        # Draw Current Score
        current_score_text = self.font_score.render(f"Score: {self.current_score}", True, TEXT_COLOR)
        self.screen.blit(current_score_text, (30, SCREEN_HEIGHT // 2))

        # Draw Predicted Score
        predicted_score_text = self.font_score.render(f"Predicted: {self.predicted_score}", True, TEXT_COLOR)
        self.screen.blit(predicted_score_text, (30, SCREEN_HEIGHT // 2 + 30))


    def change_state(self, new_state: str):
        """Changes the current game state."""
        self.current_game_state = new_state

    def run(self):
        """Main game loop."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

# --- Main execution block ---
if __name__ == "__main__":

    game = Game()
    game.run()