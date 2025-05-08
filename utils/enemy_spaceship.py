import pygame
from utils.animation import AnimatedSprite, load_sprite_sheet
from utils.bullet import Bullet
import random
import math

class EnemySpaceship:
    def __init__(self, image_path, size, position, speed, target, engine_path=None, engine_size=None):
        self.frames = load_sprite_sheet(image_path, *size)
        self.sprite = AnimatedSprite(self.frames, position, frame_delay=100)
        self.size = size
        self.position = list(position)
        self.speed = speed
        self.target = target  # Player spaceship referansı
        self.bullets = []
        self.last_shot_time = 0
        self.shoot_delay = 1000  # ms
        self.destination = self.random_destination()
        self.see_distance = 400  # Görüş mesafesi
        self.health = 3
        self.explosion_frames = load_sprite_sheet("assets/Space_Stage_Assets/sprites/spaceship/explosion.png", 65, 64)
        self.explosion_sprite = AnimatedSprite(self.explosion_frames, position, frame_delay=80)
        self.exploding = False
        self.explosion_time = 0
        self.explosion_duration = 720  # ms

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

    def update(self):
        if self.exploding:
            self.explosion_sprite.pos = tuple(self.position)
            self.explosion_sprite.update()
            sound = pygame.mixer.Sound("assets/Space_Stage_Assets/sounds/explosion.wav")
            sound.set_volume(0.07)  # Sesin ses seviyesini ayarla
            sound.play()

            if pygame.time.get_ticks() - self.explosion_time > self.explosion_duration:
                self.health = -99
                return
        # Eğer oyuncu görüş mesafesinde ise ona yönel ve ateş et
        dx = self.target.position[0] - self.position[0]
        dy = self.target.position[1] - self.position[1]
        distance = math.hypot(dx, dy)
        if distance < self.see_distance:
            # Oyuncuya yönel
            angle = math.atan2(dy, dx)
            self.position[0] += self.speed * math.cos(angle)
            self.position[1] += self.speed * math.sin(angle)
            #self.fire(angle)
        else:
            # Rastgele hedefe git
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
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            bullet_x = self.position[0] + self.size[0] // 2
            bullet_y = self.position[1] + self.size[1] // 2
            bullet = Bullet((bullet_x, bullet_y))
            # Mermiye yön ver
            bullet.speed_x = 10 * math.cos(angle)
            bullet.speed_y = 10 * math.sin(angle)
            bullet.update = lambda: (
                setattr(bullet, 'position', [bullet.position[0] + bullet.speed_x, bullet.position[1] + bullet.speed_y])
            )
            self.bullets.append(bullet)
            self.last_shot_time = now

    def draw(self, screen, camera_offset):
        screen_pos = (self.position[0] - camera_offset[0], self.position[1] - camera_offset[1])
        
        if self.exploding:
            self.explosion_sprite.draw(screen, screen_pos)
            return

        self.sprite.pos = screen_pos
        image = self.sprite.image.copy()
        screen.blit(image, screen_pos)
        for bullet in self.bullets:
            bullet_screen_pos = (bullet.position[0] - camera_offset[0], bullet.position[1] - camera_offset[1])
            screen.blit(bullet.image, bullet_screen_pos)

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])