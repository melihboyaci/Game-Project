import pygame
from settings import (
    PLAYER_FIRE_COOLDOWN, PLAYER_HEALTH, DEATH_ANIMATION_SPEED,
    SPRITE_SCALE, BULLET_MAX_DISTANCE
)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, bullets):
        super().__init__()
        
        # Run sprite sheet
        self.spritesheet_run = pygame.image.load("assets/Rifle_Stage_Assets/sprites/soldier/rifle/run.png").convert_alpha()
        # Fire sprite sheet
        self.spritesheet_fire = pygame.image.load("assets/Rifle_Stage_Assets/sprites/soldier/rifle/fire(no_fx_new).png").convert_alpha()
        # Reload sprite sheet
        self.spritesheet_reload = pygame.image.load("assets/Rifle_Stage_Assets/sprites/soldier/rifle/reload.png").convert_alpha()
        # Damaged sprite sheet
        self.spritesheet_damaged = pygame.image.load("assets/Rifle_Stage_Assets/sprites/soldier/rifle/damaged.png").convert_alpha()
        # Death sprite sheet
        self.spritesheet_death = pygame.image.load("assets/Rifle_Stage_Assets/sprites/soldier/rifle/death.png").convert_alpha()

        self.frame_width = 102  # Her bir karenin genişliği
        self.frame_height = 36  # Her bir karenin yüksekliği

        self.num_frames_run = self.spritesheet_run.get_width() // self.frame_width
        self.num_frames_fire = self.spritesheet_fire.get_width() // self.frame_width
        self.num_frames_reload = self.spritesheet_reload.get_width() // self.frame_width
        self.num_frames_damaged = self.spritesheet_damaged.get_width() // self.frame_width
        self.num_frames_death = self.spritesheet_death.get_width() // self.frame_width
        self.bullets = bullets

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

        self.current_frame = 0
        self.animation_speed = 0.15
        self.frame_timer = 0

        self.image = self.frames_run_right[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.facing_right = True
        self.moving = False

        self.firing = False
        self.fire_frame = 0
        self.fire_timer = 0

        self.reloading = False
        self.reload_frame = 0
        self.reload_timer = 0

        # Hasar animasyonu için değişkenler
        self.damaged = False
        self.damaged_frame = 0
        self.damaged_timer = 0
        self.damaged_duration = 500  # Hasar animasyonunun süresi (ms)
        self.last_damage_time = 0

        # Fire cooldown
        self.fire_cooldown = PLAYER_FIRE_COOLDOWN
        self.last_fire_time = 0

        # Karakterin gerçek boyutu
        self.karakter_genislik = 9*SPRITE_SCALE
        self.karakter_yukseklik = 20*SPRITE_SCALE
        self.karakter_offset_x = 10*SPRITE_SCALE
        self.karakter_offset_y = 9*SPRITE_SCALE

        self.collision_rect = pygame.Rect(
            self.rect.left + self.karakter_offset_x,
            self.rect.top + self.karakter_offset_y,
            self.karakter_genislik,
            self.karakter_yukseklik
        )

        from objects import Bullet
        self.bullet_sprites = pygame.sprite.Group()

        self.health = PLAYER_HEALTH

        self.dead = False
        self.death_frame = 0
        self.death_timer = 0
        self.death_animation_finished = False
        self.death_animation_speed = DEATH_ANIMATION_SPEED

    def take_damage(self, damage):
        """Oyuncu hasar aldığında çağrılır"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time > self.damaged_duration:
            print(f"Oyuncu hasar aldı! Alınan hasar: {damage}")
            self.health = max(0, self.health - damage)
            self.damaged = True
            self.damaged_frame = 0
            self.damaged_timer = 0
            self.last_damage_time = current_time
            if self.health <= 0:
                self.dead = True
                self.death_frame = 0
                self.death_timer = 0
                self.firing = False
                self.moving = False
                self.reloading = False
                return True
            return True
        return False

    def update(self, keys, screen_width, screen_height):
        # Öncelikle ölüm animasyonu kontrolü
        if self.dead:
            self.death_timer += self.death_animation_speed
            if self.death_timer >= 1:
                self.death_frame += 1
                self.death_timer = 0
            if self.death_frame >= self.num_frames_death:
                self.death_animation_finished = True
                self.kill()
                return
            if self.facing_right:
                self.image = self.frames_death_right[min(self.death_frame, self.num_frames_death-1)]
            else:
                self.image = self.frames_death_left[min(self.death_frame, self.num_frames_death-1)]
            return

        self.moving = False
        moved = False

        # Hareket ve yön kontrolü
        if keys[pygame.K_LEFT]:
            if self.rect.left > 5*SPRITE_SCALE:
                self.rect.x -= self.speed
            self.facing_right = False
            moved = True
        if keys[pygame.K_RIGHT]:
            if self.rect.right < screen_width + 70*SPRITE_SCALE:  # Yeni sprite genişliğine göre ayarlandı
                self.rect.x += self.speed
            self.facing_right = True
            moved = True
        if keys[pygame.K_UP]:
            if self.rect.top > -2.5*SPRITE_SCALE:
                self.rect.y -= self.speed
            moved = True
        if keys[pygame.K_DOWN]:
            if self.rect.bottom < screen_height-1.5*SPRITE_SCALE:
                self.rect.y += self.speed
            moved = True

        self.moving = moved

        # Hareket sonrası çarpışma kutusunu offset ile güncelle
        self.collision_rect.topleft = (
            self.rect.left + self.karakter_offset_x,
            self.rect.top + self.karakter_offset_y
        )

        # Fire animasyonu başlat (mermi varsa ve cooldown geçtiyse)
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and not self.firing and (current_time - self.last_fire_time > self.fire_cooldown):
            self.firing = True
            self.fire_frame = 0
            self.fire_timer = 0
            self.bullets -= 1  # Mermiyi azalt
            self.last_fire_time = current_time
            if self.bullets < 0:
                self.firing = False
                self.bullets = 0
            else:
                from objects import Bullet
                if self.facing_right:
                    start_pos = (self.rect.left + 26*SPRITE_SCALE, self.rect.top + 18*SPRITE_SCALE)
                    # Mermi izinin bittiği noktayı bulmak için:
                    step = 1
                else:
                    start_pos = (self.rect.left -10*SPRITE_SCALE, self.rect.top + 18*SPRITE_SCALE)
                    step = -1
                max_length = BULLET_MAX_DISTANCE
                end_pos = (start_pos[0] + step * max_length, start_pos[1])
                # Bloklara çarpana kadar olan noktayı bul
                if hasattr(self, 'blocks_for_bullet') and self.blocks_for_bullet is not None:
                    for i in range(max_length):
                        test_x = int(start_pos[0] + step * i)
                        test_y = int(start_pos[1])
                        for block in self.blocks_for_bullet:
                            if block.rect.collidepoint(test_x, test_y):
                                end_pos = (test_x, test_y)
                                break
                        else:
                            continue
                        break
                self.bullet_sprites.add(Bullet(start_pos, end_pos))

        # Animasyon güncelle
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

        ### Reload ###
        # Reload animasyonu başlat (R tuşu ile, şu anda ateş edilmiyorsa ve reload edilmiyorsa)
        if keys[pygame.K_r] and not self.reloading and not self.firing:
            self.reloading = True
            self.reload_frame = 0
            self.reload_timer = 0

        # Reload animasyonu oynat
        if self.reloading:
            self.reload_timer += self.animation_speed * 1.5
            if self.reload_timer >= 1:
                self.reload_frame += 1
                self.reload_timer = 0
            if self.reload_frame >= self.num_frames_reload:
                self.reloading = False
                self.reload_frame = 0
                # Mermiyi doldur
                from settings import PLAYER_BULLETS
                self.bullets = PLAYER_BULLETS
            # Reload animasyon karesi seç
            if self.facing_right:
                self.image = self.frames_reload_right[min(self.reload_frame, self.num_frames_reload-1)]
            else:
                self.image = self.frames_reload_left[min(self.reload_frame, self.num_frames_reload-1)]
            return  # Reload sırasında başka animasyon oynama

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

        self.bullet_sprites.update()

    def draw(self, surface, blocks=None):
        if not self.facing_right:
            surface.blit(self.image, (self.rect.x - 75*SPRITE_SCALE, self.rect.y))
        else:
            surface.blit(self.image, self.rect.topleft)

        # Mermileri çiz
        self.bullet_sprites.draw(surface)
        # Mermilerin bloklara göre yolunu bulmak için blokları kaydet
        self.blocks_for_bullet = blocks 