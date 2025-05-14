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


player = Player.Player(100, 100)
clock = pygame.time.Clock()
running = True
enemies = [Enemy.Enemy(300, 100), Enemy.Enemy(500, 200), Enemy.Enemy(500, 250 )]  # Enemy nesneleri listesi


solid_rects = tile_assets.create_solid_rects()  # Yürünemez alanları oluştur
all_characters = enemies  # Tüm karakterleri bir listeye ekle
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.handle_input(solid_rects, all_characters)

    player.attack(enemies)
    player.update()

    # for e in enemies:
    #     e.update(player)
    #     # Enemy ile player birbirine girerse itiştir:
    #     player.resolve_collision(e.rect)
    #     e.resolve_collision(player.rect)
  
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
