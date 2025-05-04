import pygame
import os

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4
        self.direction = "right"  # default yön

        self.animations = {
            "idle": {},
            "walk": {},
            "attack": {}
        }
        self.load_animations()
        self.state = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 100  # ms başına frame değişim hızı
        self.image = self.animations["idle"]["right"][0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def load_animation(self, sheet_path, frame_w, frame_h, scale_factor=2):
        sheet = pygame.image.load(sheet_path).convert_alpha()
        frame_count = sheet.get_rect().width // frame_w
        frames = []
        for i in range(frame_count):
            frame_rect = pygame.Rect(i * frame_w, 0, frame_w, frame_h)
            frame = sheet.subsurface(frame_rect)
            scaled_frame = pygame.transform.scale(frame, (frame_w * scale_factor, frame_h * scale_factor))
            frames.append(scaled_frame)
        return frames

    def load_animations(self):
        scale_factor = 2

        base_idle = self.load_animation(
            "assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Idle.png", 
            100, 100, scale_factor
        )
        base_walk = self.load_animation(
            "assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Walk.png", 
            100, 100, scale_factor
        )
        base_attack = self.load_animation(
            "assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Attack01.png", 
            100, 100, scale_factor
        )

        # Sağ yön default, sola flip’leyerek
        for state, base_frames in zip(["idle", "walk", "attack"], [base_idle, base_walk, base_attack]):
            self.animations[state]["right"] = base_frames
            self.animations[state]["left"]  = [pygame.transform.flip(f, True, False) for f in base_frames]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_w]:
            self.y -= self.speed
            moving = True
        if keys[pygame.K_s]:
            self.y += self.speed
            moving = True
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.direction = "left"
            moving = True
        if keys[pygame.K_d]:
            self.x += self.speed
            self.direction = "right"
            moving = True

        if keys[pygame.K_SPACE]:
            self.state = "attack"
            self.frame_index = 0
            self.frame_timer = pygame.time.get_ticks()
        elif moving:
            if self.state != "attack":
                self.state = "walk"
        else:
            if self.state != "attack":
                self.state = "idle"

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_speed:
            self.frame_timer = now
            self.frame_index += 1
            if self.frame_index >= len(self.animations[self.state][self.direction]):
                if self.state == "attack":
                    self.state = "idle"
                self.frame_index = 0
            self.image = self.animations[self.state][self.direction][self.frame_index]

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
