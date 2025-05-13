import pygame
from utils.animation import AnimatedSprite, load_sprite_sheet
from utils.bullet import Bullet
import random
import math

class EnemySpaceship:
    def __init__(self, image_path, size, position, speed, target, engine_path=None, engine_size=None, scale=1, enemy_type="fighter"):
        self.frames = load_sprite_sheet(image_path, *size)
        self.sprite = AnimatedSprite(self.frames, position, frame_delay=100)
        self.size = size
        self.position = list(position)
        self.speed = speed
        self.target = target 
        self.bullets = []
        self.last_shot_time = 0
        self.shoot_delay = 1000  # ms
        self.destination = self.random_destination()
        self.see_distance = 600  # Görüş mesafesi
        self.health = 2
        self.explosion_frames = load_sprite_sheet("assets/Space_Stage_Assets/sprites/spaceship/enemy_fighter/fighter_destruction.png", 64, 64)
        self.explosion_sprite = AnimatedSprite(self.explosion_frames, position, frame_delay=50)
        self.exploding = False
        self.explosion_time = 0
        self.explosion_duration = 900  # ms
        self.scale = scale
        self.enemy_type = enemy_type
        self.firing = False
        self.firing_time = 0
        self.firing_duration = 1000  # ms
        self.map_width = 2000
        self.map_height = 2000


        if self.enemy_type == "torpedo":
            self.weapon_frames = load_sprite_sheet("assets/Space_Stage_Assets/sprites/spaceship/enemy_torpedo/torpedo_weapons.png", 64, 64)
            self.weapon_sprite = AnimatedSprite(self.weapon_frames, position, frame_delay=50)
        else:
            self.weapon_sprite = None


        if engine_path and engine_size:
            frames = load_sprite_sheet(engine_path, *engine_size)
            self.engine_anim = AnimatedSprite(frames, position, frame_delay=90)
        else:
            self.engine_anim = None

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.exploding = True
        self.explosion_time = pygame.time.get_ticks()
        # düşman haritadan silinir
        self.sprite.image = pygame.Surface((0, 0))  # Görünmez yap
        self.sprite.update = lambda: None  # Güncellemeyi durdur


    def random_destination(self):
        # Haritada rastgele bir hedef seç
        return [random.randint(0, 2000 - self.size[0]), random.randint(0, 2000 - self.size[1])]

    def update(self, spaceship=None):
        if self.exploding:
            self.explosion_sprite.pos = tuple(self.position)
            self.explosion_sprite.update()
            sound = pygame.mixer.Sound("assets/Space_Stage_Assets/sounds/explosion.wav")
            sound.set_volume(0.05)  # Sesin ses seviyesini ayarla
            sound.play()

            if pygame.time.get_ticks() - self.explosion_time > self.explosion_duration:
                self.health = -99
                return

        # Hedefleri belirle
        earth_dx = self.target.position[0] - self.position[0]
        earth_dy = self.target.position[1] - self.position[1]
        earth_distance = math.hypot(earth_dx, earth_dy)

        player_dx = spaceship.position[0] - self.position[0] if spaceship else 0
        player_dy = spaceship.position[1] - self.position[1] if spaceship else 0
        player_distance = math.hypot(player_dx, player_dy) if spaceship else float('inf')

        # Torpedo ise: oyuncuya yakınsa ona yönel ve ateş et, değilse dünyaya yönel
        if self.enemy_type == "torpedo" and spaceship:
            if player_distance < earth_distance and player_distance < self.see_distance:
                # Oyuncuya yönel ve ateş et
                angle = math.atan2(player_dy, player_dx)
                self.position[0] += self.speed * math.cos(angle)
                self.position[1] += self.speed * math.sin(angle)
                self.fire(angle)
            else:
                # Dünyaya yönel, ateş etme
                angle = math.atan2(earth_dy, earth_dx)
                self.position[0] += self.speed * math.cos(angle)
                self.position[1] += self.speed * math.sin(angle)
        else:
            # Diğer düşmanlar için eski davranış
            if earth_distance < self.see_distance:
                angle = math.atan2(earth_dy, earth_dx)
                self.position[0] += self.speed * math.cos(angle)
                self.position[1] += self.speed * math.sin(angle)
            else:
                dx = self.destination[0] - self.position[0]
                dy = self.destination[1] - self.position[1]
                dist = math.hypot(dx, dy)
                if dist < 10:
                    self.destination = self.random_destination()
                else:
                    angle = math.atan2(dy, dx)
                    self.position[0] += self.speed * math.cos(angle)
                    self.position[1] += self.speed * math.sin(angle)

        self.sprite.pos = tuple(self.position)
        self.sprite.update()
        
        for bullet in self.bullets:
            bullet.update()
        # Mermileri harita dışına çıkınca sil
        self.bullets = [
            b for b in self.bullets
            if 0 <= b.position[0] <= self.map_width and 0 <= b.position[1] <= self.map_height
        ]

    def fire(self, angle):
        if self.enemy_type == "torpedo":
            now = pygame.time.get_ticks()
            if now - self.last_shot_time > self.shoot_delay:
                bullet_x = self.position[0] + self.size[0] // 2
                bullet_y = self.position[1] + self.size[1] // 2
                if self.enemy_type == "torpedo":
                    bullet = Bullet(
                        image_path="assets/Space_Stage_Assets/sprites/spaceship/enemy_torpedo/torpedo_bullet.png",
                        size=(9, 24),
                        position=(bullet_x, bullet_y),
                        speed=10
                    )
                    self.firing = True
                    self.firing_time = now
                    bullet.speed_x = bullet.speed * math.cos(angle)
                    bullet.speed_y = bullet.speed * math.sin(angle)
                    bullet.update = lambda: (
                        setattr(bullet, 'position', [bullet.position[0] + bullet.speed_x, bullet.position[1] + bullet.speed_y])
                    )
                    self.bullets.append(bullet)
                    self.last_shot_time = now
                else:
                    self.firing = False
                    bullet = Bullet(
                        image_path="assets/Space_Stage_Assets/sprites/spaceship/bullet.png",
                        size=(12, 21),
                        position=(bullet_x, bullet_y),
                        speed=10
                    )
                
            
            # Mermiye yön ver
            

    def draw(self, screen, camera_offset):
        screen_pos = (self.position[0] - camera_offset[0], self.position[1] - camera_offset[1])
        
        if self.exploding:
            explosion_img = self.explosion_sprite.image.copy()
            new_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
            explosion_img = pygame.transform.scale(explosion_img, new_size)
            explosion_img = pygame.transform.rotate(explosion_img, 180)
            screen.blit(explosion_img, screen_pos)
            return

        self.sprite.pos = screen_pos
        image = self.sprite.image.copy()
        new_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
        image = pygame.transform.scale(image, new_size)
        image = pygame.transform.rotate(image, 180)
        screen.blit(image, screen_pos)

        if self.engine_anim:
            frame_width = self.engine_anim.frames[0].get_width()
            frame_height = self.engine_anim.frames[0].get_height()
            engine_img = self.engine_anim.image.copy()
            engine_img = pygame.transform.scale(engine_img, (frame_width * self.scale, frame_height * self.scale))
            engine_img = pygame.transform.rotate(engine_img, 180)
            engine_pos = (
                screen_pos[0] + new_size[0] // 2 - int(frame_width * self.scale) // 2,
                screen_pos[1] + self.size[1] - frame_height 
            )
            screen.blit(engine_img, engine_pos)
            self.engine_anim.update()

        if self.enemy_type == "torpedo" and self.firing:
            if pygame.time.get_ticks() - self.firing_time < self.firing_duration:
                weapon_img = self.weapon_sprite.image.copy()
                new_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
                weapon_img = pygame.transform.scale(weapon_img, new_size)
                weapon_img = pygame.transform.rotate(weapon_img, 180)
    
                screen.blit(weapon_img, screen_pos)
                self.weapon_sprite.update()
            else:
                self.firing = False
        
        for bullet in self.bullets:
            bullet_screen_pos = (bullet.position[0] - camera_offset[0], bullet.position[1] - camera_offset[1])
            screen.blit(bullet.sprite.image, bullet_screen_pos)

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])