import pygame
import random

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load("media_files/invader.jpg")
        self.image = pygame.transform.scale(self.image, (50, 50))

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()


    def reset_pos(self):
        """ Reset position to the top of the screen, at a random x location.
        Called by update() or the main program loop if there is a collision.
        """
        self.rect.x = 820
        self.rect.y = random.randrange(0, 500)

    def update(self):
        """ Called each frame. """

        # Move block down one pixel
        self.rect.x -= 2

        # If block is too far down, reset to top of screen.
        if self.rect.x < 0:
            self.reset_pos()