import pygame

class Portal:
    def __init__(self, x, y, scale_factor=1, frame_speed=100):
        self.x = x
        self.y = y
        self.state = "open"
        self.scale_factor = scale_factor
        self.frame_speed = frame_speed

        # Animasyon yolları ve frame boyutları burada!
        self.anim_paths = {
            "open":  ("assets/portal_assets/Green_Portal_open.png", 64, 64),
            "idle":  ("assets/portal_assets/Green_Portal_idle.png", 64, 64),
            "close": ("assets/portal_assets/Green_Portal_close.png", 64, 64)
        }

        # Portal.py içinde, __init__ fonksiyonuna ekle:
        self.sounds = {
            "open": pygame.mixer.Sound("assets\Middle_Age_Assets\sounds\portal_open.mp3"),
            "idle": pygame.mixer.Sound("assets\Middle_Age_Assets\sounds\portal_idle.mp3"),
            "close": pygame.mixer.Sound("assets\Middle_Age_Assets\sounds\portal_close.mp3"),
        }
        self.idle_channel = None  # Idle sesi için özel kanal
        self.last_state = self.state


        self.animations = {}
        for state, (path, w, h) in self.anim_paths.items():
            self.animations[state] = self.load_animation(path, w, h, self.scale_factor)

        self.frame_index = 0
        self.frame_timer = pygame.time.get_ticks()
        self.finished = False

    def load_animation(self, sheet_path, frame_w, frame_h, scale_factor=1):
        sheet = pygame.image.load(sheet_path).convert_alpha()
        frame_count = sheet.get_rect().width // frame_w
        frames = []
        for i in range(frame_count):
            frame_rect = pygame.Rect(i * frame_w, 0, frame_w, frame_h)
            frame = sheet.subsurface(frame_rect)
            scaled_frame = pygame.transform.scale(frame, (frame_w * scale_factor, frame_h * scale_factor))
            frames.append(scaled_frame)
        return frames

    def update(self):
        now = pygame.time.get_ticks()
        # State değişimini kontrol et
        if self.state != self.last_state:
            # Önce idle sesi varsa durdur
            if self.last_state == "idle" and self.idle_channel is not None:
                self.idle_channel.stop()
                self.idle_channel = None
            # Yeni state'e göre sesi çal
            if self.state == "open":
                self.sounds["open"].play()
            elif self.state == "close":
                self.sounds["close"].play()
            elif self.state == "idle":
                # Idle sesi loop'lu çalsın
                self.idle_channel = self.sounds["idle"].play(loops=-1)
            self.last_state = self.state

        if now - self.frame_timer > self.frame_speed:
            self.frame_timer = now
            self.frame_index += 1
            frames = self.animations[self.state]
            if self.frame_index >= len(frames):
                if self.state == "open":
                    self.state = "idle"
                    self.frame_index = 0
                elif self.state == "idle":
                    self.frame_index = 0
                elif self.state == "close":
                    self.finished = True
                    self.frame_index = len(frames) - 1  # Son karede kal

        if self.state == "close" and self.finished and self.idle_channel is not None:
            self.idle_channel.stop()
            self.idle_channel = None

    def draw(self, surface):
        img = self.animations[self.state][self.frame_index]
        surface.blit(img, (self.x, self.y))


    def draw_flipped(self, surface):
        img = self.animations[self.state][self.frame_index]
        img_flipped = pygame.transform.flip(img, True, False)
        surface.blit(img_flipped, (self.x, self.y))