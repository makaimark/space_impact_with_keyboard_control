import pygame


class SpaceShip:
    life = 3
    image = pygame.image.load("media_files/spaceship.bmp")

    def event_handler(self, event, shiprect):
        if event.key == pygame.K_LEFT:
            if shiprect.left > 0:
                return shiprect.move([-15, 0])
            return shiprect
        elif event.key == pygame.K_RIGHT:
            if shiprect.right < 1260:
                return shiprect.move([15, 0])
            return shiprect
        elif event.key == pygame.K_UP:
            if shiprect.top > 0:
                return shiprect.move([0, -15])
            return shiprect
        elif event.key == pygame.K_DOWN:
            if shiprect.bottom < 1000:
                return shiprect.move([0, 15])
            return shiprect

    def getrect(self):
        return self.image.get_rect()