import pygame

class SoilUpgrade:
    """
    Class to handle soil upgrades in a game."""
    def __init__(self , x , y, image_path:str, name , target_size = (50,50) ,description="simple 2x multiplier", upgrade_effect = "multiplier_boost", effect_value = 1):
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

        self.is_hovered = False
        self.description = description
        self.popup_font = pygame.font.Font("assets/fonts/pixelFont.ttf", 14)

    
    @classmethod
    def load_upgrades(cls ,data:dict , x =0 , y =0):
        return cls(
            x,
            y,
            data['image'],
            data['name'],
            data['size'],
            data['description'],
            data['upgrade_effect'],
            data['effect_value']
        )


    def draw(self, screen:pygame.Surface):
        """
        Draws the upgrade image on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the upgrade on.
        """
        screen.blit(self.image, self.rect.topleft)


        self.draw_popup_pos(screen)

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


    def update_hoover_screen(self , mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw_popup_pos(self , screen):
        if self.is_hovered:
            
            text_surface = self.popup_font.render(self.description, True, (255, 255, 255))

            
            padding = 5
            popup_width = text_surface.get_width() + 2 * padding
            popup_height = text_surface.get_height() + 2 * padding

            
            popup_x = self.rect.centerx - popup_width // 2
            popup_y = self.rect.top - popup_height - 5

            if popup_x < 0:
                popup_x = 0
            if popup_x + popup_width > screen.get_width():
                popup_x = screen.get_width() - popup_width

            popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
            pygame.draw.rect(screen, (30, 30, 30), popup_rect, border_radius=5) 
            pygame.draw.rect(screen, (100, 100, 100), popup_rect, 1, border_radius=5) 

            screen.blit(text_surface, (popup_x + padding, popup_y + padding))