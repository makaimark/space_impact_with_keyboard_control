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


def main():
    pygame.mixer.init()
    sound = pygame.mixer.Sound('sound.wav')
    sound.play(-1)

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (1280, 1024)
    screen = pygame.display.set_mode(size)
    enemy_list = pygame.sprite.Group()

    # Loop until the user clicks the close button.
    done = False


    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    ship = spaceship.SpaceShip()

    shiprect = ship.getrect()
    pygame.key.set_repeat(1, 40)
    bullet_list = []
    delay = 250000
    last_shot = datetime.datetime.now()

    def spawn_enemy(default):
        for i in range(default):
            enemy = Enemy()
            enemy.rect.x = random.randrange(1000,size[0])
            enemy.rect.y = random.randrange(50 , size[1] -50)
            enemy_list.add(enemy)

    number_of_lifes(screen, ship)

    # -------- Main Program Loop -----------
    while not done:

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



        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)
        enemy_list.update()
        enemy_list.draw(screen)

        screen.blit(ship.image, shiprect)
        screen.blit(number_of_lifes(screen, ship), (0, 0))


        for bull in bullet_list:
            if bull.x_coordinate > 1260:
                bullet_list.remove(bull)
                continue
            bulletrect = (bull.x_coordinate, bull.y_coordinate-5)
            bull.bullet_mover()
            screen.blit(bull.image, bulletrect)

        for enemy in enemy_list:
            if enemy.rect.colliderect(shiprect):
                ship.life -= 1
                enemy_list.remove(enemy)

        for enemy in enemy_list:
            for bull in bullet_list:
                if enemy.rect.colliderect((bull.x_coordinate, bull.y_coordinate, 30, 10)):
                    bullet_list.remove(bull)
                    enemy_list.remove(enemy)
                    continue

        if len(enemy_list) <= 5:
            spawn_enemy(level * 5)
            level += 1

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