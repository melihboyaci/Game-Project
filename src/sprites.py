import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, bullets):
        super().__init__()
        
        # Run sprite sheet
        self.spritesheet_run = pygame.image.load("assets/Rifle_Stage_Assets/sprites/soldier/rifle/run.png").convert_alpha()
        # Fire sprite sheet
        self.spritesheet_fire = pygame.image.load("assets/Rifle_Stage_Assets/sprites/soldier/rifle/fire.png").convert_alpha()
        # Reload sprite sheet
        self.spritesheet_reload = pygame.image.load("assets/Rifle_Stage_Assets/sprites/soldier/rifle/reload.png").convert_alpha()


        self.frame_width = 102  # Her bir karenin genişliği
        self.frame_height = 36  # Her bir karenin yüksekliği

        self.num_frames_run = self.spritesheet_run.get_width() // self.frame_width
        self.num_frames_fire = self.spritesheet_fire.get_width() // self.frame_width
        self.num_frames_reload = self.spritesheet_reload.get_width() // self.frame_width
        self.bullets = bullets

        # Run animasyon kareleri
        self.frames_run_right = [
            pygame.transform.scale(
                self.spritesheet_run.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)),
                (self.frame_width * 2, self.frame_height * 2)
            ) for i in range(self.num_frames_run)
        ]
        self.frames_run_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_run_right]

        # Fire animasyon kareleri
        self.frames_fire_right = [
            pygame.transform.scale(
                self.spritesheet_fire.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)),
                (self.frame_width * 2, self.frame_height * 2)
            ) for i in range(self.num_frames_fire)
        ]
        self.frames_fire_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_fire_right]

        # Reload animasyon kareleri
        self.frames_reload_right = [
            pygame.transform.scale(
                self.spritesheet_reload.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)),
                (self.frame_width * 2, self.frame_height * 2)
            ) for i in range(self.num_frames_reload)
        ]        
        self.frames_reload_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_reload_right]

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

    def update(self, keys, screen_width, screen_height):
        self.moving = False
        moved = False

        # Hareket ve yön kontrolü
        if keys[pygame.K_LEFT]:
            if self.rect.left > 10:
                self.rect.x -= self.speed
            self.facing_right = False
            moved = True
        if keys[pygame.K_RIGHT]:
            if self.rect.right < screen_width + 135:
                self.rect.x += self.speed
            self.facing_right = True
            moved = True
        if keys[pygame.K_UP]:
            if self.rect.top > -5:
                self.rect.y -= self.speed
            moved = True
        if keys[pygame.K_DOWN]:
            if self.rect.bottom < screen_height-5:
                self.rect.y += self.speed
            moved = True

        self.moving = moved

        # Fire animasyonu başlat (mermi varsa)
        if keys[pygame.K_SPACE] and not self.firing:
            self.firing = True
            self.fire_frame = 0
            self.fire_timer = 0
            self.bullets -= 1  # Mermiyi azalt
            if self.bullets < 0:
                self.firing = False
                self.bullets = 0

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

    def draw(self, surface):
        if not self.facing_right:
            surface.blit(self.image, (self.rect.x - 150, self.rect.y))
        else:
            surface.blit(self.image, self.rect.topleft)

class Block1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/Rifle_Stage_Assets/background_tileset/Block1.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))