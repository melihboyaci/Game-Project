import pygame
import numpy as np
import Player as Player
import Enemy as Enemy

pygame.init()

TILE_SIZE = 32

screen = pygame.display.set_mode((TILE_SIZE * 30, TILE_SIZE * 20))
pygame.display.set_caption("Tile Map Test")

tileset = pygame.image.load("assets/Forest_TileSet/forest_tiles.png").convert_alpha()

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
enemy=Enemy.Enemy(200, 100)
enemy2=Enemy.Enemy(300, 100)

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.handle_input()

    
    player.update_animation()
    enemy.update_animation()
    enemy2.update_animation()

    screen.fill((0, 0, 0))
    draw_map()
    player.draw(screen)
    enemy.draw(screen)
    enemy2.draw(screen)
    pygame.display.update()

pygame.quit()
