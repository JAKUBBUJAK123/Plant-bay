import pygame

class SoilUpgrade:
    """
    Class to handle soil upgrades in a game."""
    def __init__(self , x , y, image_path:str, name , target_size = (60,60) , upgrade_effect = "multiplier_boost", effect_value = 1):
        """
        Initializes a SoilUpgrade object.

        Args:
            x (int): The x-coordinate for drawing (can be dummy for inventory).
            y (int): The y-coordinate for drawing (can be dummy for inventory).
            image_path (str): The file path to the upgrade image asset.
            name (str): The name of the upgrade (e.g., "Watering Can").
            target_size (tuple[int, int]): The desired width and height to scale the image to.
            upgrade_effect (str): The type of effect this upgrade applies (e.g., "multiplier_boost").
            effect_value (int): The value of the effect (e.g., how much to boost multiplier).
        """
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, target_size)
        self.name = name
        self.upgrade_effect = upgrade_effect
        self.rect = self.image.get_rect(topleft=(x, y))
        self.effect_value = effect_value
        self.original_x = x
        self.original_y = y

    
    def draw(self, screen:pygame.Surface):
        """
        Draws the upgrade image on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the upgrade on.
        """
        screen.blit(self.image, self.rect.topleft)

        font = pygame.font.Font(None, 20)
        text_surface = font.render(self.name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 10))
        screen.blit(text_surface, text_rect)

    def update(self, dt: int):
        for soil in self.soils:
            soil.update(dt)

    def update_position(self, new_x, new_y):
        """
        Updates the position of the upgrade.

        Args:
            x (int): The new x-coordinate.
            y (int): The new y-coordinate.
        """
        self.rect.x = new_x
        self.rect.y = new_y

    
    def reset_position(self):
        """
        Resets the position of the upgrade to its original coordinates.
        """
        self.rect.x = self.original_x
        self.rect.y = self.original_y


    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        """Checks if the mouse position is over the item's bounding box."""
        return self.rect.collidepoint(mouse_pos)
    

    def apply_effect(self, target_soil):
        """
        Applies the upgrade effect to the target soil.

        Args:
            target_soil (Soil): The soil object to apply the effect to.
        """
        if self.upgrade_effect == "multiplier_boost":
            target_soil.multiplier += self.effect_value
            target_soil.set_color((0, 255, 0))
            print(f"Applied {self.name} to soil! Soil multiplier is now x{target_soil.multiplier}")
        else:
            print('Unknown upgrade effect:', self.upgrade_effect)