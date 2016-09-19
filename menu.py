# Highlight-able menu in Pygame
#
# To run, use:
#     python pygame-menu-mouseover.py
#
# You should see a window with three grey menu options on it.  Place the mouse
# cursor over a menu option and it will become white.
import pygame
import sys
from main import main

class Option:
    hovered = False

    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (255, 255, 255)
        else:
            return (100, 100, 100)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos


pygame.init()
screen = pygame.display.set_mode((1280, 1024))
menu_font = pygame.font.Font("font/PressStart2P.ttf", 40)
pygame.font.init()

new_game = Option("NEW GAME", (500, 300))
# highscrore = Option("HIGHSCORE", (135, 155))
exit = Option("EXIT", (500, 400))
options = [new_game, exit]

while True:
    pygame.event.pump()
    screen.fill((0, 0, 0))
    events = pygame.event.get()

    for option in options:
        option.draw()

    for event in events:

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                if new_game.hovered == True and exit.hovered == False:
                    new_game.hovered = False
                    exit.hovered = True
                elif exit.hovered == True and new_game.hovered == False:
                    exit.hovered = False
                    new_game.hovered = True
                elif new_game.hovered == False and exit.hovered == False:
                    new_game.hovered = True
            elif event.key == pygame.K_SPACE:
                if new_game.hovered == True:
                    main()
                if exit.hovered == True:
                    sys.exit()

    pygame.display.update()