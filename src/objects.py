import pygame
import math
from settings import PLAYER_BULLET_SPEED, SPRITE_SCALE

class Block1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/Block1.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width(), original_image.get_height()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collidable = True

class Block2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/Block2.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width(), original_image.get_height()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collidable = True
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos, speed):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/images/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (18.5*SPRITE_SCALE/1.5, 3*SPRITE_SCALE/1.5))
        self.rect = pygame.Rect(0, 0, 18.5*SPRITE_SCALE/1.5, 3*SPRITE_SCALE/1.5)
        self.rect.center = start_pos
        self.speed = speed
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        self.dir_x = dx / distance if distance != 0 else 0
        self.dir_y = dy / distance if distance != 0 else 0
        self.end_pos = end_pos
        self.start_pos = start_pos
        self.traveled = 0
        self.max_distance = distance
        """ print(f"Bullet created at {start_pos} towards {end_pos}")"""

    def update(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed
        self.traveled += self.speed
        """ print(f"Bullet at {self.rect.topleft}, traveled: {self.traveled}/{self.max_distance}") """
        # Hedefe ulaştıysa sprite'ı öldür
        if self.traveled >= self.max_distance:
            """ print("Bullet killed (reached max distance)") """   
            self.kill() 

class Rock1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/rock1.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width(), original_image.get_height()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collidable = False

class Rock2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/rock2.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width(), original_image.get_height()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collidable = False

class Rock3(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/rock3.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width(), original_image.get_height()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collidable = False

class Stump(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/stump.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width(), original_image.get_height()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collidable = True
class Tree1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/tree1.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width(), original_image.get_height()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collidable = False