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
            "open":  ("assets/portal_open.png", 64, 64),
            "idle":  ("assets/portal_idle.png", 64, 64),
            "close": ("assets/portal_close.png", 64, 64)
        }

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
        if now - self.frame_timer > self.frame_speed:
            self.frame_timer = now
            self.frame_index += 1
            frames = self.animations[self.state]
            if self.frame_index >= len(frames):
                if self.state == "open":
                    self.state = "idle"
                    self.frame_index = 0
                elif self.state == "idle":
                    self.state = "close"
                    self.frame_index = 0
                elif self.state == "close":
                    self.finished = True
                    self.frame_index = len(frames) - 1  # Son karede kal

    def draw(self, surface):
        img = self.animations[self.state][self.frame_index]
        surface.blit(img, (self.x, self.y))