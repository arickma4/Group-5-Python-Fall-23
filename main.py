import pygame
import random
import math

pygame.init()

# creating screen
screen = pygame.display.set_mode((800, 800))

# Title and icon
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('rocket(1).png')
pygame.display.set_icon(icon)
running = True
# background
background_img = pygame.image.load('space_bg.jpg')
# Player
player_icon = pygame.image.load('spaceship(1).png')
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
spawn = 30
for i in range(spawn):
    enemy_icon.append(pygame.image.load('enemy(1).png'))
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
        # checking keys
        if task.type == pygame.KEYDOWN:
            if task.key == pygame.K_LEFT:
                playerX_co = -2
            if task.key == pygame.K_RIGHT:
                playerX_co = 2
            if task.key == pygame.K_SPACE:
                if bullet_state == 'reload':
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