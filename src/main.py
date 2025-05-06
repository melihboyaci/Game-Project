import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BACKGROUND_COLOR, TITLE
from sprites import Player

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Arka plan görselini yükle
background = pygame.image.load("assets/Rifle_Stage_Assets/images/map3.png").convert()

player = Player(200, 10, 5)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys, SCREEN_WIDTH, SCREEN_HEIGHT)

    screen.blit(background, (0, 0))
    player.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()