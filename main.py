import pygame
import random
import math
import sys
import pygame._sdl2.controller
import pygame.gfxdraw

pygame.init()

# creating screen
screen = pygame.display.set_mode((0, 0))
#Font for endgame
fontL = pygame.font.Font('OCR.ttf', 50)
fontS = pygame.font.Font('OCR.ttf', 30)
WinT = fontL.render('Congrats! You Won!', True, (240,0,0))
LoseT = fontL.render('Game Over', True, (240,0,0))
#LoseT = font.render('Game Over', True, green, blue)
#WinT = font.render('Congrats!', True, green, blue)
# Title and icon
pygame.display.set_caption('Jets!')
icon = pygame.image.load('rocket(1).png')
pygame.display.set_icon(icon)
running = True
# background
background_img = pygame.image.load('Background.png')
# Player
player_icon = pygame.image.load('Jet.png')
playerX = (screen.get_width()/2)
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
Score = 100000
for i in range(spawn):
    enemy_icon.append(pygame.image.load('Alien Ship.png'))
    enemyX.append(random.randint(((screen.get_width()/4)), ((screen.get_width()/4)*3)))
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
    Score -= 10
    screen.fill((0, 0, 0))
    screen.blit(background_img, ((screen.get_width())/4, 0))
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
    if playerX <= (screen.get_width()/4):
        playerX = (screen.get_width()/4)
    elif playerX >= ((screen.get_width()/4)*3):
        playerX = ((screen.get_width()/4)*3)
    if playerY <= 0:
        playerY = 0
    elif playerY >= 736:
        playerY = 736

    # enemy co-ordinates
    for i in range(spawn):
        enemyX[i] += enemyX_co[i]
        if enemyX[i] <= (screen.get_width()/4) or enemyX[i] >= ((screen.get_width()/4)*3):
            if abs(enemyX_co[i]) < 5:
              enemyX_co[i] = enemyX_co[i] * -1.1
            else:
              enemyX_co[i] = enemyX_co[i] * -1
            enemyY[i] += enemyY_co[i]

        # collision
        Death = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if Death:
            pygame.gfxdraw.box(screen, pygame.Rect(0,0,2000,2000), (0,0,0,200))
            LoseR = LoseT.get_rect()
            LoseR.center = ((screen.get_width()/2), 300)
            screen.blit(LoseT, LoseR)
            Score = str(Score)
            ScoreT = fontS.render('Your Score was '+Score, True, (240,0,0))
            ScoreR = ScoreT.get_rect()
            ScoreR.center = ((screen.get_width()/2), 400)
            screen.blit(ScoreT, ScoreR)
            AgainT = fontS.render('Press Space to play again', True, (0,100,0))
            AgainR = AgainT.get_rect()
            AgainR.center = ((screen.get_width()/2), 500)
            screen.blit(AgainT, AgainR)
            pause = True
            pygame.display.update()
            while pause:
                for task in pygame.event.get():
                    if task.type == pygame.KEYDOWN:
                        if task.key == pygame.K_SPACE:
                            pause = False
                            #Again!
                            background_img = pygame.image.load('Background.png')
                            # Player
                            player_icon = pygame.image.load('Jet.png')
                            playerX = (screen.get_width()/2)
                            playerY = 630
                            playerX_co = 0
                            playerY_co = 0
                            # enemy
                            enemy_icon = []
                            spawn = 20
                            enemyX = []
                            enemyY = []
                            enemyX_co = []
                            enemyY_co = []
                            Score = 100000
                            for i in range(spawn):
                                enemy_icon.append(pygame.image.load('Alien Ship.png'))
                                enemyX.append(random.randint(((screen.get_width()/4)), ((screen.get_width()/4)*3)))
                                enemyY.append(random.randint(50, 150))
                                enemyX_co.append(1)
                                enemyY_co.append(40)
                            # bullet
                            bullet_icon = pygame.image.load('bullet(1).png')
                            bulletX = 0
                            bulletY = 630
                            bulletX_co = 0
                            bulletY_co = 6
                            bullet_state = "reload"
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            pygame.mixer.Sound.play(Boom)
            bulletY = 630
            bullet_state = 'reload'
            enemyX[i] = random.randint(((screen.get_width()/4)), ((screen.get_width()/4)*3))
            enemyY[i] = random.randint(50, 150)
            spawn -= 1
            if spawn == 0:
                pygame.gfxdraw.box(screen, pygame.Rect(0,0,2000,2000), (0,0,0,200))
                WinR = WinT.get_rect()
                WinR.center = ((screen.get_width()/2), 300)
                screen.blit(WinT, WinR)
                Score = str(Score)
                ScoreT = fontS.render('Your Score was '+Score, True, (240,0,0))
                ScoreR = ScoreT.get_rect()
                ScoreR.center = ((screen.get_width()/2), 400)
                screen.blit(ScoreT, ScoreR)
                AgainT = fontS.render('Press Space to play again', True, (0,100,0))
                AgainR = AgainT.get_rect()
                AgainR.center = ((screen.get_width()/2), 500)
                screen.blit(AgainT, AgainR)
                pause = True
                pygame.display.update()
                while pause:
                    for task in pygame.event.get():
                        if task.type == pygame.KEYDOWN:
                            if task.key == pygame.K_SPACE:
                                pause = False
                                #Again!
                                background_img = pygame.image.load('Background.png')
                                # Player
                                player_icon = pygame.image.load('Jet.png')
                                playerX = (screen.get_width()/2)
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
                                Score = 100000
                                for i in range(spawn):
                                    enemy_icon.append(pygame.image.load('Alien Ship.png'))
                                    enemyX.append(random.randint(((screen.get_width()/4)), ((screen.get_width()/4)*3)))
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
