import pygame
from seed import Seed
import random

class Player:
    """
    Represents the player in the game, managing their score and seed backpack.
    """
    def __init__(self , initial_seeds_count: int = 10):
        """
        Initializes the Player with a starting set of seeds.

        Args:
            initial_seeds_count (int): The number of seeds to start the game with in the backpack.
        """
        self.backpack_seeds: list[Seed] = []
        self.max_backpack_size = 20

        for i in range(initial_seeds_count):
            seed = Seed(0,0 , 'assets/seed.jpg', 'Basic Seed', (40,40), 10)
            self.backpack_seeds.append(seed)

    def add_seed(self, seed:Seed):
        """
        Adds a seed to the player's backpack if there is space.

        Args:
            seed (Seed): The seed to add to the backpack.
        """
        if len(self.backpack_seeds) < self.max_backpack_size:
            self.backpack_seeds.append(seed)
            print(f"Added {seed.name} to backpack.")
        else:
            print("Backpack is full. Cannot add more seeds.")


    def get_seeds_to_hand(self, num_seeds_to_draw:int) -> list[Seed]:
        """
        Draws a specified number of seeds from the backpack to the player's hand.

        Args:
            num_seeds_to_draw (int): The number of seeds to draw from the backpack.

        Returns:
            list[Seed]: A list of seeds drawn from the backpack.
        """
        drawn_hand = []
        actual_drawn_hand = min(num_seeds_to_draw, len(self.backpack_seeds))
        for i in range(actual_drawn_hand):
            drawn_hand.append(self.backpack_seeds.pop(0))
        return drawn_hand
    
    def return_seeds_to_backpack(self, seeds: list[Seed]):
        """
        Returns a list of seeds back to the backpack.

        Args:
            seeds (list[Seed]): The seeds to return to the backpack.
        """
        for seed in seeds:
            if len(self.backpack_seeds) < self.max_backpack_size:
                self.backpack_seeds.append(seed)
                print(f"Returned {seed.name} to backpack.")
            else:
                print("Backpack is full. Cannot return more seeds.")

    def get_backpack_seed_count(self) -> int:
        """Returns the current number of seeds in the backpack."""
        return len(self.backpack_seeds)


    def is_backpack_empty(self) -> bool:
        """Checks if the backpack is empty."""
        return len(self.backpack_seeds) == 0