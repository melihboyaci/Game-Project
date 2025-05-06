import pygame
from utils.planet import Planet
import random
from utils.animation import AnimatedSprite, load_sprite_sheet
from utils.views import draw_scrolling_bg
from utils.spaceship import Spaceship
from utils.enemy_spaceship import EnemySpaceship

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


        ## Gezegenlerin boyutları ve konumları
        self.planet_count = 6
        self.planet_sizes = [
            (100, 100),
            (300, 300),
            (100, 100),
            (100, 100),
            (100, 100),
            (100, 100),
        ]

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
                self.map_height // 2 - 300 // 2
                )
        Earth = Planet(earth_path, earth_size, earth_pos, scale=(1.5))    
        self.planets.append(Earth) # Dünya
        self.earth = Earth

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
        self.enemy_image = "assets/Space_Stage_Assets/sprites/spaceship/2.png"
        for i in range(5):
            max_attempts = 100 # Maksimum deneme sayısı
            for attempt in range(max_attempts):
                base_pos = (random.randint(100, 400), random.randint(100, 400))
                new_rect = pygame.Rect(base_pos, (64, 64))  # base alanı
                if all (not new_rect.colliderect(e.get_rect()) for e in self.enemy_spaceships):
                    break
            
            enemy = EnemySpaceship(self.enemy_image, (64, 64), base_pos, 2, self.earth)
            self.enemy_spaceships.append(enemy)

    def update_camera(self):
            self.camera_pos[0] = self.spaceship.position[0] + self.spaceship.size[0] // 2 - self.width // 2
            self.camera_pos[1] = self.spaceship.position[1] + self.spaceship.size[1] // 2 - self.height // 2
            self.camera_pos[0] = max(0, min(self.camera_pos[0], self.map_width - self.width))
            self.camera_pos[1] = max(0, min(self.camera_pos[1], self.map_height - self.height))
            
        
    def run(self):
       
    
        # Oyun döngüsü
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Mermi ateşleme işlemi
                    self.spaceship.fire()
            
            self.screen.fill((0, 0, 0)) # Ekranı temizle siyah
            bar_width = 300
            bar_height = 20
            bar_x = (self.width - bar_width) // 2
            bar_y = 20
        
            
            #hareketli arka plan
            draw_scrolling_bg(self.screen, self.bg_image, self.bg_offset, self.bg_speed)

            for planet in self.planets:
                planet.update()
                planet.draw(self.screen, self.camera_pos)

            enemies_to_remove = []
            for enemy in self.enemy_spaceships[:]:  # Iterate over a copy of the list
                enemy.update()
                enemy.draw(self.screen, self.camera_pos)
                if enemy.get_rect().colliderect(self.earth.get_rect()):
                    enemies_to_remove.append(enemy)
                    self.earth_bar -= 10
            for enemy in enemies_to_remove:
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

            pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))  # Arka plan
            pygame.draw.rect(self.screen, (0, 200, 0), (bar_x, bar_y, int(bar_width * self.earth_bar / 100), bar_height))  # Doluluk

            pygame.display.flip() #ekran güncelle
            
            self.clock.tick(60) # FPS ayarla

