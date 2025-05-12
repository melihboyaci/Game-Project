import pygame
import numpy as np

import random


pygame.init()

TILE_SIZE = 32

import tile_assets 
import Player as Player
import Enemy as Enemy 


pygame.display.set_caption("Tile Map Test")




# #yürünebilirlik kontrolü
# # (x, y) koordinatındaki tile ve object'in yürünebilirliğini kontrol eder
# def is_walkable(x, y):
#     if x < 0 or y < 0 or x >= map_data.shape[1] or y >= map_data.shape[0]:
#         return False
#     tile_walkable = tile_assets.tile_dict[map_data[y][x]]["walkable"]
#     object_walkable = tile_assets.object_dict[object_data[y][x]]["walkable"]
#     return tile_walkable and object_walkable



player = Player.Player(100, 100)
clock = pygame.time.Clock()
running = True
enemies = [Enemy.Enemy(300, 100), Enemy.Enemy(500, 200), Enemy.Enemy(1000, 1000)]  # Enemy nesneleri listesi


solid_rects = tile_assets.create_solid_rects()  # Yürünemez alanları oluştur

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.handle_input(solid_rects)

    player.attack(enemies)
    player.update()

    # for e in enemies:
    #     e.update(player)
    #     # Enemy ile player birbirine girerse itiştir:
    #     player.resolve_collision(e.rect)
    #     e.resolve_collision(player.rect)
  
    # Enemy listesini güncelle
    for enemy in enemies[:]:  # Listeyi kopyalayarak iterate edin
        if not enemy.alive:  # Eğer enemy hayatta değilse
            enemies.remove(enemy)  # Listeden kaldır
        else:
            enemy.update(player)
            enemy.update_animation()
    
    tile_assets.screen.fill((0, 0, 0))
    tile_assets.draw_map()
    player.draw(tile_assets.screen)
    
    for enemy in enemies:
        enemy.draw(tile_assets.screen)

    pygame.display.update()
   

pygame.quit()
