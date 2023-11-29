import pygame
import random
import math
import sys
import pygame._sdl2.controller

pygame.init()

# creating screen
screen = pygame.display.set_mode((800, 800))

# Title and icon
pygame.display.set_caption('Jets!')
icon = pygame.image.load('rocket(1).png')
pygame.display.set_icon(icon)
running = True
# background
background_img = pygame.image.load('space_bg.jpg')
# Player
player_icon = pygame.image.load('Jet.png')
playerX = 360
playerY = 630
playerX_co = 0
playerY_co = 0
# enemy
enemy_icon = []
enemyX = []
enemyY = []
enemyX_co = []
enemyY_co = []
spawn = 20
for i in range(spawn):
    enemy_icon.append(pygame.image.load('Alien Ship.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_co.append(1)
    enemyY_co.append(40)
# bullet
bullet_icon = pygame.image.load('bullet(1).png')
bulletX = 0
bulletY = 630
bulletX_co = 0
bulletY_co = 6
bullet_state = 'reload'

#Controller init
pygame._sdl2.controller.init()
for x in range(pygame.joystick.get_count()):
    if pygame._sdl2.controller.is_controller(x):
        ABXY = pygame._sdl2.controller.Controller(x)

#Audio Init
Bang = pygame.mixer.Sound('Bang.mp3')
Boom = pygame.mixer.Sound('Boom.mp3')

def player(x, y):
    screen.blit(player_icon, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_icon[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_icon, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
while running:

    screen.fill((0, 0, 0))
    screen.blit(background_img, (0, 0))
    for task in pygame.event.get():
        if task.type == pygame.QUIT:
            running = False
        # checking keys, controller, and mouse
        mrx, mry = pygame.mouse.get_rel()
        if mrx > 0 or mry > 0:
          mousex, mousey = pygame.mouse.get_pos()
          playerX = mousex - 30
        if pygame.mouse.get_pressed()[0]:
                if bullet_state == 'reload':
                    pygame.mixer.Sound.play(Bang)
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        #if pygame.controller 
        if "ControllerButtonDown" in str((pygame.event.event_name(task.type))):
            if task.dict['button'] == 14:
                playerX_co = 2
            if task.dict['button'] == 13:
                playerX_co = -2
            if task.dict['button'] == 0:
              if bullet_state == 'reload':
                    pygame.mixer.Sound.play(Bang)
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if "ControllerAxisMotion" in str((pygame.event.event_name(task.type))):
            if task.dict["axis"] == 4:
                if task.dict["value"] > 1:
                    playerX_co = -(task.dict["value"])/10000
                else:
                    playerX_co = 0
            if task.dict["axis"] == 5:
                if task.dict["value"] > 1:
                    playerX_co = (task.dict["value"])/10000
                else:
                    playerX_co = 0
            if task.dict["axis"] == 0:
                if task.dict["value"] > 10000:
                    playerX_co = (task.dict["value"])/5000
                elif task.dict["value"] < -10000:
                    playerX_co = (task.dict["value"])/5000
                else:
                    playerX_co = 0
        
        if "ControllerButtonUp" in str((pygame.event.event_name(task.type))) and task.dict['button'] != 0:
            playerX_co = 0

        if task.type == pygame.KEYDOWN:
            if task.key == pygame.K_LEFT:
                playerX_co = -2
            if task.key == pygame.K_RIGHT:
                playerX_co = 2
            if task.key == pygame.K_SPACE:
                if bullet_state == 'reload':
                    pygame.mixer.Sound.play(Bang)
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if task.type == pygame.KEYUP:
            if task.key == pygame.K_LEFT or task.key == pygame.K_RIGHT:
                playerX_co = 0
            if task.key == pygame.K_UP or task.key == pygame.K_DOWN:
                playerY_co = 0

    # player
    playerX += playerX_co
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY >= 736:
        playerY = 736

    # enemy co-ordinates
    for i in range(spawn):
        enemyX[i] += enemyX_co[i]
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            if abs(enemyX_co[i]) < 5:
              enemyX_co[i] = enemyX_co[i] * -1.1
            else:
              enemyX_co[i] = enemyX_co[i] * -1
            enemyY[i] += enemyY_co[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            pygame.mixer.Sound.play(Boom)
            bulletY = 630
            bullet_state = 'reload'
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            spawn -= 1
            if spawn == 0:
                running = False
        enemy(enemyX[i], enemyY[i], i)

    # bullet movements
    if bulletY <= 0:
        bulletY = 630
        bullet_state = 'reload'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_co

    player(playerX, playerY)

    pygame.display.update()
    

pygame.quit()
sys.exit()
