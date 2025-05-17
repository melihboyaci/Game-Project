import pygame
import math
from settings import SPRITE_SCALE, SCREEN_WIDTH, SCREEN_HEIGHT

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
        # Ekran sınırları kontrolü
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()
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

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/tower.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width(), original_image.get_height()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collidable = True

class Tower2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/tower2.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width(), original_image.get_height()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collidable = True

class Ruin1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/ruin1.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width(), original_image.get_height()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collidable = True

class Ruin2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/ruin2.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width(), original_image.get_height()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collidable = True

class Ruin3(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/ruin3.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width(), original_image.get_height()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collidable = True

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=2, on_finish=None):
        super().__init__()
        self.frames_open = self.load_frames('assets/portal_assets/Green_Portal_open.png', scale)
        self.frames_idle = self.load_frames('assets/portal_assets/Green_Portal_idle.png', scale)
        self.frames_close = self.load_frames('assets/portal_assets/Green_Portal_close.png', scale)
        self.state = 'opening'  # 'opening', 'idle', 'closing', 'finished'
        self.frame_index = 0
        self.frame_timer = 0
        self.animation_speed = 0.2
        self.image = self.frames_open[0]
        self.rect = self.image.get_rect(center=(x, y))
        # Ortalanmış 30x30'luk collision rect, 20 piksel sağa kaydırılmış
        self.collision_rect = pygame.Rect(0, 0, 30, 30)
        self.collision_rect.center = self.rect.center
        self.collision_rect.x += 120
        self.on_finish = on_finish
        # Portal idle sesini yükle
        self.idle_sound = pygame.mixer.Sound('assets/Rifle_Stage_Assets/sounds/portal_idle.mp3')
        self.idle_sound_channel = None
        self.idle_sound_playing = False
        # Açılış ve kapanış sesleri
        self.open_sound = pygame.mixer.Sound('assets/Rifle_Stage_Assets/sounds/portal_open.mp3')
        self.close_sound = pygame.mixer.Sound('assets/Rifle_Stage_Assets/sounds/portal_close.mp3')
        self.open_sound_played = False
        self.close_sound_played = False

    def load_frames(self, path, scale):
        img = pygame.image.load(path).convert_alpha()
        frame_width = img.get_width() // 8  # 8 frames per row
        frame_height = img.get_height()
        frames = [pygame.transform.scale(
            img.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)),
            (frame_width * scale, frame_height * scale)
        ) for i in range(8)]
        return frames

    def update(self):
        self.frame_timer += self.animation_speed
        # Her frame'de collision_rect merkezini güncelle ve sağa kaydır
        self.collision_rect.center = self.rect.center
        self.collision_rect.x += 120
        if self.state == 'opening':
            # Açılış sesi bir kez çal
            if not self.open_sound_played:
                self.open_sound.play()
                self.open_sound_played = True
            if self.frame_timer >= 1:
                self.frame_index += 1
                self.frame_timer = 0
            if self.frame_index >= len(self.frames_open):
                self.state = 'idle'
                self.frame_index = 0
                # Sesleri sıfırla
                self.open_sound_played = False  # Bir sonraki açılış için sıfırla
                self.close_sound_played = False  # Kapanıştan döndüyse sıfırla
            else:
                self.image = self.frames_open[min(self.frame_index, len(self.frames_open)-1)]
        elif self.state == 'idle':
            if self.frame_timer >= 1:
                self.frame_index += 1
                self.frame_timer = 0
            self.image = self.frames_idle[self.frame_index % len(self.frames_idle)]
            # Idle ses kontrolü
            if not self.idle_sound_playing:
                self.idle_sound_channel = self.idle_sound.play(-1)  # Döngüde çal
                self.idle_sound_playing = True
        elif self.state == 'closing':
            # Kapanış sesi bir kez çal
            if not self.close_sound_played:
                self.close_sound.play()
                self.close_sound_played = True
            if self.frame_timer >= 1:
                self.frame_index += 1
                self.frame_timer = 0
            if self.frame_index >= len(self.frames_close):
                self.state = 'finished'
                # Sesleri sıfırla
                self.close_sound_played = False  # Bir sonraki kapanış için sıfırla
                self.open_sound_played = False  # Açılıştan döndüyse sıfırla
                if self.on_finish:
                    self.on_finish()
            else:
                self.image = self.frames_close[min(self.frame_index, len(self.frames_close)-1)]
            # Idle ses kontrolü
            if self.idle_sound_playing:
                if self.idle_sound_channel:
                    self.idle_sound_channel.stop()
                self.idle_sound_playing = False

    def start_closing(self):
        self.state = 'closing'
        self.frame_index = 0
        self.frame_timer = 0
        self.close_sound_played = False  # Kapanış başında flag sıfırla

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)