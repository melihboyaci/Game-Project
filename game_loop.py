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
        self.bg_image = pygame.image.load("assets/ui/backgrounds/space4.png").convert_alpha()        
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        random.seed(27)

        
        self.planet_count = 4
        self.planet_sizes = [
            (100, 100),
            (100, 100),
            (300, 300),
            (100, 100),
        ]

        self.planets = []
        for i in range(self.planet_count):
            planet_path = f"assets/sprites/planets/planet{i+1}.png"
            size = self.planet_sizes[i]
            position = (
                random.randint(0, self.width - size[0]), 
                random.randint(0, self.height - size[1])
                )
            planet = Planet(planet_path, size, position)
            self.planets.append(planet)

        self.spaceship_path = "assets/sprites/spaceship/1.png"
        self.spaceship_position = (self.width // 2, self.height // 2)
        self.spaceship_speed = 5
        self.spaceship = Spaceship(self.spaceship_path, self.spaceship_size, self.spaceship_position, self.spaceship_speed, )    
        
            

    def run(self):
       
    
        # Oyun döngüsü
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.screen.fill((0, 0, 0)) # Ekranı temizle siyah
            
            #hareketli arka plan
            draw_scrolling_bg(self.screen, self.bg_image, self.bg_offset, self.bg_speed)

            for planet in self.planets:
                planet.update()
                planet.draw(self.screen)


        
            self.spaceship.update(pygame.key.get_pressed(), self.width, self.height)
            self.spaceship.draw(self.screen)
            


            pygame.display.flip() #ekran güncelle
            
            self.clock.tick(60) # FPS ayarla

