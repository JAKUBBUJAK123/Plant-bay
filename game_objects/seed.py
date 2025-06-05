import pygame

class Seed:
    """
    Represents a single seed in the player's hand/deck.
    Now uses an image asset.
    """
    def __init__(self, x: int, y: int, image_path: str, name: str = "Basic Seed", target_size: tuple[int, int] = (50, 50) , value: int = 10):
        """
        Initializes a Seed object.

        Args:
            x (int): The x-coordinate of the top-left corner of the seed's bounding box.
            y (int): The y-coordinate of the top-left corner of the seed's bounding box.
            image_path (str): The file path to the seed image asset.
            name (str): The name of the seed.
            target_size (tuple[int, int]): The desired width and height to scale the image to.
        """
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, target_size)

        self.name = name
        self.value = value
        self.rect = self.image.get_rect(topleft=(x, y))

        # Store original position for snapping back
        self.original_x = x
        self.original_y = y

    def draw(self, screen: pygame.Surface):
        """
        Draws the seed using its image asset with its name on the given Pygame screen.

        Args:
            screen (pygame.Surface): The Pygame surface to draw on.
        """
        # Draw the seed image
        screen.blit(self.image, self.rect)

        font = pygame.font.Font("assets/fonts/pixelFont.ttf", 15)
        text_surface = font.render(self.name, True, (255, 255, 255)) # White text
        # Position text below the seed's image
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 10))
        screen.blit(text_surface, text_rect)

    def reset_position(self):
        """Resets the seed to its original spawning position."""
        self.rect.x = self.original_x
        self.rect.y = self.original_y

    def update_position(self, new_x: int, new_y: int):
        """Updates the seed's top-left position."""
        self.rect.x = new_x
        self.rect.y = new_y

    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        """Checks if the mouse position is over the seed's bounding box."""
        return self.rect.collidepoint(mouse_pos)