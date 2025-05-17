import pygame
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
        # Ortalanmış 30x30'luk collision rect, 120 piksel sağa kaydırılmış
        self.collision_rect = pygame.Rect(0, 0, 30, 30)
        self.collision_rect.center = self.rect.center
        self.collision_rect.x += 120
        self.on_finish = on_finish
        # Portal idle sesini yükle
        self.idle_sound = pygame.mixer.Sound('assets/Space_Stage_Assets/sounds/portal_idle.mp3')
        self.idle_sound_channel = None
        self.idle_sound_playing = False
        # Açılış ve kapanış sesleri
        self.open_sound = pygame.mixer.Sound('assets/Space_Stage_Assets/sounds/portal_open.mp3')
        self.close_sound = pygame.mixer.Sound('assets/Space_Stage_Assets/sounds/portal_close.mp3')
        self.open_sound_played = False
        self.close_sound_played = False

        self.open_time = pygame.time.get_ticks()
        self.open_duration = 2000  # 2 saniye

    def update(self):
        # Portal idle durumunda belli bir süre sonra kapanmaya başlasın
        if self.state == 'idle':
            if pygame.time.get_ticks() - self.open_time > self.open_duration:
                self.start_closing()
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

    def load_frames(self, path, scale):
        img = pygame.image.load(path).convert_alpha()
        frame_width = img.get_width() // 8  # 8 frames per row
        frame_height = img.get_height()
        frames = [pygame.transform.scale(
            img.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)),
            (frame_width * scale, frame_height * scale)
        ) for i in range(8)]
        return frames

    

    def start_closing(self):
        self.state = 'closing'
        self.frame_index = 0
        self.frame_timer = 0
        self.close_sound_played = False  # Kapanış başında flag sıfırla

    def draw(self, surface, camera):
        #portalı 90 derede döndür
        self.image = pygame.transform.rotate(self.image, 90)
        screen_pos = (self.rect.x - camera.pos[0], self.rect.y - camera.pos[1])
        surface.blit(self.image, screen_pos)