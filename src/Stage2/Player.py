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
            "attack1": {},
            "attack2": {}
        }
        self.load_animations()
        self.state = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 100  # ms başına frame değişim hızı
        self.image = self.animations["idle"]["right"][0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Sağlık
        self.health = 100  # Maksimum sağlık
        self.max_health = 100

        # Attack tuşları
        self.attack_keys = {
            "attack1": pygame.K_j,
            "attack2": pygame.K_k
        }

        # Hasarlar
        self.attack_damage = {
            "attack1": 10,
            "attack2": 20
        }

        # Cooldown süreleri (ms)
        self.attack_cooldowns = {
            "attack1": 500,
            "attack2": 10000  # 10 saniye
        }

        # Son kullanımlar
        self.last_attack_time = {
            "attack1": 0,
            "attack2": 0
        }

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
            "assets/Middle_Age_Assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Idle.png", 
            100, 100, scale_factor
        )
        base_walk = self.load_animation(
            "assets/Middle_Age_Assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Walk.png", 
            100, 100, scale_factor
        )
        attack1_frames = self.load_animation(
            "assets/Middle_Age_Assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Attack01.png", 
            100, 100, scale_factor
        )
        attack2_frames = self.load_animation(
            "assets/Middle_Age_Assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Attack02.png", 
            100, 100, scale_factor
        )

        for state, base_frames in zip(["idle", "walk", "attack1", "attack2"], [base_idle, base_walk, attack1_frames, attack2_frames]):
            self.animations[state]["right"] = base_frames
            self.animations[state]["left"]  = [pygame.transform.flip(f, True, False) for f in base_frames]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        moving = False
        now = pygame.time.get_ticks()
        self.rect.center = (self.x, self.y)
        # Ekrandan taşmaması için sınırları ayarla
        if self.x < 0:
            self.x = 0
        elif self.x > 1280 - self.rect.width:
            self.x = 1280 - self.rect.width
        if self.y < 0:
            self.y = 0
        elif self.y > 720 - self.rect.height:
            self.y = 720 - self.rect.height
        self.rect.center = (self.x, self.y)

        # Hareket inputları
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

        # Attack inputları
        for attack_name, key in self.attack_keys.items():
            if keys[key] and now - self.last_attack_time[attack_name] > self.attack_cooldowns[attack_name]:
                self.state = attack_name
                self.frame_index = 0
                self.frame_timer = now
                self.last_attack_time[attack_name] = now
                print(f"{attack_name} kullanıldı! Hasar: {self.attack_damage[attack_name]}")
                return  # aynı anda başka hareket yapmasın

        # Eğer saldırıda değilse, yürüme veya idle state'e geç
        if self.state.startswith("attack"):
            return

        if moving:
            self.state = "walk"
        else:
            self.state = "idle"

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_speed:
            self.frame_timer = now
            self.frame_index += 1
            if self.frame_index >= len(self.animations[self.state][self.direction]):
                if self.state.startswith("attack"):
                    self.state = "idle"
                self.frame_index = 0
            self.image = self.animations[self.state][self.direction][self.frame_index]

    def draw_health_bar(self, surface):
        # Sağlık barı
        bar_width = 200
        bar_height = 20
        x = 20
        y = 20
        health_ratio = self.health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))  # Arkaplan (kırmızı)
        pygame.draw.rect(surface, (0, 255, 0), (x, y, bar_width * health_ratio, bar_height))  # Sağlık (yeşil)
        pygame.draw.rect(surface, (0, 0, 0), (x, y, bar_width, bar_height), 2)  # Çerçeve

    def draw_cooldown_bar(self, surface):
        # Attack2 cooldown barı
        now = pygame.time.get_ticks()
        cooldown = self.attack_cooldowns["attack2"]
        last_used = self.last_attack_time["attack2"]
        elapsed = min(now - last_used, cooldown)
        cooldown_ratio = elapsed / cooldown

        bar_width = 200
        bar_height = 20
        x = 20
        y = 50
        pygame.draw.rect(surface, (50, 50, 50), (x, y, bar_width, bar_height))  # Arkaplan (gri)
        pygame.draw.rect(surface, (0, 0, 255), (x, y, bar_width * cooldown_ratio, bar_height))  # Cooldown (mavi)
        pygame.draw.rect(surface, (0, 0, 0), (x, y, bar_width, bar_height), 2)  # Çerçeve

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        self.draw_health_bar(surface)
        self.draw_cooldown_bar(surface)

    def update(self):
        # karakter rect güncelle
        self.rect.center = (self.x, self.y)
        # animasyonu güncelle
        self.update_animation()