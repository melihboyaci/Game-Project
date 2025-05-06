import pygame
from utils.animation import AnimatedSprite, load_sprite_sheet
from utils.bullet import Bullet

class Spaceship:
    def __init__(self, image_path, size, position, speed, engine_path=None, engine_size=None):
        self.frames = load_sprite_sheet(image_path, *size)
        self.sprite = AnimatedSprite(self.frames, position, frame_delay=10000)
        self.size = size
        self.position = list(position)
        self.speed = speed
        self.direction = "right"
        self.map_width = 2000  # Harita genişliği
        self.map_height = 2000

        self.bullets = []  # Mermileri saklamak için bir liste
        self.last_shot_time = 0  # Son ateş etme zamanı
        self.shoot_delay = 250  # Merminin ateşlenme gecikmesi (ms)


        # Motor efekti için
        if engine_path and engine_size:
            frames = load_sprite_sheet(engine_path, *engine_size)
            self.engine_anim = AnimatedSprite(frames, position, frame_delay=90)
        else:
            self.engine_anim = None

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.position[0] -= self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.position[0] += self.speed
            self.direction = "right"
        if keys[pygame.K_UP]:
            self.position[1] -= self.speed
        if keys[pygame.K_DOWN]:
            self.position[1] += self.speed

        # Ekranın dışına çıkmaması için sınırları kontrol et
        self.position[0] = max(0, min(self.position[0], self.map_width - self.size[0]))
        self.position[1] = max(0, min(self.position[1], self.map_height - self.size[1]))
        self.sprite.pos = tuple(self.position)
        self.sprite.update()

        for bullet in self.bullets:
            bullet.update()
            # Merminin ekran dışına çıkıp çıkmadığını kontrol et
            self.bullets = [
                b for b in self.bullets
                if 0 <= b.position[0] <= self.map_width and 0 <= b.position[1] <= self.map_height
            ] 
        
        if self.engine_anim:
            frame_width = self.engine_anim.frames[0].get_width()
            frame_height = self.engine_anim.frames[0].get_height()
            engine_pos = (
                self.position[0] + self.size[0] // 2 - frame_width // 2,
                self.position[1] + self.size[1] - frame_height // 2
            )
            self.engine_anim.pos = engine_pos
            self.engine_anim.update()


    def fire(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            bullet_x = self.position[0] + self.size[0] // 2 - self.bullets[0].size[0] // 2 if self.bullets else self.position[0] + self.size[0] // 2
            bullet_y = self.position[1] + self.size[1] // 2 - 8  # 8: mermi yüksekliğinin yarısı (örnek)
            bullet_position = (bullet_x, bullet_y)
            self.bullets.append(Bullet(bullet_position))
            self.last_shot_time = now
        pygame.mixer.Sound("assets/Space_Stage_Assets/sounds/laserfire.ogg").play()
        
    
    
    def draw(self, screen, camera_offset):

        screen_pos = (self.position[0] - camera_offset[0], self.position[1] - camera_offset[1])
        self.sprite.pos = screen_pos
        image = self.sprite.image
        if self.direction == "left":
            image = pygame.transform.flip(image, True, False)
        screen.blit(image, self.sprite.pos)
        
        if self.engine_anim:
            engine_screen_pos = (self.engine_anim.pos[0] - camera_offset[0], self.engine_anim.pos[1] - camera_offset[1])
            self.engine_anim.draw(screen, engine_screen_pos)

        for bullet in self.bullets:
            bullet_screen_pos = (bullet.position[0] - camera_offset[0], bullet.position[1] - camera_offset[1])
            screen.blit(bullet.image, bullet_screen_pos)


    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])