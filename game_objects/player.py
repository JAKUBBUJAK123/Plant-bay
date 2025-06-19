import pygame
from game_objects.seed import Seed
import random
from game_objects.soil_upgrade import SoilUpgrade
from game_helpers.json_loader import load_json_file

class Player:
    """
    Represents the player in the game, managing their score and seed backpack.
    """
    def __init__(self , initial_seeds_count: int = 10 , initial_coins : int = 0 , inital_upgrades = 1):
        """
        Initializes the Player with a starting set of seeds.

        Args:
            initial_seeds_count (int): The number of seeds to start the game with in the backpack.
        """
        self.backpack_seeds: list[Seed] = []
        self.backpack_upgrades: list[SoilUpgrade] = []
        self.max_backpack_size = 20
        self.max_upgrade_capacity = 5
        self.coins = initial_coins

        #loading Seeds
        seed_data = load_json_file('seed_list.json')
        for i in range(int(initial_seeds_count)):
            seed = Seed.load_seed(seed_data['Basic_Seed'])
            self.backpack_seeds.append(seed)

        #loading upgrades
        upgrades_data = load_json_file('upgrades_list.json')
        for i in range(inital_upgrades):
            upgrade1 = SoilUpgrade.load_upgrades(upgrades_data['Odd_Bottle'])
            self.backpack_upgrades.append(upgrade1)
            upgrade2 = SoilUpgrade.load_upgrades(upgrades_data['Even_Bottle'])
            self.backpack_upgrades.append(upgrade2)
            upgrade3 = SoilUpgrade.load_upgrades(upgrades_data['Blood'])
            self.backpack_upgrades.append(upgrade3)
            upgrade4 = SoilUpgrade.load_upgrades(upgrades_data['Hoe'])
            self.backpack_upgrades.append(upgrade4)



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


    def add_upgrade(self, upgrade:SoilUpgrade):
        if (len(self.backpack_upgrades) < self.max_upgrade_capacity):
            self.backpack_upgrades.append(upgrade)
            print(f"Added {upgrade.name} to backpack.")
        else:
            print("Backpack is full. Cannot add more upgrades.")

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

    def get_backpack_upgrade_count(self) -> int:
        """Returns the current number of upgrades in the backpack."""
        return len(self.backpack_upgrades)

    def is_backpack_empty(self) -> bool:
        """Checks if the backpack is empty."""
        return len(self.backpack_seeds) == 0
    def get_backpack_seeds(self) -> list[Seed]:
        return self.backpack_seeds

    def get_backpack_upgrades(self) -> list[SoilUpgrade]:
        """Returns a reference to the list of upgrades in the backpack."""
        return self.backpack_upgrades


    def add_coins(self, amount: int):
        """
        Adds coins to the player's total.

        Args:
            amount (int): The number of coins to add.
        """
        self.coins += amount
        print(f"Added {amount} coins. Total coins: {self.coins}")

    def remove_coins(self, amount: int):
        """
        Removes coins from the player's total.

        Args:
            amount (int): The number of coins to remove.
        """
        if amount <= self.coins:
            self.coins -= amount
            print(f"Removed {amount} coins. Total coins: {self.coins}")
        else:
            print("Not enough coins to buy a product.")

    def get_coins(self) -> int:
        return self.coins 