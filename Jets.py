import pygame
import random
import math
import sys
import pygame._sdl2.controller
import pygame.gfxdraw
import multiprocessing

pygame.init()

# creating screen
screen = pygame.display.set_mode((0, 0))

#Scale factor
SF=screen.get_height()/900
#Logical Processor Factor (Yeah, I had to go there)
SQLP =(math.sqrt(multiprocessing.cpu_count()))
LPF=(math.log(SQLP, SF*2))/(3/SQLP)
print(LPF)
print((math.ceil((2/(LPF))))*10)
print(math.log(50, SF*2))

#Fonts and Text for endgame
fontL = pygame.font.Font('Assets/OCR.ttf', int(50*SF))
fontS = pygame.font.Font('Assets/OCR.ttf', int(30*SF))
WinT = fontL.render('Congrats! You Won!', True, (240,0,0))
LoseT = fontL.render('Game Over', True, (240,0,0))

#Title and pictures init
pygame.display.set_caption('Jets!')
icon = pygame.image.load('Assets/Jets_icon.png')
background_img = pygame.image.load('Assets/Background.png')
background_img = pygame.transform.scale(background_img, (screen.get_height(), screen.get_height()))
player_icon = pygame.image.load('Assets/Jet.png')
player_icon = pygame.transform.scale(player_icon, ((player_icon.get_width()*SF),(player_icon.get_height()*SF)))
alien_icon = pygame.image.load('Assets/Alien Ship.png')
alien_icon = pygame.transform.scale(alien_icon, ((alien_icon.get_width()*SF),(alien_icon.get_height()*SF)))
bullet_icon = pygame.image.load('Assets/bullet.png')
bullet_icon = pygame.transform.scale(bullet_icon, ((bullet_icon.get_width()*SF),(bullet_icon.get_height()*SF)))
Explosion = pygame.image.load('Assets/Explosion.png')
Explosion = pygame.transform.scale(Explosion, ((Explosion.get_width()*SF),(Explosion.get_height()*SF)))
pygame.display.set_icon(icon)

#Starting x value
FirstX = (screen.get_width()/2)-(background_img.get_width()/2)
LastX= (screen.get_width()-FirstX)

#Audio Init
Bang = pygame.mixer.Sound('Assets/Bang.mp3')
Boom = pygame.mixer.Sound('Assets/Boom.mp3')

#Main run variable
running = True

#Controller init
pygame._sdl2.controller.init()
for x in range(pygame.joystick.get_count()):
    if pygame._sdl2.controller.is_controller(x):
        ABXY = pygame._sdl2.controller.Controller(x)

#Sets the base variables for every run
def run_variables():
    global playerX, playerY, playerX_co, playerY_co, enemy_icon, enemyX, enemyY, enemyX_co, enemyY_co, spawn, Score, enemy_icon, bulletX, bulletY, bulletX_co, bulletY_co, bullet_state, Explosions
    # Player
    playerX = ((screen.get_width()/2)-(player_icon.get_width()/2))
    playerY = (screen.get_height()-170)
    playerX_co = 0
    playerY_co = 0
    # enemy
    Explosions = []
    enemy_icon = []
    enemyX = []
    enemyY = []
    enemyX_co = []
    enemyY_co = []
    #How many are spawning
    spawn = 20
    #Max Score (-10 each frame)
    Score = 1000000
    #Cords Genorator for enemies
    for i in range(spawn):
        enemy_icon.append(alien_icon)
        enemyX.append(random.randint((FirstX), (LastX-alien_icon.get_width())))
        enemyY.append(random.randint(50, 150))
        enemyX_co.append(1/((LPF*2/SF**2)/(1/(math.sqrt(1/SQLP)))))
        enemyY_co.append(alien_icon.get_height())
    # bullet
    bulletX = 0
    bulletY = (screen.get_height()-170)
    bulletX_co = 0
    bulletY_co = ((6/(math.ceil(LPF)**1.1))*(SF**3))
    bullet_state = 'reload'

#immediately runs that because it is the start of the game 
run_variables()

#Player blit function
def player(x, y):
    screen.blit(player_icon, (x, y))

#Enemy blit function
def enemy(x, y, i):
    screen.blit(enemy_icon[i], (x, y))

#Bullet blit function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_icon, (x+(player_icon.get_width()/2)-(bullet_icon.get_width()/2), y-(player_icon.get_height()/4)))

#Bullet collision function
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
while running:
    #Instead of flip, we clear the screen
    screen.fill(("black"))
    screen.blit(background_img, (FirstX, 0))   
    #Score renderer 
    ScoreT = fontS.render(str(Score), True, (240,0,0))
    ScoreR = ScoreT.get_rect()
    ScoreR.center = (((screen.get_width()/2)), 40)
    screen.blit(ScoreT, ScoreR)
    #Score Subtractor
    Score -= ((math.ceil((2/(LPF))))*10)
    #Main task Queue
    for task in pygame.event.get():
        if task.type == pygame.QUIT:
            running = False

        #Mouse left and right
        mrx, mry = pygame.mouse.get_rel()
        if mrx != 0 or mry != 0:
          mousex, mousey = pygame.mouse.get_pos()
          playerX = mousex - 30
        #Mouse buttons
        if pygame.mouse.get_pressed()[0]:
                if bullet_state == 'reload':
                    pygame.mixer.Sound.play(Bang)
                    bulletX = playerX
                    bulletY = (screen.get_height()-170)
                    fire_bullet(bulletX, bulletY)

        #Controller buttons
        if "ControllerButtonDown" in str((pygame.event.event_name(task.type))):
            if task.dict['button'] == 14:
                playerX_co = 2/LPF
            if task.dict['button'] == 13:
                playerX_co = -2/LPF
            if task.dict['button'] == 0:
              if bullet_state == 'reload':
                    pygame.mixer.Sound.play(Bang)
                    bulletX = playerX
                    bulletY = (screen.get_height()-170)
                    fire_bullet(bulletX, bulletY)
        #Controller left and right
        if "ControllerAxisMotion" in str((pygame.event.event_name(task.type))):
            #Triggers
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
            #Left Joystick
            if task.dict["axis"] == 0:
                if task.dict["value"] > 10000:
                    playerX_co = ((task.dict["value"])/5000)/LPF
                elif task.dict["value"] < -10000:
                    playerX_co = ((task.dict["value"])/5000)/LPF
                else:
                    playerX_co = 0
        #Clears the button if you let go
        if "ControllerButtonUp" in str((pygame.event.event_name(task.type))) and task.dict['button'] != 0:
            playerX_co = 0

        #Keyboard buttons
        if task.type == pygame.KEYDOWN:
            if task.key == pygame.K_LEFT:
                playerX_co = -2
            if task.key == pygame.K_RIGHT:
                playerX_co = 2
            if task.key == pygame.K_SPACE:
                if bullet_state == 'reload':
                    pygame.mixer.Sound.play(Bang)
                    bulletY = (screen.get_height()-170)
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            #Escape exits the game
            if task.key == pygame.K_ESCAPE:
                running = False
        #Clears the key if you let go
        if task.type == pygame.KEYUP:
            if task.key == pygame.K_LEFT or task.key == pygame.K_RIGHT:
                playerX_co = 0

    #Player Boundaries
    playerX += playerX_co
    if playerX <= (FirstX):
        playerX = (FirstX)
    elif playerX >= (LastX-player_icon.get_width()):
        playerX = (LastX-player_icon.get_width())

    # enemy co-ordinates
    for i in range(spawn):
        enemyX[i] += enemyX_co[i]
        if enemyX[i] <= (FirstX) or enemyX[i] >= (LastX-alien_icon.get_width()):
            if abs(enemyX_co[i]) < (5/LPF):
              enemyX_co[i] = enemyX_co[i] * -1.1
            else:
              enemyX_co[i] = enemyX_co[i] * -1
            enemyY[i] += enemyY_co[i]

        # collision
        Death = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if Death:
            #You Lose! Death Screen
            #Big transparent black box
            pygame.mixer.Sound.play(Boom)
            screen.blit(Explosion, (playerX, (screen.get_height()-170)))
            pygame.gfxdraw.box(screen, pygame.Rect(0,0,20000,20000), (0,0,0,200))
            #Drawing text
            LoseR = LoseT.get_rect()
            LoseR.center = ((screen.get_width()/2), 300)
            screen.blit(LoseT, LoseR)
            pause = True
            pygame.display.update()
            pygame.time.wait(1000)
            AgainT = fontS.render('Press Any Key to play again', True, (0,100,0))
            AgainR = AgainT.get_rect()
            AgainR.center = ((screen.get_width()/2), 500)
            screen.blit(AgainT, AgainR)
            pygame.display.update()
            #Waiting for input
            LEvent = ""
            Event = ""
            while pause:
                Event=LEvent
                LEvent = str((pygame.event.event_name(task.type)))
                for task in pygame.event.get():
                    if task.type == pygame.QUIT:
                        pause = False
                        running = False
                    if task.type == pygame.KEYDOWN:
                        if task.key == pygame.K_ESCAPE:
                            pause = False
                            running = False
                if LEvent != "" and Event != "" and LEvent != Event and LEvent == "JoyButtonDown" or LEvent == "TextInput" or LEvent == "MouseButtonDown" or LEvent == "ControllerButtonDown":
                    pause = False
                    #Again!
                    run_variables()

        #Collision detection variable
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            #If Alien is hit...
            pygame.mixer.Sound.play(Boom)
            Explosions.append([5, (bulletX, (bulletY-35))])
            bulletY = screen.get_height()
            bullet_state = 'reload'
            #If there is any more left in the spawn cue, spawn one of them now
            enemyX[i] = random.randint(((screen.get_width()/4)), (((screen.get_width()/4)*3)-15))
            enemyY[i] = random.randint(50, 150)
            #Remove 1 from the spawn cue
            spawn -= 1
        enemy(enemyX[i], enemyY[i], i)

    for i in Explosions:
        if i[0]<0:
            Explosions.remove(i)
        else:
            screen.blit(Explosion, i[1])
            i[0]-=.1

    # bullet movements
    if bulletY <= 0:
        bulletY = (screen.get_height()-170)
        bullet_state = 'reload'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_co

    player(playerX, playerY)

    pygame.display.update()

    #Win Mechanics
    if spawn == 0 and Death == False:
                screen.blit(background_img, ((screen.get_width())/4, 0)) 
                pygame.gfxdraw.box(screen, pygame.Rect(0,0,2000,2000), (0,0,0,200))
                WinR = WinT.get_rect()
                WinR.center = ((screen.get_width()/2), 300)
                screen.blit(WinT, WinR)
                Score = str(Score)
                ScoreT = fontS.render('Your Score was '+Score, True, (240,0,0))
                ScoreR = ScoreT.get_rect()
                ScoreR.center = ((screen.get_width()/2), 400)
                screen.blit(ScoreT, ScoreR)
                pygame.display.update()
                pygame.time.wait(1000)
                AgainT = fontS.render('Press Any Key to play again', True, (0,100,0))
                AgainR = AgainT.get_rect()
                AgainR.center = ((screen.get_width()/2), 500)
                screen.blit(AgainT, AgainR)
                pause = True
                pygame.display.update()
                LEvent = ""
                Event = ""
                while pause:
                    Event=LEvent
                    LEvent = str((pygame.event.event_name(task.type)))
                    for task in pygame.event.get():
                        if task.type == pygame.QUIT:
                            pause = False
                            running = False
                        if task.type == pygame.KEYDOWN:
                            if task.key == pygame.K_ESCAPE:
                                pause = False
                                running = False
                    if LEvent != "" and Event != "" and LEvent != Event and LEvent == "JoyButtonDown" or LEvent == "TextInput" or LEvent == "MouseButtonDown" or LEvent == "ControllerButtonDown":
                        pause = False
                        #Again!
                        run_variables()
screen.fill((0, 0, 0))
pygame.display.update()

pygame.quit()
sys.exit()
