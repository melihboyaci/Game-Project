import pygame
import numpy as np

import random


pygame.init()
pygame.mixer.init()


TILE_SIZE = 32

import tile_assets 
import Player as Player
import Enemy as Enemy

pygame.display.set_caption("Tile Map Test") 


# Bu fonksiyon, haritadaki yürünebilir pozisyonları bulur ve bunlardan rastgele birini döndürür.
def get_random_walkable_position(enemy_size=(4,4)):
    walkable_positions = []
    map_h, map_w = tile_assets.map_data.shape
    solid_rects = tile_assets.create_solid_rects()
    for y in range(map_h - enemy_size[1] + 1):
        for x in range(map_w - enemy_size[0] + 1):
            # Enemy'nin kaplayacağı alanı rect olarak oluştur
            enemy_rect = pygame.Rect(
                x * TILE_SIZE,
                y * TILE_SIZE,
                enemy_size[0] * TILE_SIZE,
                enemy_size[1] * TILE_SIZE
            )
            # Eğer bu alan solid_rects ile çakışıyorsa spawn etme
            collision = False
            for solid in solid_rects:
                if enemy_rect.colliderect(solid):
                    collision = True
                    break
            if not collision:
                walkable_positions.append((x, y))
    if walkable_positions:
        return random.choice(walkable_positions)
    else:
        return None




enemies= []
MAX_TOTAL_ENEMY = 200
MAX_ACTIVE_ENEMY = 10
SPAWN_INTERVAL = 2000  # ms
last_spawn_time = pygame.time.get_ticks()
total_spawned = len(enemies)


player = Player.Player(100, 100)
clock = pygame.time.Clock()
running = True
# enemies = [Enemy.Enemy(300, 100), Enemy.Enemy(500, 200), Enemy.Enemy(500, 250 )]  # Enemy nesneleri listesi


# Başlangıç Enemy spawn
for _ in range(MAX_ACTIVE_ENEMY):
    pos = get_random_walkable_position()
    if pos:
        x, y = pos
        enemies.append(Enemy.Enemy(x * TILE_SIZE, y * TILE_SIZE))

total_spawned = len(enemies)

solid_rects = tile_assets.create_solid_rects()  # Yürünemez alanları oluştur
all_characters = enemies  # Tüm karakterleri bir listeye ekle
while running:
    dt = clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Otomatik düşman spawn kontrolü ---
    if len(enemies) < MAX_ACTIVE_ENEMY and total_spawned < MAX_TOTAL_ENEMY and now - last_spawn_time > SPAWN_INTERVAL:
        pos = get_random_walkable_position()
        if pos:
            x, y = pos
            enemies.append(Enemy.Enemy(x * TILE_SIZE, y * TILE_SIZE))
            total_spawned += 1
            last_spawn_time = now

    player.handle_input(solid_rects, all_characters)
    player.attack(enemies)
    player.update()

  
    # Enemy listesini güncelle
    for enemy in enemies[:]:
        if not enemy.alive:
            enemies.remove(enemy)
        else:
            # Kendisi dışındaki tüm düşmanları topla
            other_enemies = [e for e in enemies if e is not enemy]
            # Player’ı ve diğer düşmanları tek listede birleştir
            chars = [player] + other_enemies
            enemy.update(player, solid_rects, chars)
            enemy.update_animation()
    
    tile_assets.screen.fill((0, 0, 0))
    tile_assets.draw_map()
    player.draw(tile_assets.screen)
    
    for enemy in enemies:
        enemy.draw(tile_assets.screen)

    pygame.display.update()
   

pygame.quit()
