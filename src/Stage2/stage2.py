import pygame
import numpy as np
import Player as Player
import Enemy as Enemy

pygame.init()

TILE_SIZE = 32

screen = pygame.display.set_mode((TILE_SIZE * 30, TILE_SIZE * 20))
pygame.display.set_caption("Tile Map Test")

tileset = pygame.image.load("assets/Middle_Age_Assets/Forest_TileSet/forest_tiles.png").convert_alpha()

# Tile'ları kes
grassGround    = tileset.subsurface((0, 0, TILE_SIZE, TILE_SIZE))
flavourGrass   = tileset.subsurface((TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
flavourGrass2  = tileset.subsurface((TILE_SIZE * 2, 0, TILE_SIZE, TILE_SIZE))
flavourGrass3  = tileset.subsurface((TILE_SIZE * 3, 0, TILE_SIZE, TILE_SIZE))
flavourGrass4  = tileset.subsurface((TILE_SIZE * 4, 0, TILE_SIZE, TILE_SIZE))

tiles = [grassGround, flavourGrass, flavourGrass2, flavourGrass3, flavourGrass4]

# Map datası
map_data2 = np.zeros((20, 30), dtype=int)

def draw_map():
    for y in range(len(map_data2)):
        for x in range(len(map_data2[y])):
            tile_index = map_data2[y][x]
            screen.blit(tiles[tile_index], (x * TILE_SIZE, y * TILE_SIZE))


player = Player.Player(100, 100)
clock = pygame.time.Clock()
running = True
enemies = [Enemy.Enemy(300, 100), Enemy.Enemy(500, 200), Enemy.Enemy(1000, 1000)]  # Enemy nesneleri listesi

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.handle_input()

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
    
    screen.fill((0, 0, 0))
    draw_map()
    player.draw(screen)
    
    for enemy in enemies:
        enemy.draw(screen)

    pygame.display.update()
   

pygame.quit()
