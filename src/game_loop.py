import pygame, random
from utils.planet import Planet
from utils.views import draw_scrolling_bg, draw_earth_bar, draw_health_bar, draw_base_health_bar
from utils.spaceship import Spaceship
from utils.camera import Camera
from managers.enemy_manager import EnemyManager
from managers.planet_manager import PlanetManager

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
        self.earth_bar = 100
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.last_enemy_spawn = pygame.time.get_ticks()
        
        self.camera = Camera(self.width, self.height, self.map_width, self.map_height)

        # Dünya
        self.earth = Planet(
            image_path="assets/Space_Stage_Assets/sprites/planets/earth2.png",
            size=(300, 300),
            position=(
                self.map_width // 2 - 300 // 2,
                self.map_height // 2 + 300
            ),
            scale=(1.5)
        )

        self.planet1 = Planet(
            image_path="assets/Space_Stage_Assets/sprites/planets/planet2.png",
            size=(100, 100),
            position=(
                random.randint(0, self.map_width - 100),
                random.randint(0, self.map_height - 100)
            ),
            scale=(1)
        )

        self.planet_manager = PlanetManager()
        self.planet_manager
        self.planet_manager.add_planet(self.earth)
        
        self.enemy_manager = EnemyManager(self.camera, self.earth, self.earth_bar)


        self.spaceship_path = "assets/Space_Stage_Assets/sprites/spaceship/main_ship/full_health.png"
        self.engine_path = "assets/Space_Stage_Assets/sprites/spaceship/main_ship/engine2_idle.png"
        self.engine_powering_path = "assets/Space_Stage_Assets/sprites/spaceship/main_ship/engine2_powering.png"
        self.gun_path = "assets/Space_Stage_Assets/sprites/spaceship/main_ship/space_gun.png"
        spaceship_size = (48, 48)
        self.spaceship_position = (
            self.earth.position[0] + self.earth.size[0] // 2 - spaceship_size[0] // 2 + 70,
            self.earth.position[1] - spaceship_size[1] - 20
        )
        self.spaceship_speed = 6
        self.spaceship = Spaceship(
            self.spaceship_path, 
            spaceship_size, 
            self.spaceship_position, 
            self.spaceship_speed, 
            engine_path=self.engine_path, 
            engine_size=(48, 48), scale=3, 
            engine_powering_path=self.engine_powering_path, 
            gun_path=self.gun_path
        )

    def run(self):

        # Oyun döngüsü
        running = True
        while running:
            #get_busy() ile müziğin çalıp çalmadığını kontrol et
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("assets/Space_Stage_Assets/sounds/space_journey.mp3")
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
            

            self.planet_manager.update()
            self.planet_manager.draw(self.screen, self.camera.pos)

            self.camera.update(self.spaceship.position, self.spaceship.size)
            self.spaceship.update(pygame.key.get_pressed())
            self.spaceship.draw(self.screen, self.camera.pos)
            self.enemy_manager.update(self.spaceship)
            self.enemy_manager.draw(self.screen)

            draw_earth_bar(self.screen, self.enemy_manager.earth_bar)
            draw_health_bar(self.screen, self.spaceship.health)
            if self.enemy_manager.base_vulnerable and self.enemy_manager.enemy_base.alive:
                draw_base_health_bar(self.screen, self.enemy_manager.enemy_base, self.camera, self.enemy_manager.enemy_base.health)            
            
            pygame.display.flip() #ekran güncelle

            self.clock.tick(60) # FPS ayarla

