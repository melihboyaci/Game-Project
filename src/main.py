import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    PLAYER_START_X, PLAYER_START_Y, PLAYER_SPEED, PLAYER_BULLETS,
    ENEMY_COUNT, ENEMY_MIN_DISTANCE, ENEMY_DAMAGE
)
from soldier import Player
from enemy import Enemy, EnemyManager
from collision_manager import CollisionManager
from background import Background

bullet_icon = pygame.image.load("assets/Rifle_Stage_Assets/images/bullet_icon.png")
hp_icon = pygame.image.load("assets/Rifle_Stage_Assets/images/hp_icon.png")
enemy_icon = pygame.image.load("assets/Rifle_Stage_Assets/images/enemy_icon.png")

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Arka plan ve blokları oluştur
background = Background()

player = Player(PLAYER_START_X, PLAYER_START_Y, PLAYER_SPEED, PLAYER_BULLETS)
enemy_manager = EnemyManager(num_enemies=ENEMY_COUNT, min_distance=ENEMY_MIN_DISTANCE)
enemy_manager.spawn_enemies(background.get_blocks())  # Blokları geçerek düşmanları oluştur

font = pygame.font.SysFont(None, 36)

running = True
while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    old_rect = player.rect.copy()
    old_collision_rect = player.collision_rect.copy()
    player.update(keys, SCREEN_WIDTH, SCREEN_HEIGHT)
    if getattr(player, 'death_animation_finished', False):
        running = False
    enemy_manager.update(player, background.get_blocks())

    # Çarpışma kontrolü
    if CollisionManager.check_player_block_collision(player, background.get_blocks()):
        player.rect = old_rect
        player.collision_rect = old_collision_rect

    # Düşman mermilerinin oyuncuya çarpışma kontrolü (yeni sistem)
    for enemy in enemy_manager.enemies:
        for bullet in enemy.bullet_sprites.sprites():
            if player.collision_rect.colliderect(bullet.rect):
                player.take_damage(ENEMY_DAMAGE)
                bullet.kill()

    # Oyuncunun mermilerinin düşmanlarla ve bloklarla çarpışma kontrolü
    for bullet in player.bullet_sprites.sprites():
        # Blok kontrolü
        if CollisionManager.check_bullet_block_collision(bullet, background.get_blocks()):
            bullet.kill()
            continue
        
        # Düşman kontrolü
        for enemy in enemy_manager.enemies:
            collision, damage = CollisionManager.check_bullet_enemy_collision(bullet, enemy)
            if collision:
                if enemy.take_damage(damage):
                    pass
                bullet.kill()
                break

    # Arka planı ve blokları çiz
    background.draw(screen)
    
    # Oyuncu ve düşmanları çiz
    player.draw(screen, background.get_blocks())
    enemy_manager.draw(screen, background.get_blocks())

    # Mermi ikonu ve sayısı
    screen.blit(bullet_icon, (860, 10))
    bullet_text = font.render(f"{player.bullets}", True, (255, 255, 255))
    screen.blit(bullet_text, (890, 10))  # ikonun sağına

    # Can ikonu ve sayısı
    screen.blit(hp_icon, (860, 35))
    health_text = font.render(f"{player.health}", True, (255, 255, 255))
    screen.blit(health_text, (890, 35))

    # Düşman ikonu ve sayısı
    screen.blit(enemy_icon, (860, 60))
    enemies_text = font.render(f"{enemy_manager.get_enemy_count()}", True, (255, 255, 255))
    screen.blit(enemies_text, (890, 60))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()