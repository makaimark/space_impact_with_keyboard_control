import datetime
import random
import time

import pygame

import bullet
import spaceship
from enemy import Enemy
# import menu

pygame.init()


def life_printer(screen, ship):
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("You have : " + str(ship.life) + " life(s) remain", 1, (255, 255, 0))
    screen.blit(label, (0, 0))


def game_over(screen):
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("GAME OVER", 1, (255, 255, 0))
    screen.blit(label, (600, 500))


def music_player():
    pygame.mixer.init()
    sound = pygame.mixer.Sound('sound.wav')
    sound.play(-1)


def main():

    def spawn_enemy(default):
        for i in range(default):
            enemy = Enemy()
            enemy.rect.x = random.randrange(1000, size[0])
            enemy.rect.y = random.randrange(50, size[1] - 50)
            enemy_list.add(enemy)


    def init():
        BLACK = (0, 0, 0)
        size = (1280, 1024)     # Set the width and height of the screen [width, height]
        screen = pygame.display.set_mode(size)
        enemy_list = pygame.sprite.Group()
        music_player()

        bullet_list = []
        clock = pygame.time.Clock()         # Used to manage how fast the screen updates
        ship = spaceship.SpaceShip()
        shiprect = ship.getrect()
        pygame.key.set_repeat(1, 40)
        delay = 250000
        last_shot = datetime.datetime.now()
        life_printer(screen, ship)
        return (BLACK, size, screen, enemy_list, bullet_list, clock, ship, shiprect, delay, last_shot)

    BLACK, size, screen, enemy_list, bullet_list, clock, ship, shiprect, delay, last_shot = init()


    def iterate_bullet_list(bullet_list):
        for bull in bullet_list:
            if bull.x_coordinate > 1260:
                bullet_list.remove(bull)
                continue
            bulletrect = (bull.x_coordinate, bull.y_coordinate - 5)
            bull.bullet_mover()
            screen.blit(bull.image, bulletrect)


    def check_if_bullet_shot_ship(enemy_list):
        for enemy in enemy_list:
            if enemy.rect.colliderect(shiprect):
                ship.life -= 1
                enemy_list.remove(enemy)


    def check_enemy_death(enemy_list):
        for enemy in enemy_list:
            for bull in bullet_list:
                if enemy.rect.colliderect((bull.x_coordinate, bull.y_coordinate, 30, 10)):
                    bullet_list.remove(bull)
                    enemy_list.remove(enemy)
                    ship.highscore += 1
                    continue


    def check_number_of_enemies(level, enemy_list):
        if len(enemy_list) <= 5:
            spawn_enemy(level * 5)
            level += 1


    def highscore_printer(ship):
        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        myfont = pygame.font.SysFont("monospace", 15)
        # render text
        label = myfont.render("Your score: "+str(ship.highscore), 1, (255, 255, 0))
        screen.blit(label, (0, 100))

    # -------- Main Program Loop -----------
    while ship.life != 0:

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)

        level = 2
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    delta_time = datetime.datetime.now() - last_shot
                    if delta_time.microseconds > delay:
                        last_shot = datetime.datetime.now()
                        bullet_1 = bullet.Bullet(pygame.image.load("media_files/Green_laser.png"),  shiprect.midright[0], shiprect.midright[1])
                        bulletrect = (bullet_1.x_coordinate, bullet_1.y_coordinate -5)
                        bullet_list.append(bullet_1)
                else:
                    shiprect = ship.event_handler(event, shiprect)

        enemy_list.update()
        enemy_list.draw(screen)

        screen.blit(ship.image, shiprect)
        life_printer(screen, ship)

        # move and remove all bullet objects
        iterate_bullet_list(bullet_list)

        # check if a bullet shot the ship
        check_if_bullet_shot_ship(enemy_list)

        # iterate thwough list of the enemies, and check if we shot them down
        check_enemy_death(enemy_list)

        check_number_of_enemies(level, enemy_list)

        highscore_printer(ship)

        if ship.life == 0:
            game_over(screen)
            time.sleep(5)
            exit()


        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)
    # Close the window and quit.
    pygame.quit()


# main()