import pygame
import os
import tile_assets

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y


        self.can_control = False  # Başta kontrol edilemez
        self.auto_walk = False

        self.speed = 4
        self.direction = "right"  # default yön
        self.is_player = True # Oyuncu karakteri
        self.animations = {
            "idle": {},
            "walk": {},
            "attack1": {},
            "attack2": {},
            "hurt": {},
            "death": {}
        }

        self.attack1_sound = pygame.mixer.Sound("assets/Middle_Age_Assets/sounds/sword-normal.mp3")
        self.attack1_sound.set_volume(0.3)

        self.attack2_sound = pygame.mixer.Sound("assets/Middle_Age_Assets/sounds/sword-ultimate.mp3")
        self.attack2_sound.set_volume(0.5)
        

        self.load_animations()
        self.state = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.hurt_timer = 0
        self.frame_speed = 100  # ms başına frame değişim hızı
        self.image = self.animations["idle"]["right"][0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Sağlık
        self.health = 300  # Maksimum sağlık
        self.max_health = 300

        

        # Attack tuşları
        self.attack_keys = {
            "attack1": pygame.K_SPACE,
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

        self.attack_once = False # Sadece bir kez saldırı yapabilmek için    
        # Mesaj göstermek için
        self.attack_message = ""

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
        hurt_frames = self.load_animation(
            "assets/Middle_Age_Assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Hurt.png", 
            100, 100, scale_factor
        )
        death_frames = self.load_animation(
            "assets/Middle_Age_Assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/Soldier/Soldier-Death.png", 
            100, 100, scale_factor
        )

        for state, base_frames in zip(["idle", "walk", "attack1", "attack2", "hurt", "death"], 
                                    [base_idle, base_walk, attack1_frames, attack2_frames, hurt_frames, death_frames]):
            self.animations[state]["right"] = base_frames
            self.animations[state]["left"]  = [pygame.transform.flip(f, True, False) for f in base_frames]

    def handle_input(self, solid_rects, all_characters):
        if self.state == "death":
            return  # input handle yok, karakter kontrol edilemez

        TILE_SIZE = 32
        if self.state == "hurt" and pygame.time.get_ticks() - self.hurt_timer < 300:
            return

        keys = pygame.key.get_pressed()
        moving = False
        now = pygame.time.get_ticks()
        self.rect.center = (self.x, self.y)

        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_a]:
            dx = -1
            self.direction = "left"
        if keys[pygame.K_d]:
            dx = 1
            self.direction = "right"

        # --- X ekseni için ayrı kontrol ---
        if dx != 0:
            next_hitbox_x = self.get_hitbox_rect().move(dx * self.speed, 0)
            can_move_x = True
            # Sınır kontrolü
            if not self.is_within_map(next_hitbox_x):
                can_move_x = False
            # Diğer çarpışma kontrolleri...
            for rect in solid_rects:
                if next_hitbox_x.colliderect(rect):
                    can_move_x = False
                    break
            if can_move_x:
                for other in all_characters:
                    if other is self:
                        continue
                    if next_hitbox_x.colliderect(other.get_hitbox_rect()):
                        can_move_x = False
                        break
            if can_move_x:
                self.x += dx * self.speed
                moving = True

        # --- Y ekseni için ayrı kontrol ---
        if dy != 0:
            next_hitbox_y = self.get_hitbox_rect().move(0, dy * self.speed)
            can_move_y = True
            # Sınır kontrolü
            if not self.is_within_map(next_hitbox_y):
                can_move_y = False
            # Diğer çarpışma kontrolleri...
            for rect in solid_rects:
                if next_hitbox_y.colliderect(rect):
                    can_move_y = False
                    break
            if can_move_y:
                for other in all_characters:
                    if other is self:
                        continue
                    if next_hitbox_y.colliderect(other.get_hitbox_rect()):
                        can_move_y = False
                        break
            if can_move_y:
                self.y += dy * self.speed
                moving = True

        # Attack inputları ve state güncellemesi aynı kalabilir
        for attack_name, key in self.attack_keys.items():
            if keys[key] and now - self.last_attack_time[attack_name] > self.attack_cooldowns[attack_name]:
                self.state = attack_name
                self.frame_index = 0
                self.frame_timer = now
                self.last_attack_time[attack_name] = now
                self.attack_message = f"{attack_name.upper()} kullanıldı!"
                print(f"{attack_name} kullanıldı! Hasar: {self.attack_damage[attack_name]}")
                if attack_name == "attack1":
                    self.attack1_sound.play()
                elif attack_name == "attack2":
                    self.attack2_sound.play()
                return

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
            if self.state != "death" or self.frame_index < len(self.animations[self.state][self.direction]) - 1:
                self.frame_index += 1

            # Eğer animasyonun son karesine ulaşıldıysa
            if self.frame_index >= len(self.animations[self.state][self.direction]):
                if self.state == "hurt":
                    self.state = "idle"
                    self.frame_index = 0
                elif self.state.startswith("attack"):
                    self.state = "idle"
                    self.frame_index = 0
                elif self.state != "death":
                    self.frame_index = len(self.animations[self.state][self.direction]) - 1

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
        # Attack2 cooldown barı (sağlık barının yanında)
        now = pygame.time.get_ticks()
        cooldown = self.attack_cooldowns["attack2"]
        last_used = self.last_attack_time["attack2"]
        elapsed = min(now - last_used, cooldown)
        cooldown_ratio = elapsed / cooldown

        bar_width = 100
        bar_height = 20
        x = 250  # Sağlık barının hemen sağında
        y = 20
        pygame.draw.rect(surface, (50, 50, 50), (x, y, bar_width, bar_height))  # Arkaplan (gri)
        pygame.draw.rect(surface, (0, 0, 255), (x, y, bar_width * cooldown_ratio, bar_height))  # Cooldown (mavi)
        pygame.draw.rect(surface, (0, 0, 0), (x, y, bar_width, bar_height), 2)  # Çerçeve

    def draw_attack_info_message(self, surface):
        font = pygame.font.Font(None, 25)
        text = font.render("K:", True, (255, 255, 255))
        surface.blit(text, (230, 20))  # Mesaj ekranın sol üstünde gösterilir


    def attack(self, enemies):
        """Daire menzilli saldırı mekanizması"""
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_k] or keys[pygame.K_SPACE]):
            if not self.attack_once:  # sadece ilk basışta çalışsın
                if self.state not in self.attack_damage:
                    print(f"Hata: '{self.state}' geçerli bir saldırı durumu değil.")
                    return

                # Saldırı menzili seçimi (daire)
                if self.state == "attack2":
                    center, radius = self.get_attack2_circle()
                else:
                    center, radius = self.get_attack1_circle()

                for enemy in enemies:
                    if self.is_in_circle(center, radius, enemy.get_hitbox_rect()):
                        enemy.take_damage(self.attack_damage[self.state])
                        print(f"Enemy hasar aldı! Kalan sağlık: {enemy.health}")

                self.attack_once = True
        else:
            self.attack_once = False

    def take_damage(self, damage):
        """Hasar alma mekanizması"""
        self.health -= damage
        self.state = "hurt"
        self.frame_index = 0
        now = pygame.time.get_ticks()
        self.frame_timer = now
        self.hurt_timer = now 
        self.image = self.animations["hurt"][self.direction][self.frame_index]  # Animasyonu hemen güncelle
        print(f"Player {damage} hasar aldı! Kalan can: {self.health}")
        if self.health <= 0:
            self.state = "death"
            self.frame_index = 0
            self.frame_timer = pygame.time.get_ticks()
            self.image = self.animations["death"][self.direction][self.frame_index]  # Ölüm animasyonunu başlat  
            self.die()

    def die(self):
        """Player öldüğünde yapılacak işlemler"""
        print("Player öldü! Oyun bitti.")

    #çarpışma kontrolü için
    def get_collision_rect(self):
        # Daraltılmış çarpışma alanı
        return self.rect.inflate(-self.rect.width * 0.7, -self.rect.height * 0.7)


    def draw_attack2_range(self, surface):
        if self.state == "attack2":
            center, radius = self.get_attack2_circle()
            s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (0, 0, 255, 80), (radius, radius), radius)
            surface.blit(s, (center[0] - radius, center[1] - radius))

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        self.draw_health_bar(surface)
        self.draw_cooldown_bar(surface)
        self.draw_attack_info_message(surface)
        # Sağlık barı ve cooldown barı için mesaj
        self.draw_attack2_range(surface)

    def update(self):
        # Eğer 'death' durumundaysa, animasyonu tamamla ve oyunu sonlandır
        if self.state == "death":
            self.update_animation()
            return

        # Eğer 'hurt' durumundaysa, başka bir duruma geçme
        if self.state == "hurt":
            if pygame.time.get_ticks() - self.hurt_timer < 500:  # 500 ms boyunca 'hurt' durumunda kal
                self.update_animation()
                return
            else:
                self.state = "idle"  # 'hurt' süresi dolduğunda 'idle' durumuna geç

        # Karakter rect güncelle
        self.rect.center = (self.x, self.y)
        # Animasyonu güncelle
        self.update_animation()


    def is_area_walkable(self,x, y, size=(1, 1)):
        """Verilen sol üst köşe ve boyut için tüm alanın yürünebilir olup olmadığını kontrol eder."""
        for dy in range(size[1]):
            for dx in range(size[0]):
                tx = x + dx
                ty = y + dy
                if tx < 0 or ty < 0 or tx >= tile_assets.map_data.shape[1] or ty >= tile_assets.map_data.shape[0]:
                    return False
                tile_walkable = tile_assets.tile_dict[tile_assets.map_data[ty][tx]]["walkable"]
                object_index = tile_assets.object_data[ty][tx]
                object_walkable = tile_assets.object_dict[object_index]["walkable"]
                if not (tile_walkable and object_walkable):
                    return False
        return True    
    
    def get_hitbox_rect(self):
        # Karakterin merkezinden 18 piksel uzaklıkta 36x36'lık bir kare
        hitbox_size = 20 #orijinal 36 
        center_x = self.x + self.rect.width // 2
        center_y = self.y + self.rect.height // 2
        return pygame.Rect(
            center_x - hitbox_size // 2,
            center_y - hitbox_size // 2,
            hitbox_size,
            hitbox_size
        )
    

    def get_attack1_circle(self):
        # Küçük menzil (ör: yarıçap 50)
        center_x = self.x + self.rect.width // 2
        center_y = self.y + self.rect.height // 2
        return (center_x, center_y), 50

    def get_attack2_circle(self):
        # Büyük menzil (ör: yarıçap 60)
        center_x = self.x + self.rect.width // 2
        center_y = self.y + self.rect.height // 2
        return (center_x, center_y), 60

    def is_in_circle(self,center, radius, rect):
        # Enemy'nin hitbox merkezini al
        enemy_center = rect.center
        dx = enemy_center[0] - center[0]
        dy = enemy_center[1] - center[1]
        return dx*dx + dy*dy <= radius*radius

    def auto_walk_forward(self, distance=64):
        """Player'ı sağa doğru distance kadar otomatik yürüt."""
        if not hasattr(self, "_auto_walk_start_x"):
            self._auto_walk_start_x = self.x
        walk_speed = 2    
        if self.x < self._auto_walk_start_x + distance:
            self.x += walk_speed
            self.state = "walk"
            self.direction = "right"
            self.rect.center = (self.x, self.y)
            self.update_animation()
            return False  # Hala yürüyor
        else:
            self.auto_walk = False
            self.can_control = True
            del self._auto_walk_start_x
            return True   # Yürüyüş bitti

    def is_within_map(self,rect):
        """Verilen rect'in harita sınırları içinde olup olmadığını kontrol eder."""
        map_width=1280
        map_height=704
        return (
            rect.left >= 0 and
            rect.top >= 0 and
            rect.right <= map_width and
            rect.bottom <= map_height
        )