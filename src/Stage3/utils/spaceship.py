import pygame
from .animation import AnimatedSprite, load_sprite_sheet
from .bullet import Bullet

class Spaceship:
    def __init__(self, image_path, size, position, speed, engine_path=None, engine_powering_path=None, engine_size=None, gun_path=None, scale=1):
        self.frames = load_sprite_sheet(image_path, *size)
        self.sprite = AnimatedSprite(self.frames, position, frame_delay=10000)
        self.size = size
        self.position = list(position)
        self.speed = speed
        self.direction = "right"
        self.map_width = 2000  # Harita genişliği
        self.map_height = 2000
        self.health = 15
        self.exploading = False
        self.scale = scale
        self.gun = None
        self.gun_sprite = None
        self.gun_firing = False
        self.gun_firing_time = 10
        self.gun_firing_duration = 480  # ms
        self.exploding = False
        self.explosion_frames = load_sprite_sheet("assets/Space_Stage_Assets/sprites/spaceship/explosion.png", 64, 64)
        self.explosion_sprite = AnimatedSprite(self.explosion_frames, position, frame_delay=80)
        self.explosion_time = 0 
        self.explosion_duration = 732  


        if gun_path:
            self.gun = load_sprite_sheet(gun_path, *size)
            gun_pos = (
                self.position[0] + self.size[0] - 20,  # Gemi X + genişlik - küçük bir offset
                self.position[1] + self.size[1] - 8
            )
            self.gun_sprite = AnimatedSprite(self.gun, gun_pos, frame_delay=40)


        self.bullets = []  # Mermileri saklamak için bir liste
        self.last_shot_time = 0  # Son ateş etme zamanı
        self.shoot_delay = 400  # Merminin ateşlenme gecikmesi (ms)


        # Motor efekti için
        if engine_path and engine_size and engine_powering_path:
            self.engine_powering_frames = load_sprite_sheet(engine_powering_path, *engine_size)
            self.engine_powering_anim = AnimatedSprite(self.engine_powering_frames, position, frame_delay=100)
            self.engine_frames = load_sprite_sheet(engine_path, *engine_size)
            self.engine_anim = AnimatedSprite(self.engine_frames, position, frame_delay=100)
        else:
            self.engine_anim = None
            self.engine_powering_anim = None

    def update(self, keys):
        
        if self.exploding:
            self.explosion_sprite.pos = tuple(self.position)
            self.explosion_sprite.update()
            sound = pygame.mixer.Sound("assets/Space_Stage_Assets/sounds/explosion.wav")
            sound.set_volume(0.5)
            sound.play()

            if pygame.time.get_ticks() - self.explosion_time > self.explosion_duration:
                self.health = -99
                self.exploding = False
                return

        moving = False
        if keys[pygame.K_LEFT]:
            self.position[0] -= self.speed
            self.direction = "left"
            moving = True
        
        if keys[pygame.K_RIGHT]:
            self.position[0] += self.speed
            self.direction = "right"
            moving = True

        if keys[pygame.K_UP]:
            self.position[1] -= self.speed
            moving = True

        if keys[pygame.K_DOWN]:
            self.position[1] += self.speed
            moving = True

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
        
        self.active_engine = self.engine_powering_anim if moving else self.engine_anim
        if self.active_engine:
            frame_width = self.active_engine.frames[0].get_width()
            frame_height = self.active_engine.frames[0].get_height()
            engine_pos = (
                self.position[0] + self.size[0] // 2 - frame_width // 2 + 48,
                self.position[1] + self.size[1] - frame_height // 7 + 35
            )
            self.active_engine.pos = engine_pos
            self.active_engine.update()

    def die(self):
        self.exploding = True
        self.explosion_time = pygame.time.get_ticks()
        self.sprite.update = lambda: None  # Güncellemeyi durdur

    def fire(self):
        if self.gun_sprite:
            self.gun_firing = True
            self.gun_firing_time = pygame.time.get_ticks()
            self.gun_sprite.index = 0
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            bullet_x = self.position[0] + self.size[0] // 2 + 9
            bullet_y = self.position[1] + self.size[1] // 2 - 15  # 8: mermi yüksekliğinin yarısı (örnek)
            bullet_position = (bullet_x, bullet_y)
            if now - self.last_shot_time > self.shoot_delay:
                self.bullets.append(Bullet(
                    image_path="assets/Space_Stage_Assets/sprites/spaceship/main_ship/plasma.png",
                    size=(10, 31),
                    position=bullet_position,
                    speed=8
                ))
            self.last_shot_time = now
            pygame.mixer.Sound("assets/Space_Stage_Assets/sounds/laserfirenew.mp3").play()
        
    def draw(self, screen, camera_offset):
        if self.health <= 0 and not self.exploding:
            return
        
        screen_pos = (self.position[0] - camera_offset[0], self.position[1] - camera_offset[1])
        
        if self.exploding:
            explosion_img = self.explosion_sprite.image.copy()
            new_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
            explosion_img = pygame.transform.scale(explosion_img, new_size)
            screen.blit(explosion_img, screen_pos)
            return

        if self.gun_sprite:
            # Pozisyonu geminin sağ altına göre güncelle
            gun_x = screen_pos[0] + self.size[0] - 27  
            gun_y = screen_pos[1] + self.size[1] + 4
            self.gun_sprite.pos = (gun_x, gun_y)
            now = pygame.time.get_ticks()
            if self.gun_firing:
                self.gun_sprite.update()
                if now - self.gun_firing_time > self.gun_firing_duration:
                    self.gun_firing = False
            else:
                self.gun_sprite.index = 0
                self.gun_sprite.image = self.gun_sprite.frames[0]
            self.gun_sprite.draw(screen, self.gun_sprite.pos)
        
        self.sprite.pos = screen_pos
        image = self.sprite.image
        new_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
        image = pygame.transform.scale(image, new_size)
        if self.direction == "left":
            image = pygame.transform.flip(image, True, False)
        screen.blit(image, self.sprite.pos)

        # Motor animasyonu
        if hasattr(self, 'active_engine') and self.active_engine:
            engine_screen_pos = (self.active_engine.pos[0] - camera_offset[0], self.active_engine.pos[1] - camera_offset[1])
            image = self.active_engine.image.copy()
            new_size = (int(self.size[0] * (self.scale // 1.6)), int(self.size[1] * (self.scale // 1.6)))
            image = pygame.transform.scale(image, new_size)
            screen.blit(image, engine_screen_pos)

        # Mermiler
        for bullet in self.bullets:
            bullet_screen_pos = (bullet.position[0] - camera_offset[0], bullet.position[1] - camera_offset[1])
            bullet_image = bullet.sprite.image.copy()
            new_size = (int(bullet.size[0] * 1.5), int(bullet.size[1] * 1.5))
            bullet_image = pygame.transform.scale(bullet_image, new_size)
            screen.blit(bullet_image, bullet_screen_pos)

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    
    def take_damage(self, damage):
        # Hasar alındığında yapılacak işlemler
        self.health -= damage
        if self.health > 11:
            pass
        elif  7 <= self.health <= 11:
            self.change_ship_image("assets/Space_Stage_Assets/sprites/spaceship/main_ship/slight_damage.png", (48, 48))
        elif 3 <= self.health <= 6:
            self.change_ship_image("assets/Space_Stage_Assets/sprites/spaceship/main_ship/damaged.png", (48, 48))
        else:
            self.change_ship_image("assets/Space_Stage_Assets/sprites/spaceship/main_ship/very_damaged.png", (48, 48))
        if self.health <= 0:
            self.die()

    def change_ship_image(self, image_path, size):
        self.frames = load_sprite_sheet(image_path, *size)
        self.sprite = AnimatedSprite(self.frames, self.position, frame_delay=1000)
