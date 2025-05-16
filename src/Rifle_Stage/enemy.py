import pygame
import random
import os
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SPEED, ENEMY_BULLETS, ENEMY_HEALTH,
    ENEMY_DETECTION_RANGE, ENEMY_FIRE_RANGE, ENEMY_FIRE_COOLDOWN,
    ENEMY_DAMAGE, ENEMY_VERTICAL_THRESHOLD, DEATH_ANIMATION_SPEED, SPRITE_SCALE,
    BULLET_MAX_DISTANCE, ENEMY_BULLET_SPEED
)
from soldier import Player
from objects import Bullet

class Enemy(Player):
    ENEMY_FIRE_SOUND = None  # Sadece bir kez yüklenecek
    def __init__(self, x, y, speed, bullets):
        super().__init__(x, y, speed, bullets)
        
        # Düşman için kesilmiş sprite'ı kullan
        base_path = "assets/Rifle_Stage_Assets/sprites/enemy/rifle/"
        # Yeni sprite sheetler
        self.spritesheet_run = pygame.image.load(os.path.join(base_path, "run.png")).convert_alpha()
        self.spritesheet_fire = pygame.image.load(os.path.join(base_path, "FIRE.png")).convert_alpha()
        self.spritesheet_reload = pygame.image.load(os.path.join(base_path, "reload.png")).convert_alpha()
        self.spritesheet_idle = pygame.image.load(os.path.join(base_path, "soldier-rifle.png")).convert_alpha()
        self.spritesheet_damaged = pygame.image.load(os.path.join(base_path, "damaged.png")).convert_alpha()
        self.spritesheet_death = pygame.image.load(os.path.join(base_path, "death.png")).convert_alpha()

        self.frame_width = 102
        self.frame_height = 36

        self.num_frames_run = self.spritesheet_run.get_width() // self.frame_width
        self.num_frames_fire = self.spritesheet_fire.get_width() // self.frame_width
        self.num_frames_reload = self.spritesheet_reload.get_width() // self.frame_width
        self.num_frames_idle = self.spritesheet_idle.get_width() // self.frame_width
        self.num_frames_damaged = self.spritesheet_damaged.get_width() // self.frame_width
        self.num_frames_death = self.spritesheet_death.get_width() // self.frame_width

        # Run animasyon kareleri
        self.frames_run_right = [
            pygame.transform.scale(
                self.spritesheet_run.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)),
                (self.frame_width * SPRITE_SCALE, self.frame_height * SPRITE_SCALE)
            ) for i in range(self.num_frames_run)
        ]
        self.frames_run_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_run_right]

        # Fire animasyon kareleri
        self.frames_fire_right = [
            pygame.transform.scale(
                self.spritesheet_fire.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)),
                (self.frame_width * SPRITE_SCALE, self.frame_height * SPRITE_SCALE)
            ) for i in range(self.num_frames_fire)
        ]
        self.frames_fire_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_fire_right]

        # Reload animasyon kareleri
        self.frames_reload_right = [
            pygame.transform.scale(
                self.spritesheet_reload.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)),
                (self.frame_width * SPRITE_SCALE, self.frame_height * SPRITE_SCALE)
            ) for i in range(self.num_frames_reload)
        ]
        self.frames_reload_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_reload_right]

        # Idle animasyon kareleri
        self.frames_idle_right = [
            pygame.transform.scale(
                self.spritesheet_idle.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)),
                (self.frame_width * SPRITE_SCALE, self.frame_height * SPRITE_SCALE)
            ) for i in range(self.num_frames_idle)
        ]
        self.frames_idle_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_idle_right]

        # Damaged animasyon kareleri
        self.frames_damaged_right = [
            pygame.transform.scale(
                self.spritesheet_damaged.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)),
                (self.frame_width * SPRITE_SCALE, self.frame_height * SPRITE_SCALE)
            ) for i in range(self.num_frames_damaged)
        ]
        self.frames_damaged_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_damaged_right]

        # Death animasyon kareleri
        self.frames_death_right = [
            pygame.transform.scale(
                self.spritesheet_death.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)),
                (self.frame_width * SPRITE_SCALE, self.frame_height * SPRITE_SCALE)
            ) for i in range(self.num_frames_death)
        ]
        self.frames_death_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_death_right]

        # Düşman özellikleri
        self.health = ENEMY_HEALTH
        self.detection_range = ENEMY_DETECTION_RANGE
        self.fire_range = ENEMY_FIRE_RANGE
        self.last_fire_time = 0
        self.fire_cooldown = ENEMY_FIRE_COOLDOWN
        self.damage = ENEMY_DAMAGE

        # Hasar animasyonu için değişkenler
        self.damaged = False
        self.damaged_frame = 0
        self.damaged_timer = 0
        self.damaged_duration = 500  # Hasar animasyonunun süresi (ms)
        self.last_damage_time = 0

        # Düşman karakterinin gerçek boyutu ve offseti (oyuncu ile aynı)
        self.karakter_genislik = 11*SPRITE_SCALE
        self.karakter_yukseklik = 22*SPRITE_SCALE
        self.karakter_offset_x = 10*SPRITE_SCALE
        self.karakter_offset_y = 9*SPRITE_SCALE

        self.collision_rect = pygame.Rect(
            self.rect.left + self.karakter_offset_x,
            self.rect.top + self.karakter_offset_y,
            self.karakter_genislik,
            self.karakter_yukseklik
        )
        print(f"Düşman oluşturuldu! Başlangıç canı: {self.health}")

        self.bullet_sprites = pygame.sprite.Group()

        # Death animasyonu için değişkenler
        self.dead = False
        self.death_frame = 0
        self.death_timer = 0
        self.death_animation_speed = DEATH_ANIMATION_SPEED

    def take_damage(self, damage):
        """Düşman hasar aldığında çağrılır"""
        current_time = pygame.time.get_ticks()
        # --- CAN AZALTMA ---
        self.health = max(0, self.health - damage)  # Can 0'ın altına düşmesin
        print(f"Düşman hasar aldı! Alınan hasar: {damage} | Kalan can: {self.health}")
        if self.health <= 0:
            self.dead = True
            self.death_frame = 0
            self.death_timer = 0
            self.firing = False
            self.moving = False
            self.reloading = False
            return True
        # --- ANİMASYON ---
        if current_time - self.last_damage_time > self.damaged_duration:
            self.damaged = True
            self.damaged_frame = 0
            self.damaged_timer = 0
            self.last_damage_time = current_time
        return False

    def update(self, player, blocks):
        self.bullet_sprites.update()  # Mermiler her durumda sadece bir kez güncellenir
        # Öncelikle ölüm animasyonu kontrolü
        if self.dead:
            self.death_timer += self.death_animation_speed
            if self.death_timer >= 1:
                self.death_frame += 1
                self.death_timer = 0
            if self.death_frame >= self.num_frames_death:
                self.kill()
                return
            if self.facing_right:
                self.image = self.frames_death_right[min(self.death_frame, self.num_frames_death-1)]
            else:
                self.image = self.frames_death_left[min(self.death_frame, self.num_frames_death-1)]
            return

        # Eğer düşman öldüyse güncelleme yapma
        if self.health <= 0:
            return

        current_time = pygame.time.get_ticks()

        # Hasar animasyonu kontrolü
        if self.damaged:
            self.damaged_timer += self.animation_speed * 2
            if self.damaged_timer >= 1:
                self.damaged_frame += 1
                self.damaged_timer = 0
            if self.damaged_frame >= self.num_frames_damaged:
                self.damaged = False
                self.damaged_frame = 0
            # Hasar animasyon karesi seç
            if self.facing_right:
                self.image = self.frames_damaged_right[min(self.damaged_frame, self.num_frames_damaged-1)]
            else:
                self.image = self.frames_damaged_left[min(self.damaged_frame, self.num_frames_damaged-1)]
            return  # Hasar animasyonu sırasında diğer animasyonları oynatma

        # Oyuncuya olan mesafeyi hesapla
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5
        # Oyuncuya doğru yönel
        self.facing_right = dx > 0
        # Ateş etme kontrolü (sadece y ekseninde yakın olduğunda)
        if abs(dy) < ENEMY_VERTICAL_THRESHOLD and distance <= self.fire_range and current_time - self.last_fire_time > self.fire_cooldown:
            self.firing = True
            self.fire_frame = 0
            self.fire_timer = 0
            self.last_fire_time = current_time
            # Mermi sprite'ı oluştur
            if self.facing_right:
                start_pos = (self.rect.left + 26*SPRITE_SCALE, self.rect.top + 18*SPRITE_SCALE)
                step = 1
            else:
                start_pos = (self.rect.left -10*SPRITE_SCALE, self.rect.top + 18*SPRITE_SCALE)
                step = -1
            max_length = BULLET_MAX_DISTANCE
            end_pos = (start_pos[0] + step * max_length, start_pos[1])
            if blocks is not None:
                for i in range(max_length):
                    test_x = int(start_pos[0] + step * i)
                    test_y = int(start_pos[1])
                    for block in blocks:
                        if block.collidable and block.rect.collidepoint(test_x, test_y):
                            end_pos = (test_x, test_y)
                            break
                    else:
                        continue
                    break
            self.bullet_sprites.add(Bullet(start_pos, end_pos, ENEMY_BULLET_SPEED))
            # Sesi ilk ateş anında yükle ve çal
            if Enemy.ENEMY_FIRE_SOUND is None:
                Enemy.ENEMY_FIRE_SOUND = pygame.mixer.Sound('assets/Rifle_Stage_Assets/sounds/ak_new.wav')
            Enemy.ENEMY_FIRE_SOUND.play()
        # --- Animasyon güncelle ---
        if self.firing:
            self.fire_timer += self.animation_speed * 2
            if self.fire_timer >= 1:
                self.fire_frame += 1
                self.fire_timer = 0
            if self.fire_frame >= self.num_frames_fire:
                self.firing = False
                self.fire_frame = 0
            # Fire animasyon karesi seç
            if self.facing_right:
                self.image = self.frames_fire_right[min(self.fire_frame, self.num_frames_fire-1)]
            else:
                self.image = self.frames_fire_left[min(self.fire_frame, self.num_frames_fire-1)]
        else:
            if self.moving:
                self.frame_timer += self.animation_speed
                if self.frame_timer >= 1:
                    self.current_frame = (self.current_frame + 1) % self.num_frames_run
                    self.frame_timer = 0
            else:
                self.current_frame = 0  # Duran kare
            if self.facing_right:
                self.image = self.frames_run_right[self.current_frame]
            else:
                self.image = self.frames_run_left[self.current_frame]
        # Çarpışma kutusunu güncelle
        self.collision_rect.topleft = (
            self.rect.left + self.karakter_offset_x,
            self.rect.top + self.karakter_offset_y
        )

    def draw(self, surface, blocks=None):
        if not self.facing_right:
            surface.blit(self.image, (self.rect.x - 75*SPRITE_SCALE, self.rect.y))
        else:
            surface.blit(self.image, self.rect.topleft)
        # Düşman mermilerini çiz
        self.bullet_sprites.draw(surface)

class EnemyManager:
    def __init__(self, num_enemies=3, min_distance=200):
        self.enemies = pygame.sprite.Group()
        self.num_enemies = num_enemies
        self.min_distance = min_distance

    def is_valid_position(self, x, y, blocks=None):
        """Yeni düşman pozisyonunun geçerli olup olmadığını kontrol et"""
        # Ekran sınırları kontrolü
        if x < 30*SPRITE_SCALE or x > SCREEN_WIDTH - 30*SPRITE_SCALE or y < 30*SPRITE_SCALE or y > SCREEN_HEIGHT - 30*SPRITE_SCALE:
            return False
        
        # Diğer düşmanlarla mesafe kontrolü
        for enemy in self.enemies:
            dx = enemy.rect.centerx - x
            dy = enemy.rect.centery - y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance < self.min_distance:
                return False
        
        # Bloklarla çakışma kontrolü
        if blocks:
            # Güncel çarpışma kutusu boyutları ve offsetiyle test_rect oluştur
            karakter_genislik = 9*SPRITE_SCALE
            karakter_yukseklik = 18*SPRITE_SCALE
            karakter_offset_x = 10*SPRITE_SCALE
            karakter_offset_y = 10*SPRITE_SCALE
            test_rect = pygame.Rect(x + karakter_offset_x, y + karakter_offset_y, karakter_genislik, karakter_yukseklik)
            for block in blocks:
                if test_rect.colliderect(block.rect):
                    return False
        
        return True

    def spawn_enemies(self, blocks=None):
        """Düşmanları rastgele konumlarda oluştur"""
        for _ in range(self.num_enemies):
            attempts = 0
            max_attempts = 50  # Maksimum deneme sayısı
            
            while attempts < max_attempts:
                x = random.randint(25, SCREEN_WIDTH - 25)
                y = random.randint(25, SCREEN_HEIGHT - 25)
                if self.is_valid_position(x, y, blocks):
                    enemy = Enemy(x, y, ENEMY_SPEED, ENEMY_BULLETS)
                    self.enemies.add(enemy)
                    break
                attempts += 1
            
            if attempts >= max_attempts:
                print("Uyarı: Düşman için uygun konum bulunamadı!")

    def update(self, player, blocks):
        """Tüm düşmanları güncelle"""
        for enemy in self.enemies:
            enemy.update(player, blocks)

    def draw(self, surface, blocks):
        """Tüm düşmanları çiz"""
        for enemy in self.enemies:
            enemy.draw(surface, blocks)

    def get_enemy_count(self):
        """Kalan düşman sayısını döndür"""
        return len(self.enemies)