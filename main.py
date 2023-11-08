
ALIEN_SPEED = 2  # Smaller is faster
ALIEN_COUNT = 3




import pygame
import random
import sys
from pygame.locals import QUIT

# Initialize Pygame and set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Shoot the Aliens!')
WIDTH, HEIGHT = DISPLAYSURF.get_size()
GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)

# Load and resize images
SPACESHIP_ORIG = pygame.image.load('spaceship.png').convert_alpha()
ALIEN_ORIG = pygame.image.load('alien.png').convert_alpha()
SPACESHIP = pygame.transform.scale(SPACESHIP_ORIG, (50, 50))
ALIEN = pygame.transform.scale(ALIEN_ORIG, (50, 50))

# Variables
player_x, player_y = WIDTH // 2, HEIGHT - 100
aliens = [(random.randint(0, WIDTH), random.randint(-HEIGHT, 0))
          for _ in range(ALIEN_COUNT)]
bullets = []

# Main loop
clock = pygame.time.Clock()
game_over = False
while True:
  clock.tick(30)
  for event in pygame.event.get():
    if event.type == QUIT or (event.type == pygame.KEYDOWN
                              and event.key == pygame.K_ESCAPE):
      pygame.quit()
      sys.exit()

  if not game_over:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      player_x -= 5
    if keys[pygame.K_RIGHT]:
      player_x += 5
    if keys[pygame.K_SPACE]:
      bullets.append([player_x, player_y])

    # Update bullets and aliens
    bullets = [[x, y - 5] for x, y in bullets if y > 0]
    aliens = [(x, y + ALIEN_SPEED) if y < HEIGHT else
              (random.randint(0, WIDTH), 0) for x, y in aliens]

    # Collision check: bullets and aliens
    for ax, ay in aliens:
      for bx, by in bullets:
        if ax < bx < ax + 50 and ay < by < ay + 50:
          if (ax, ay) in aliens:
            aliens.remove((ax, ay))
            aliens.append((random.randint(0, WIDTH), 0))
          if (bx, by) in bullets:
            bullets.remove([bx, by])

    # Collision check: spaceship and aliens
    for ax, ay in aliens:
      if player_x < ax < player_x + 50 and player_y < ay < player_y + 50:
        game_over = True
        break

    # Drawing
    DISPLAYSURF.fill((0, 0, 0))
    DISPLAYSURF.blit(SPACESHIP, (player_x, player_y))
    for ax, ay in aliens:
      DISPLAYSURF.blit(ALIEN, (ax, ay))
    for bx, by in bullets:
      pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (bx, by, 5, 10))

    pygame.display.update()

  else:
    game_over_label = GAME_OVER_FONT.render("Game Over", 1, (255, 0, 0))
    DISPLAYSURF.blit(game_over_label,
                     (WIDTH // 2 - game_over_label.get_width() // 2,
                      HEIGHT // 2 - game_over_label.get_height() // 2))

    pygame.display.update()
