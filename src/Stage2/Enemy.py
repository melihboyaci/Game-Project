import pygame
import tile_assets 

TILE_SIZE = 32


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4
        self.direction = "right"  # default yön

        self.animations = {
            "idle": {},
            "walk": {},
            "attack": {},
            "hurt": {},  # Hasar alma animasyonu
            "death": {}  # Ölüm animasyonu
        }
        self.load_animations()
        self.state = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.hurt_timer = 0  # Hasar alma durumunu kilitlemek için zamanlayıcı
        self.frame_speed = 100  # ms başına frame değişim hızı
        self.image = self.animations["idle"]["right"][0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Sağlık
        self.health = 50  # Düşmanın maksimum sağlığı
        self.max_health = 50

        # Enemy'nin hayatta olup olmadığını kontrol etmek için bayrak
        self.alive = True

        # Saldırı özellikleri:
        self.attack_damage   = 10       # bir vuruşta ne kadar hasar
        self.attack_cooldown = 1000     # ms cinsinden: 1 saniye bekleme
        self.last_attack_time = 0       # en son ne zaman saldırdı

        # saldırı menzili, piksel cinsinden
        # self.attack_range = 50 #kaldıracağız gibi görünüyor !!!

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
        scale_factor = 2  # Player ile aynı boyut için scale_factor = 2

        base_idle = self.load_animation(
            "assets/Middle_Age_Assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Orc/Orc/Orc-Idle.png", 
            100, 100, scale_factor
        )
        base_walk = self.load_animation(
            "assets/Middle_Age_Assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Orc/Orc/Orc-Walk.png", 
            100, 100, scale_factor
        )
        base_attack = self.load_animation(
            "assets/Middle_Age_Assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Orc/Orc/Orc-Attack01.png", 
            100, 100, scale_factor
        )
        base_hurt = self.load_animation(
        "assets/Middle_Age_Assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Orc/Orc/Orc-Hurt.png", 
        100, 100, scale_factor
        )
        base_death = self.load_animation(
        "assets/Middle_Age_Assets/Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Orc/Orc/Orc-Death.png", 
        100, 100, scale_factor
        )

        for state, base_frames in zip(["idle", "walk", "attack", "hurt", "death"], 
                                    [base_idle, base_walk, base_attack, base_hurt, base_death]):
            self.animations[state]["right"] = base_frames
            self.animations[state]["left"]  = [pygame.transform.flip(f, True, False) for f in base_frames]

    def take_damage(self, damage):
        self.health -= damage
        self.state = "hurt"
        self.frame_index = 0
        self.frame_timer = pygame.time.get_ticks() - 90
        self.hurt_timer = pygame.time.get_ticks()
        self.image = self.animations["hurt"][self.direction][self.frame_index]

        if self.health <= 0:
            self.state = "death"
            self.frame_index = 0
            self.frame_timer = pygame.time.get_ticks()
            self.image = self.animations["death"][self.direction][self.frame_index]


    def get_collision_rect(self):
        """Daha küçük bir çarpışma alanı döndürür."""
        collision_rect = self.rect.inflate(-self.rect.width * 0.7, -self.rect.height * 0.7)  # %70 küçült
        return collision_rect

    def die(self):
        """Düşman öldüğünde yapılacak işlemler"""
        print("Enemy öldü!")
        # Düşmanı oyundan kaldırmak için gerekli işlemleri yapın
        self.alive = False  # Enemy artık hayatta değil

    def attack(self, player):
        """Player ile collision’a girince, cooldown’a göre bir kez vurur."""
        now = pygame.time.get_ticks()
        # sadece cooldown geçmişse vur
        if now - self.last_attack_time >= self.attack_cooldown:
            # vurma animasyonuna geç
            self.state = "attack"
            self.frame_index = 0
            self.frame_timer = now

            # collision kontrolünü get_collision_rect ile yap
            if self.get_collision_rect().colliderect(player.get_collision_rect()):
                player.take_damage(self.attack_damage)
                print(f"Enemy vurdu! Player kalan can: {player.health}")

            self.last_attack_time = now

    def update(self, player, solid_rects, all_characters):
        # Eğer 'death' durumundaysa, animasyonu tamamla ve oyundan kaldır
        if self.state == "death":
            if self.frame_index >= len(self.animations["death"][self.direction]) - 1:
                print("Enemy öldü ve oyundan kaldırılıyor.")
                self.die()
                return
            else:
                self.update_animation()
                return

        # Eğer 'hurt' durumundaysa, başka bir duruma geçme
        if self.state == "hurt":
            if pygame.time.get_ticks() - self.hurt_timer < 500:
                self.update_animation()
                return
            else:
                self.state = "idle"

        # Player ile aradaki mesafe
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx * dx + dy * dy) ** 0.5

        # Yön belirle
        self.direction = "right" if dx > 0 else "left"

        # Saldırı menzili kontrolü
        if self.get_collision_rect().colliderect(player.get_collision_rect()):
            self.attack(player)
        else:
            # Eğer çok yakınsa hareket etmesin
            if distance > 5:
                # --- X ekseni için ayrı kontrol ---
                norm = max(1, distance)
                step_x = self.speed * dx / norm
                step_y = self.speed * dy / norm

                # Çok küçük adımları sıfırla
                if abs(step_x) < 1: step_x = 0
                if abs(step_y) < 1: step_y = 0

                # X ekseni hareketi
                if step_x != 0:
                    next_hitbox_x = self.get_hitbox_rect().move(step_x, 0)
                    can_move_x = True
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
                        self.x += step_x

                # Y ekseni hareketi
                if step_y != 0:
                    next_hitbox_y = self.get_hitbox_rect().move(0, step_y)
                    can_move_y = True
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
                        self.y += step_y

                if (step_x != 0 and can_move_x) or (step_y != 0 and can_move_y):
                    self.state = "walk"
                else:
                    self.state = "idle"
            else:
                self.state = "idle"

        self.rect.center = (self.x, self.y)
        self.update_animation()

    # Çarpışma kontrolü
    def get_collision_rect(self):
        # Daraltılmış çarpışma alanı
        return self.rect.inflate(-self.rect.width * 0.9, -self.rect.height * 0.9)

    def resolve_collision(self, other):
        """
        Diğer objenin daraltılmış collision rect'i ile kendi daraltılmış rect'inin overlap'ini gider.
        other: ya bir pygame.Rect ya da get_collision_rect() döndüren obje
        """
        # other bir obje ise onun collision rect'ini al
        other_rect = other.get_collision_rect() if hasattr(other, 'get_collision_rect') else other
        self_rect  = self.get_collision_rect()

        if not self_rect.colliderect(other_rect):
            return
        # çakışan bölge
        overlap = self_rect.clip(other_rect)
        # en kısa eksende itiş
        if overlap.width < overlap.height:
            # x ekseni
            if self_rect.centerx < other_rect.centerx:
                self.x -= overlap.width
            else:
                self.x += overlap.width
        else:
            # y ekseni
            if self_rect.centery < other_rect.centery:
                self.y -= overlap.height
            else:
                self.y += overlap.height
        # rect'e yansıt
        self.rect.center = (self.x, self.y)

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_speed:
            self.frame_timer = now
            self.frame_index += 1

            # Eğer animasyonun son karesine ulaşıldıysa
            if self.frame_index >= len(self.animations[self.state][self.direction]):
                if self.state == "hurt":
                    self.state = "idle"  # Hasar alma animasyonu bittiğinde 'idle' durumuna geç
                elif self.state == "death":
                    self.frame_index = len(self.animations["death"][self.direction]) - 1  # Ölüm animasyonunda son karede kal
                    return
                self.frame_index = 0  # Animasyonu sıfırla

            # Geçerli animasyon karesini güncelle
            self.image = self.animations[self.state][self.direction][self.frame_index]


    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

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
        hitbox_size = 15 #orijinal 36 
        center_x = self.x + self.rect.width // 2
        center_y = self.y + self.rect.height // 2
        return pygame.Rect(
            center_x - hitbox_size // 2,
            center_y - hitbox_size // 2,
            hitbox_size,
            hitbox_size
        )