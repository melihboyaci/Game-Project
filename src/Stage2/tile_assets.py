import pygame
import random
import numpy as np

pygame.init()

TILE_SIZE = 32

screen = pygame.display.set_mode((TILE_SIZE * 40, TILE_SIZE * 22))


tileset = pygame.image.load("assets/Middle_Age_Assets/Forest_TileSet/forest_tiles.png").convert_alpha()

pool_tileset = pygame.image.load("assets/Middle_Age_Assets/Forest_TileSet/poolWB2.png").convert_alpha()

tileStufs = pygame.image.load("assets/Middle_Age_Assets/Forest_TileSet/tileStufs.png").convert_alpha()

tree_assets=pygame.image.load("assets/Middle_Age_Assets/Forest_TileSet/tree_assets.png").convert_alpha()

# Tile'ları kes
grassGround    = tileset.subsurface((0, 0, TILE_SIZE, TILE_SIZE))
flavourGrass   = tileset.subsurface((TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
flavourGrass2  = tileset.subsurface((TILE_SIZE * 2, 0, TILE_SIZE, TILE_SIZE))
flavourGrass3  = tileset.subsurface((TILE_SIZE * 3, 0, TILE_SIZE, TILE_SIZE))
flavourGrass4  = tileset.subsurface((TILE_SIZE * 4, 0, TILE_SIZE, TILE_SIZE))

littleObject  = tileset.subsurface((0, TILE_SIZE*3, TILE_SIZE, TILE_SIZE))
littleObject2  = tileset.subsurface((TILE_SIZE, TILE_SIZE*3, TILE_SIZE, TILE_SIZE))
littleObject3  = tileset.subsurface((TILE_SIZE*2, TILE_SIZE*3, TILE_SIZE, TILE_SIZE))
littleObject4  = tileset.subsurface((TILE_SIZE*3, TILE_SIZE*3, TILE_SIZE, TILE_SIZE))
littleObject5  = tileset.subsurface((TILE_SIZE*4, TILE_SIZE*3, TILE_SIZE, TILE_SIZE))
littleObject6  = tileset.subsurface((TILE_SIZE*5, TILE_SIZE*3, TILE_SIZE, TILE_SIZE))
littleObject7  = tileset.subsurface((TILE_SIZE*6, TILE_SIZE*3, TILE_SIZE, TILE_SIZE))
bigObject  = tileset.subsurface((TILE_SIZE*7, TILE_SIZE*3, TILE_SIZE*2, TILE_SIZE))
bigObject2  = tileset.subsurface((TILE_SIZE*9, TILE_SIZE*3, TILE_SIZE*2, TILE_SIZE))

giantHole  = tileset.subsurface((TILE_SIZE * 6, 0, TILE_SIZE*3, TILE_SIZE*3))
littleHole  = tileset.subsurface((TILE_SIZE * 5, 0, TILE_SIZE, TILE_SIZE))

campFire1  = tileset.subsurface((0, TILE_SIZE*5, TILE_SIZE, TILE_SIZE))
campFire2  = tileset.subsurface((TILE_SIZE, TILE_SIZE*5, TILE_SIZE, TILE_SIZE))
campFire3  = tileset.subsurface((TILE_SIZE*2, TILE_SIZE*5, TILE_SIZE, TILE_SIZE))
campFire4  = tileset.subsurface((TILE_SIZE*3, TILE_SIZE*5, TILE_SIZE, TILE_SIZE))
campFire5  = tileset.subsurface((TILE_SIZE*4, TILE_SIZE*5, TILE_SIZE, TILE_SIZE))

tree1  = tileset.subsurface((0, TILE_SIZE*6, TILE_SIZE*2, TILE_SIZE*2))
tree1_Forest  = tileset.subsurface((TILE_SIZE*2, TILE_SIZE*6, TILE_SIZE*2, TILE_SIZE*2))
tree2  = tileset.subsurface((0, TILE_SIZE*8, TILE_SIZE*2, TILE_SIZE*2))
tree2_Forest  = tileset.subsurface((0, TILE_SIZE*10, TILE_SIZE*2, TILE_SIZE*2))

pool1= tileset.subsurface((TILE_SIZE*4, TILE_SIZE*7, TILE_SIZE, TILE_SIZE))
pool2= tileset.subsurface((TILE_SIZE*5, TILE_SIZE*7, TILE_SIZE, TILE_SIZE))
pool3= tileset.subsurface((TILE_SIZE*6, TILE_SIZE*7, TILE_SIZE, TILE_SIZE))
pool4= tileset.subsurface((TILE_SIZE*4, TILE_SIZE*8, TILE_SIZE, TILE_SIZE))
pool5WithWave= tileset.subsurface((TILE_SIZE*5, TILE_SIZE*8, TILE_SIZE, TILE_SIZE))
pool6= tileset.subsurface((TILE_SIZE*6, TILE_SIZE*8, TILE_SIZE, TILE_SIZE))
pool7= tileset.subsurface((TILE_SIZE*4, TILE_SIZE*9, TILE_SIZE, TILE_SIZE))
pool8= tileset.subsurface((TILE_SIZE*5, TILE_SIZE*9, TILE_SIZE, TILE_SIZE))
pool9= tileset.subsurface((TILE_SIZE*6, TILE_SIZE*9, TILE_SIZE, TILE_SIZE))

pool5WithLessWave= tileset.subsurface((TILE_SIZE*8, TILE_SIZE*8, TILE_SIZE, TILE_SIZE))

tiles = [grassGround, flavourGrass, flavourGrass2, flavourGrass3, flavourGrass4]



poolWB1= pool_tileset.subsurface((TILE_SIZE*10,TILE_SIZE* 4, TILE_SIZE*12, TILE_SIZE*5))
poolWB2= pool_tileset.subsurface((TILE_SIZE*17,TILE_SIZE* 9, TILE_SIZE*5, TILE_SIZE*2))

tileStufs1= tileStufs.subsurface((0, 0, TILE_SIZE*3, TILE_SIZE*2))
tileStufs2= tileStufs.subsurface((0, TILE_SIZE*2, TILE_SIZE*2, TILE_SIZE))
tileStufs3= tileStufs.subsurface((0, TILE_SIZE*3, TILE_SIZE*1, TILE_SIZE*2))
tileStufs4= tileStufs.subsurface((TILE_SIZE*1, TILE_SIZE*3, TILE_SIZE*1, TILE_SIZE*2))
tileStufs5= tileStufs.subsurface((TILE_SIZE*0, TILE_SIZE*5, TILE_SIZE*2, TILE_SIZE*2))
tileStufs6= tileStufs.subsurface((TILE_SIZE*0, TILE_SIZE*7, TILE_SIZE*2, TILE_SIZE*2))
tileStufs7= tileStufs.subsurface((TILE_SIZE*0, TILE_SIZE*9, TILE_SIZE*2, TILE_SIZE*1))


tree_down=tree_assets.subsurface((0,0,TILE_SIZE*2,TILE_SIZE*1))
tree_up=tree_assets.subsurface((0,TILE_SIZE,TILE_SIZE*2,TILE_SIZE*1))
tree_right=tree_assets.subsurface((0,TILE_SIZE*2,TILE_SIZE*1,TILE_SIZE*2))
tree_left=tree_assets.subsurface((TILE_SIZE*1,TILE_SIZE*2,TILE_SIZE*1,TILE_SIZE*2))

#????
tile_dict = {
    0: {"image": grassGround, "walkable": True},
    1: {"image": flavourGrass, "walkable": True},
    2: {"image": flavourGrass2, "walkable": True},
    3: {"image": flavourGrass3, "walkable": True},
    4: {"image": flavourGrass4, "walkable": True}
}

object_dict = {
    0: {"image": None, "walkable": True, "size": (1, 1)},  # boş obje
    1: {"image": littleObject, "walkable": True, "size": (1, 1)},
    2: {"image": littleObject2, "walkable": True, "size": (1, 1)},
    3: {"image": bigObject, "walkable": False, "size": (2, 1)},
    4: {"image": tree1, "walkable": False, "size": (2, 2)},
    5: {"image": tree1_Forest, "walkable": False, "size": (2, 2)},
    6: {"image": giantHole, "walkable": False, "size": (3, 3)},
    7: {"image": littleHole, "walkable": False, "size": (1, 1)},
    8: {"image": campFire1, "walkable": False, "size": (1, 1)},
    9: {"image": campFire2, "walkable": False, "size": (1, 1)},
    10: {"image": campFire3, "walkable": False, "size": (1, 1)},
    11: {"image": campFire4, "walkable": False, "size": (1, 1)},
    12: {"image": campFire5, "walkable": False, "size": (1, 1)},
    13: {"image": tree2, "walkable": False, "size": (2, 2)},
    14: {"image": tree2_Forest, "walkable": False, "size": (2, 2)},
    15: {"image": pool1, "walkable": False, "size": (1, 1)},
    16: {"image": pool2, "walkable": False, "size": (1, 1)},
    17: {"image": pool3, "walkable": False, "size": (1, 1)},
    18: {"image": pool4, "walkable": False, "size": (1, 1)},
    19: {"image": pool5WithWave, "walkable": False, "size": (1, 1)},
    20: {"image": pool6, "walkable": False, "size": (1, 1)},
    21: {"image": pool7, "walkable": False, "size": (1, 1)},
    22: {"image": pool8, "walkable": False, "size": (1, 1)},
    23: {"image": pool9, "walkable": False, "size": (1, 1)},
    24: {"image": pool5WithLessWave, "walkable": False, "size": (1, 1)},
    25: {"image": poolWB1, "walkable": False, "size": (12, 5)},
    26: {"image": poolWB2, "walkable": False, "size": (5, 2)},
    27: {"image": tileStufs1, "walkable": False, "size": (3, 2)},
    28: {"image": tileStufs2, "walkable": False, "size": (2, 1)},
    29: {"image": tileStufs3, "walkable": False, "size": (1, 2)},
    30: {"image": tileStufs4, "walkable": False, "size": (1, 2)},
    31: {"image": tileStufs5, "walkable": False, "size": (2, 2)},
    32: {"image": tileStufs6, "walkable": False, "size": (2, 2)},
    33: {"image": tileStufs7, "walkable": False, "size": (2, 1)},
    34: {"image": tree_down, "walkable": False, "size": (2, 1)},
    35: {"image": tree_up, "walkable": False, "size": (2, 1)},
    36: {"image": tree_right, "walkable": False, "size": (1, 2)},
    37: {"image": tree_left, "walkable": False, "size": (1, 2)},
}

# Map datası
map_data = np.zeros((22, 40), dtype=int)

#Objeler için
object_data = np.zeros((22, 40), dtype=int)     # üstündeki objeler


# Zemin
map_data[:] = 0

# Birkaç zemin çeşidi
for y in range(22):
    for x in range(40):
        if random.random() < 0.07:  # %5 ihtimalle farklı bir zemin türü
            map_data[y, x] = random.randint(1, 4)  # 1 ile 4 arasında rastgele bir zemin türü
        


# Objeler
object_data[8, 5] = 1
object_data[8, 6] = 2

object_data[9, 7] = 3
object_data[10, 8] = 4


#Hole
object_data[13, 9] = 6
object_data[16, 10] = 7

#Create Forest
# Sağ tarafa ikişer tane indeksi 5 olan öğe ekle
for y in range(0, 22, 2):  # 2 satırda bir öğe ekle
    for x in range(35, 40, 2):  # Sağ tarafta 38 ve 39. sütunlara ekle
        object_data[y, x] = 5  # İndeksi 5 olan öğe

    for x in range(34, 35, 2):  
        object_data[y, x] = 4

    # for x in range(0, 4, 2):
    #     object_data[y, x] = 14

    # for x in range(3, 5, 2):
    #     object_data[y, x] = 13



object_data[4,19]=25
object_data[9,26]=26

object_data[19, 4] = 32

object_data[3, 16] = 33

#library
object_data[5,2]=29

#little forest
object_data[13, 16] = 5
object_data[12, 16] = 35
object_data[13,18]=36
object_data[15,16]=34
object_data[13,15]=37

object_data[13, 20] = 4
object_data[16, 19] = 4

object_data[18, 28] = 31
object_data[14, 29] = 27


def draw_map():
    for y in range(map_data.shape[0]):
        for x in range(map_data.shape[1]):
            tile_index = map_data[y][x]
            tile_image = tile_dict[tile_index]["image"]
            if tile_image:
                screen.blit(tile_image, (x * TILE_SIZE, y * TILE_SIZE))

    # Objeleri ayrı döngüyle çiz
    for y in range(object_data.shape[0]):
        for x in range(object_data.shape[1]):
            object_index = object_data[y][x]

            # Eğer obje boşsa veya bu hücre objenin devamıysa atla
            if object_index == 0:
                continue

            # Sadece objenin sol üst köşesini çiz
            obj_size = object_dict[object_index]["size"]
            is_top_left = True

            for j in range(obj_size[1]):
                for i in range(obj_size[0]):
                    if (0 <= y - j < object_data.shape[0] and 0 <= x - i < object_data.shape[1] 
                        and object_data[y - j][x - i] == object_index):
                        if i != 0 or j != 0:
                            is_top_left = False
            if not is_top_left:
                continue

            object_image = object_dict[object_index]["image"]
            if object_image:
                screen.blit(object_image, (x * TILE_SIZE, y * TILE_SIZE))


def create_solid_rects():
    solid_rects = []
    for y in range(object_data.shape[0]):
        for x in range(object_data.shape[1]):
            obj_id = object_data[y, x]
            if obj_id == 0:
                continue
            info = object_dict[obj_id]
            # sadece yürünemez objeler için
            if not info["walkable"]:
                w_tiles, h_tiles = info["size"]
                rect = pygame.Rect(
                    x * TILE_SIZE,
                    y * TILE_SIZE,
                    w_tiles * TILE_SIZE,
                    h_tiles * TILE_SIZE
                )
                solid_rects.append(rect)
    return solid_rects            