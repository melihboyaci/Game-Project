import pygame
from utils.planet import Planet
import random
from utils.animation import AnimatedSprite, load_sprite_sheet
from utils.views import draw_scrolling_bg
from utils.spaceship import Spaceship
from utils.enemy_spaceship import EnemySpaceship
from utils.enemybase import EnemyBase

class game_loop:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = screen.get_size()
        self.bg_offset = {'x': 0, 'y': 0}
        self.bg_speed  = {'x': -0.1, 'y': 0.2}
        self.bg_image = pygame.image.load("assets/Space_Stage_Assets/ui/backgrounds/space4.png").convert_alpha()        
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        self.map_width = 2000
        self.map_height = 2000
        self.camera_pos = [0, 0]
        self.earth_bar = 100
        self.bar_width = 300
        self.bar_height = 20
        self.bar_x = (self.width - self.bar_width) // 2
        self.bar_y = 20
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.last_enemy_spawn = pygame.time.get_ticks()


        ## Gezegenlerin boyutları ve konumları
        """self.planet_count = 6
        self.planet_sizes = [
            (100, 100),
            (300, 300),
            (100, 100),
            (100, 100),
            (100, 100),
            (100, 100),
        ]"""

        self.planets = []
        """for i in range(self.planet_count):
            planet_path = f"assets/Space_Stage_Assets/sprites/planets/planet{i+2}.png"
            size = self.planet_sizes[i]
            max_attempts = 100 # Maksimum deneme sayısı
            for attempt in range(max_attempts):
                position = (
                    random.randint(0, self.map_width - size[0]),
                    random.randint(0, self.map_height - size[1])
                )
            planet = Planet(planet_path, size, position, scale=1)
            self.planets.append(planet)"""
        
        
        earth_path = "assets/Space_Stage_Assets/sprites/planets/earth.png"
        earth_size = (300, 300)
        earth_pos = (
                self.map_width // 2 - 300 // 2,
                self.map_height // 2 + 300
                )
        Earth = Planet(earth_path, earth_size, earth_pos, scale=(1.5))    
        self.planets.append(Earth) # Dünya
        self.earth = Earth
        
        base_size = (128, 128)
        corners = [
            (0, 0),  # Sol Üst
            (self.map_width - base_size[0], 0),  # Sağ Üst
            (0, self.map_height - base_size[1]),  # Sol Alt
            (self.map_width - base_size[0], self.map_height - base_size[1])  # Sağ Alt
        ]
        earth_center = (
            self.earth.position[0] + self.earth.size[0] // 2,
            self.earth.position[1] + self.earth.size[1] // 2
        )

        max_distance = -1
        base_pos = None
        for corner in corners:
            distance = ((corner[0] - earth_center[0]) ** 2 + (corner[1] - earth_center[1]) ** 2) ** 0.5
            if distance > max_distance:
                max_distance = distance
                base_pos = corner


        enemy_base_path = "assets/Space_Stage_Assets/sprites/enemybase/base.png"
        enemy_base_size = (128, 128)
        enemy_base = EnemyBase(enemy_base_path, enemy_base_size, base_pos)
        self.enemy_base = enemy_base
        base_center = (
            self.enemy_base.position[0] + self.enemy_base.size[0] * self.enemy_base.scale // 2,
            self.enemy_base.position[1] + self.enemy_base.size[1] * self.enemy_base.scale // 2
        )
       

        self.spaceship_path = "assets/Space_Stage_Assets/sprites/spaceship/1.png"
        self.engine_path = "assets/Space_Stage_Assets/sprites/spaceship/engine.png"
        spaceship_size = (64, 64)
        self.spaceship_position = (
            earth_pos[0] + earth_size[0] // 2 - spaceship_size[0] // 2 + 150,
            earth_pos[1] - spaceship_size[1] - 20 
        )
        self.spaceship_speed = 5
        self.spaceship = Spaceship(self.spaceship_path, spaceship_size, self.spaceship_position, self.spaceship_speed, engine_path=self.engine_path, engine_size=(41, 30))    
        
        #düşman gemisi
        self.enemy_spaceships = []
        enemy_size = (64, 64)
        self.enemy_image = "assets/Space_Stage_Assets/sprites/spaceship/2.png"
        for i in range(5):
            # Her düşmanı base'in merkezinden biraz farklı bir noktada spawnla
            offset_x = random.randint(-20, 20)
            offset_y = random.randint(-20, 20)
            spawn_pos = (
                base_center[0] - enemy_size[0] // 2 + offset_x,
                base_center[1] - enemy_size[1] // 2 + offset_y
            )
            enemy = EnemySpaceship(self.enemy_image, enemy_size, spawn_pos, 2, self.earth)
            self.enemy_spaceships.append(enemy)
 

    def update_camera(self):
            self.camera_pos[0] = self.spaceship.position[0] + self.spaceship.size[0] // 2 - self.width // 2
            self.camera_pos[1] = self.spaceship.position[1] + self.spaceship.size[1] // 2 - self.height // 2
            self.camera_pos[0] = max(0, min(self.camera_pos[0], self.map_width - self.width))
            self.camera_pos[1] = max(0, min(self.camera_pos[1], self.map_height - self.height))

    def spawn_enemy(self):
        if not self.enemy_base or not self.enemy_base.alive:
            return
        enemy_size = (64, 64)
        base_center = (
            self.enemy_base.position[0] + self.enemy_base.size[0] * self.enemy_base.scale // 2,
            self.enemy_base.position[1] + self.enemy_base.size[1] * self.enemy_base.scale // 2
        )
        spawn_pos = (
            base_center[0] - enemy_size[0] // 2,
            base_center[1] - enemy_size[1] // 2
        )
        
        enemy = EnemySpaceship(self.enemy_image, enemy_size, spawn_pos, 2, self.earth)
        self.enemy_spaceships.append(enemy)

        
    def run(self):

        # Oyun döngüsü
        running = True
        while running:
            #tema müziği
            #get_busy() ile müziğin çalıp çalmadığını kontrol eder
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("assets/Space_Stage_Assets/sounds/Skyfire.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1) # Sonsuz döngüde çal

            #space tuşuna basıldığında ateş et
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Mermi ateşleme işlemi
                    self.spaceship.fire()
        
            
            self.screen.fill((0, 0, 0)) # Ekranı temizle siyah
            
            #hareketli arka plan
            draw_scrolling_bg(self.screen, self.bg_image, self.bg_offset, self.bg_speed)
            
            for planet in self.planets:
                planet.update()
                planet.draw(self.screen, self.camera_pos)

            # Düşman gemilerinin güncellenmesi ve çizilmesi
            enemies_to_remove = []
            for idx, enemy in enumerate(self.enemy_spaceships):
                old_pos = enemy.position[:]
                enemy.update()
                for j, other in enumerate(self.enemy_spaceships):
                    if idx == j:
                        continue
                    dist = ((enemy.position[0] - other.position[0]) ** 2 + (enemy.position[1] - other.position[1]) ** 2) ** 0.5
                    if dist < 10:
                        # Çok yaklaştıysa eski pozisyona geri dön ve yeni hedef seç
                        enemy.position = old_pos
                        enemy.sprite.pos = tuple(old_pos)
                        # Yeni hedef belirle (özellikle rastgele hareket edenler için)
                        if hasattr(enemy, "destination"):
                            enemy.destination = enemy.random_destination()
                        break
                enemy.draw(self.screen, self.camera_pos)                
                if enemy.get_rect().colliderect(self.earth.get_rect()):
                    enemies_to_remove.append(enemy)
                    self.earth_bar -= 10
                
                self.enemy_spaceships = [enemy for enemy in self.enemy_spaceships if enemy.health >= 0]    
            
            for enemy in enemies_to_remove:
                for enemy in enemies_to_remove:
                    if enemy in self.enemy_spaceships:
                        self.enemy_spaceships.remove(enemy)

            for bullet in self.spaceship.bullets:
                for enemy in self.enemy_spaceships:
                    if bullet.get_rect().colliderect(enemy.get_rect()):
                        enemy.take_damage(1)
                        self.spaceship.bullets.remove(bullet)
                        break

        
            self.spaceship.update(pygame.key.get_pressed())
            self.spaceship.draw(self.screen, self.camera_pos)
            self.update_camera() # Kamera güncelle
            
            if self.enemy_base and self.enemy_base.alive:
                self.enemy_base.update()
                self.enemy_base.draw(self.screen, self.camera_pos)
                now = pygame.time.get_ticks()
                if now - self.last_enemy_spawn > 6000:  # 5 saniyede bir
                    self.spawn_enemy()
                    self.last_enemy_spawn = now
            else:
                self.enemy_base = None

            # Dünya için can barı
            pygame.draw.rect(self.screen, (100, 100, 100), (self.bar_x, self.bar_y, self.bar_width, self.bar_height))  # Arka plan
            pygame.draw.rect(self.screen, (0, 200, 0), (self.bar_x, self.bar_y, int(self.bar_width * self.earth_bar / 100), self.bar_height))  # Doluluk

            pygame.display.flip() #ekran güncelle
            
            self.clock.tick(60) # FPS ayarla

