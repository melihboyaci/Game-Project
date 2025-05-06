import pygame
from utils.planet import Planet
import random
from utils.animation import AnimatedSprite, load_sprite_sheet
from utils.views import draw_scrolling_bg
from utils.spaceship import Spaceship

class game_loop:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = screen.get_size()
        self.bg_offset = {'x': 0, 'y': 0}
        self.bg_speed  = {'x': -0.1, 'y': 0.2}
        self.bg_image = pygame.image.load("assets/Space_Stage_Assets/ui/backgrounds/space4.png").convert_alpha()        
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        random.seed(19)
        self.map_width = 2000
        self.map_height = 2000

        self.camera_pos = [0, 0]

        
        self.planet_count = 7
        self.planet_sizes = [
            (100, 100),
            (100, 100),
            (300, 300),
            (100, 100),
            (100, 100),
            (100, 100),
            (100, 100),
        ]

        self.planets = []
        for i in range(self.planet_count):
            planet_path = f"assets/Space_Stage_Assets/sprites/planets/planet{i+1}.png"
            size = self.planet_sizes[i]
            max_attempts = 100 # Maksimum deneme sayısı
            for attempt in range(max_attempts):
                position = (
                    random.randint(0, self.map_width - size[0]), 
                    random.randint(0, self.map_height - size[1])
                    )
                new_rect = pygame.Rect(position, size)
                if all(not new_rect.colliderect(p.get_rect()) for p in self.planets):
                    break
            else:
                pass
            planet = Planet(planet_path, size, position)
            self.planets.append(planet)

        self.spaceship_path = "assets/Space_Stage_Assets/sprites/spaceship/1.png"
        self.engine_path = "assets/Space_Stage_Assets/sprites/spaceship/engine.png"

        self.spaceship_position = (self.width // 2, self.height // 2)
        self.spaceship_speed = 5
        self.spaceship = Spaceship(self.spaceship_path, (64, 64), self.spaceship_position, self.spaceship_speed, engine_path=self.engine_path, engine_size=(41, 30))    
        
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
            
            #hareketli arka plan
            draw_scrolling_bg(self.screen, self.bg_image, self.bg_offset, self.bg_speed)

            for planet in self.planets:
                planet.update()
                planet.draw(self.screen, self.camera_pos)


        
            self.spaceship.update(pygame.key.get_pressed())

            self.spaceship.draw(self.screen, self.camera_pos)

            self.update_camera() # Kamera güncelle



            pygame.display.flip() #ekran güncelle
            
            self.clock.tick(60) # FPS ayarla

