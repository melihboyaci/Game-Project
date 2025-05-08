import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, PLAYER_START_X, PLAYER_START_Y, PLAYER_SPEED, PLAYER_BULLETS
from sprites import Player, Block1

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Arka plan görselini yükle
background = pygame.image.load("assets/Rifle_Stage_Assets/images/map4.png").convert()

player = Player(PLAYER_START_X, PLAYER_START_Y, PLAYER_SPEED, PLAYER_BULLETS)

blocks = pygame.sprite.Group()
block1 = Block1(400, 300)
blocks.add(block1)

font = pygame.font.SysFont(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys, SCREEN_WIDTH, SCREEN_HEIGHT)

    screen.blit(background, (0, 0))
    blocks.draw(screen)
    player.draw(screen)

    # Mermi sayısını ekrana yaz
    bullet_text = font.render(f"Bullets: {player.bullets}", True, (255, 255, 255))
    screen.blit(bullet_text, (100, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()