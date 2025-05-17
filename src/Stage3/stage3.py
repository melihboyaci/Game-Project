import pygame, random
from .utils.planet import Planet
from .utils.views import draw_scrolling_bg, draw_earth_bar, draw_health_bar, draw_base_health_bar, game_complete_menu, game_over_menu
from .utils.spaceship import Spaceship
from .utils.camera import Camera
from .managers.enemy_manager import EnemyManager
from .managers.planet_manager import PlanetManager
from .utils.earth import Earth
from .utils.portal import Portal

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
        self.earth = Earth(
            image_path="assets/Space_Stage_Assets/sprites/planets/earth2.png",
            size=(300, 300),
            position=(
                self.map_width // 2 - 300 // 2,
                self.map_height // 2 + 300
            ),
            scale=(1.5)
        )

        self.planet_manager = PlanetManager()
        #self.planet_manager.add_planet(self.earth)
        
        self.enemy_manager = EnemyManager(self.camera, self.earth, self.earth.health)

        self.portal = Portal(
            90,
            1750,
            scale=3
        )
        portal_center_x = self.portal.rect.centerx
        portal_center_y = self.portal.rect.centery

        self.spaceship_path = "assets/Space_Stage_Assets/sprites/spaceship/main_ship/full_health.png"
        self.engine_path = "assets/Space_Stage_Assets/sprites/spaceship/main_ship/engine2_idle.png"
        self.engine_powering_path = "assets/Space_Stage_Assets/sprites/spaceship/main_ship/engine2_powering.png"
        self.gun_path = "assets/Space_Stage_Assets/sprites/spaceship/main_ship/space_gun.png"
        spaceship_size = (48, 48)
        self.spaceship_position = (
                portal_center_x - spaceship_size[0] // 2 - 25,
                portal_center_y - spaceship_size[1] -10 
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
        
        self.spaceship_emerging = True
        self.emerge_start_time = pygame.time.get_ticks()
        self.spaceship_visible = False
        self.portal_open_time = None


    def draw_game(self):
        self.screen.fill((0, 0, 0))
        draw_scrolling_bg(self.screen, self.bg_image, self.bg_offset, self.bg_speed)
        self.earth.draw(self.screen, self.camera.pos)
        self.spaceship.draw(self.screen, self.camera.pos)
        pygame.display.flip()
        
    
    def run(self):

        # Oyun döngüsü
        running = True
        while running:
            #get_busy() ile müziğin çalıp çalmadığını kontrol et
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("assets/Space_Stage_Assets/sounds/space_journey.mp3")
                pygame.mixer.music.set_volume(0.2)
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

            
            #self.planet_manager.update()
            #self.planet_manager.draw(self.screen, self.camera.pos)
            self.earth.update()
            self.earth.draw(self.screen, self.camera.pos)

            self.camera.update(self.spaceship.position, self.spaceship.size)
            

            self.portal.draw(self.screen, self.camera)
            self.portal.update()
            
            if self.portal.state == 'idle' and self.portal_open_time is None:
                self.portal_open_time = pygame.time.get_ticks()


            if self.spaceship_emerging:
                elapsed = pygame.time.get_ticks() - self.emerge_start_time
                if elapsed < 1500:
                    self.spaceship.position[1] -= 2
                else:
                    self.spaceship_emerging = False
            
            # Oyun döngüsünde, portal açıldıktan 1 saniye sonra spaceship görünsün
            if self.portal_open_time and not self.spaceship_visible:
                if pygame.time.get_ticks() - self.portal_open_time > 0:  # 1 saniye bekle
                    self.spaceship_visible = True
            
            
            if self.spaceship_visible:
                self.spaceship.update(pygame.key.get_pressed())
                self.spaceship.draw(self.screen, self.camera.pos)

            self.enemy_manager.update(self.spaceship)
            self.enemy_manager.draw(self.screen)

            print(self.spaceship.position)
            draw_earth_bar(self.screen, self.enemy_manager.earth_bar)
            draw_health_bar(self.screen, self.spaceship.health)
            if self.enemy_manager.base_vulnerable and self.enemy_manager.enemy_base.alive:
                draw_base_health_bar(self.screen, self.enemy_manager.enemy_base, self.camera, self.enemy_manager.enemy_base.health)            
            
            if self.earth.destroyed:
                print("Döngüye girdi, destroyed:", self.earth.destroyed, "explosion_time:", self.earth.explosion_time, pygame.time.get_ticks())
                wait_time = 2000
                if pygame.time.get_ticks() - self.earth.explosion_time > wait_time:
                    result = game_over_menu(self.screen)
                    if result == "restart":
                        game_loop.run(self)
                    elif result == "quit":
                        running = False
            
            pygame.display.flip() #ekran güncelle

            self.clock.tick(60) # FPS ayarla

