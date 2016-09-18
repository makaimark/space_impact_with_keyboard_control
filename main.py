import pygame
import spaceship
import bullet
import datetime
from enemy import Enemy
import random
import time


def number_of_lifes(screen, ship):
    if ship.life == 3:
        life = pygame.image.load("media_files/3.png")
        life = pygame.transform.scale(life, (50, 50))
        return life
    elif ship.life == 2:
        life = pygame.image.load("media_files/2.png")
        life = pygame.transform.scale(life, (50, 50))
        return life
    elif ship.life == 1:
        life = pygame.image.load("media_files/1.png")
        life = pygame.transform.scale(life, (50, 50))
        return life
    elif ship.life == 0:
        life = pygame.image.load("media_files/gameover.png")
        life = pygame.transform.scale(life, (500, 500))
        return life

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
        pygame.init()
        bullet_list = []
        clock = pygame.time.Clock()         # Used to manage how fast the screen updates
        ship = spaceship.SpaceShip()
        shiprect = ship.getrect()
        pygame.key.set_repeat(1, 40)
        delay = 250000
        last_shot = datetime.datetime.now()
        number_of_lifes(screen, ship)
        return (BLACK, size, screen, enemy_list, bullet_list, clock, ship, shiprect, delay, last_shot)

    BLACK, size, screen, enemy_list, bullet_list, clock, ship, shiprect, delay, last_shot = init()

    # -------- Main Program Loop -----------
    while ship.life != 0:

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
                        continue

        def check_number_of_enemies(level, enemy_list):
            if len(enemy_list) <= 5:
                spawn_enemy(level * 5)
                level += 1

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
        screen.blit(number_of_lifes(screen, ship), (0, 0))

        # move and remove all bullet objects
        iterate_bullet_list(bullet_list)

        # check if a bullet shot the ship
        check_if_bullet_shot_ship(enemy_list)

        # iterate thwough list of the enemies, and check if we shot them down
        check_enemy_death(enemy_list)

        check_number_of_enemies(level, enemy_list)

        '''if ship.life == 0:
            time.sleep(5)
            exit()'''



        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()

if __name__ == "__main__":
    main()