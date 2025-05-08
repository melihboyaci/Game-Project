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
            "attack2": {},
            "hurt": {},
            "death": {}
        }
        self.load_animations()
        self.state = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.hurt_timer = 0
        self.frame_speed = 100  # ms başına frame değişim hızı
        self.image = self.animations["idle"]["right"][0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Sağlık
        self.health = 100  # Maksimum sağlık
        self.max_health = 100

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

    def handle_input(self):
        # eğer hurt durumundaysa ve 300 ms dolmadıysa
        if self.state == "hurt" and pygame.time.get_ticks() - self.hurt_timer < 300:
            return     # hiçbir input işleme, animasyon da update() içinde kalacak

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
                self.attack_message = f"{attack_name.upper()} kullanıldı!"
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

            # Eğer animasyonun son karesine ulaşıldıysa
            if self.frame_index >= len(self.animations[self.state][self.direction]):
                if self.state == "hurt":
                    self.state = "idle"  # Hasar alma animasyonu bittiğinde 'idle' durumuna geç
                elif self.state.startswith("attack"):
                    self.state = "idle"  # Saldırı animasyonu bittiğinde 'idle' durumuna geç
                elif self.state == "death":
                    self.frame_index = len(self.animations["death"][self.direction]) - 1  # Ölüm animasyonunda son karede kal
                    return
                self.frame_index = 0  # Animasyonu sıfırla

            # Geçerli animasyon karesini güncelle
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
        """Saldırı mekanizması"""
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_k] or keys[pygame.K_SPACE]):
            if not self.attack_once:  # sadece ilk basışta çalışsın
                # Saldırı durumunu kontrol et
                if self.state not in self.attack_damage:
                    print(f"Hata: '{self.state}' geçerli bir saldırı durumu değil.")
                    return

                for enemy in enemies:
                    if self.get_collision_rect().colliderect(enemy.get_collision_rect()):  # Çarpışma kontrolü
                        enemy.take_damage(self.attack_damage[self.state])
                        print(f"Enemy hasar aldı! Kalan sağlık: {enemy.health}")
                
                self.attack_once = True  # saldırıyı kilitle
        else:
            self.attack_once = False  # tuş bırakıldığında sıfırla

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
        pygame.quit()
        exit()


    def get_collision_rect(self):
        """Daha küçük bir çarpışma alanı döndürür."""
        collision_rect = self.rect.inflate(-self.rect.width * 0.7, -self.rect.height * 0.7)  # %40 küçült
        return collision_rect

    #çarpışma kontrolü için
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


    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        self.draw_health_bar(surface)
        self.draw_cooldown_bar(surface)
        self.draw_attack_info_message(surface)
        # Sağlık barı ve cooldown barı için mesaj

    def update(self):
        # Eğer 'death' durumundaysa, animasyonu tamamla ve oyunu sonlandır
        if self.state == "death":
            if self.frame_index >= len(self.animations["death"][self.direction]) - 1:
                print("Player öldü! Oyun sonlandırılıyor.")
                pygame.quit()
                exit()
            else:
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