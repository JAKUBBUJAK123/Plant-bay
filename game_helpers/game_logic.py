# game_logic.py
import pygame
from game_objects.seed import Seed
from game_objects.soil_upgrade import SoilUpgrade
import random

# Constants used in game logic
DEFAULT_SEED_VALUE = 10
NUM_SEEDS_IN_HAND = 5
SEED_IMAGE_SIZE = (40, 40)
SEED_PADDING = 25
COINS_PER_ROUND = 50
PLANTED_SOIL_COLOR = (0, 70, 0)
UPGRADED_SOIL_COLOR = (0, 120, 255) 
UPGRADE_IMAGE_SIZE = (40, 40)

class GameRoundManager:
    """
    Manages game rounds, scoring, and item drop logic.
    """
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.NUM_SOILS = 5

    def calculate_predicted_score(self):
        """Calculates the predicted score based on currently planted seeds."""
        self.game_manager.predicted_score = 0
        for soil in self.game_manager.soils:
            if soil.is_planted and soil.planted_seed is not None:
                harvest_value = soil.predict_harvest_value()
                synergy_value = soil.calculate_synergy_bonus(self.game_manager.soils, self.game_manager.soils.index(soil))
                self.game_manager.predicted_score += harvest_value + synergy_value

    def _draw_hand_from_backpack(self):
        """Draws a specified number of seeds from the player's backpack to their hand."""
        self.game_manager.seeds_in_hand.clear()
        drawn_seeds = self.game_manager.player.get_seeds_to_hand(NUM_SEEDS_IN_HAND)

        seed_y = self.game_manager.screen.get_height() - SEED_IMAGE_SIZE[1] - 16
        seed_area_width = SEED_IMAGE_SIZE[0]
        total_seeds_width = (len(drawn_seeds) * seed_area_width) + ((len(drawn_seeds) - 1))
        start_seed_x = (self.game_manager.screen.get_width() - total_seeds_width) // 2 -  SEED_IMAGE_SIZE[0] - 10

        for i, seed in enumerate(drawn_seeds):
            x = start_seed_x + (i * (seed_area_width + SEED_PADDING))
            seed.update_position(x, seed_y)
            seed.original_x = x
            seed.original_y = seed_y
            self.game_manager.seeds_in_hand.append(seed)

    def _draw_upgrades_for_hand(self):
        """Draws upgrades from the player's backpack to the 'hand' list for potential dragging in playing state."""
        self.game_manager.upgrades_in_hand.clear() # Clear any previously drawn upgrades
        drawn_upgrades = self.game_manager.player.get_backpack_upgrades()

        upgrade_y = self.game_manager.screen.get_height() - UPGRADE_IMAGE_SIZE[1] - 50
        upgrade_x_start = 30
        for i, upgrade in enumerate(drawn_upgrades):
            x = upgrade_x_start + i * (UPGRADE_IMAGE_SIZE[0] + 20)
            upgrade.update_position(x, upgrade_y)
            upgrade.original_x = x
            upgrade.original_y = upgrade_y
            self.game_manager.upgrades_in_hand.append(upgrade)

    def handle_item_drop(self, dropped_item, mouse_pos):
        """
        Handles the logic for dropping a dragged item (seed or upgrade) onto the game board.
        """
        dropped_on_target = False
        for soil in self.game_manager.soils:
            if dropped_item.rect.colliderect(soil.rect):
                if isinstance(dropped_item, Seed):
                    if not soil.is_planted:
                        dropped_on_target = True
                        soil.plant_seed(dropped_item)
                        soil.set_image('assets/soils/planted_soil.png')
                        soil.spawn_particles(20, (50, 168, 82 , 180))

                        #clover soil
                        if soil.is_clover:
                            rand = random.random()
                            if rand < 0.3:
                                print('seed not consumed')
                                dropped_item.reset_position()
                            elif rand < 0.6:
                                self.game_manager.player.coins += 10
                                dropped_item.reset_position()

                        #normal soil
                        else:
                            self.game_manager.seeds_in_hand.remove(dropped_item)
                            soil.start_shaking(duration=200, intensity=10)
                            dropped_item.reset_position()
                    else:
                        print("Soil is already planted! Cannot plant seed.")
                        pass
                elif isinstance(dropped_item, SoilUpgrade):
                    if getattr(soil, "is_upgraded" , False) and not getattr(SoilUpgrade, 'upgrade_effect' , 'remove_upgrade'):
                        print('cant stack upgrades')
                        dropped_item.reset_position()
                        return
                    dropped_on_target = True
                    dropped_item.apply_effect(soil,self.game_manager.soils)
                    soil.spawn_particles(12, (0, 120, 255, 180))
                    self.game_manager.player.backpack_upgrades.remove(dropped_item)
                    if dropped_item in self.game_manager.upgrades_in_hand:
                        self.game_manager.upgrades_in_hand.remove(dropped_item)
                        soil.start_shaking(duration=200, intensity=10)
                break

        if not dropped_on_target:
            dropped_item.reset_position()

    def play_hand(self):
        """Processes the played hand, calculates score, and checks win/lose condition."""
        print("\n--- Playing Hand ---")
        unplanted_seeds_in_hand = []


        for soil in self.game_manager.soils:
            if soil.is_planted and soil.planted_seed is not None:
                if getattr(soil, 'is_evil', False):
                    if random.random() < 0.3:
                        soil.multiplier = 0
                harvest_value = soil.harvest_seed(player=self.game_manager.player)
                synergy_value = soil.calculate_synergy_bonus(self.game_manager.soils, self.game_manager.soils.index(soil))
                self.game_manager.current_score += harvest_value + synergy_value
                soil.reset_soil()

        # Any seeds remaining in hand were not planted, return them to backpack
        for seed in self.game_manager.seeds_in_hand:
            unplanted_seeds_in_hand.append(seed)

        self.game_manager.player.return_seeds_to_backpack(unplanted_seeds_in_hand)
        self.game_manager.seeds_in_hand.clear() # Clear hand after processing

        if self.game_manager.current_score >= self.game_manager.score_goal:
            self.game_manager.player.add_coins(COINS_PER_ROUND)

            self.game_manager.change_state(self.game_manager.GAME_STATE_ROUND_WON)
            def play_sound():
                click_sound = pygame.mixer.Sound("music/sound_effects/round-won.wav")
                click_sound.set_volume(0.5)
                click_sound.play()
            play_sound()
        else:
            self.start_new_round() # Start new round if failed

        if (
        self.game_manager.current_score < self.game_manager.score_goal and
        len(self.game_manager.player.backpack_seeds) == 0 and
        len(self.game_manager.seeds_in_hand) == 0
    ):
            self.game_manager.change_state(self.game_manager.GAME_STATE_LOSE)
            return

    def next_round(self):
        """Advances to the next round, increasing the score goal."""
        self.game_manager.round_number += 1
        self.game_manager.score_goal += 50 # Increase goal for next round
        self.start_new_round()

    def start_new_round(self):
        """Resets the game state for a new round of play."""
        for soil in self.game_manager.soils:
            soil.reset_soil() # This resets planted seed and color only

        # Return any seeds that might still be in hand (e.g., from previous failed round)
        self.game_manager.player.return_seeds_to_backpack(self.game_manager.seeds_in_hand)
        self.game_manager.seeds_in_hand.clear() # Clear hand for new draw

        self._draw_hand_from_backpack() # Draw new seeds for hand
        self._draw_upgrades_for_hand()  # Draw upgrades to hand (if any from backpack)
        self.calculate_predicted_score() # Recalculate score for new round