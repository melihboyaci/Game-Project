import pygame
from ..utils.enemy_spaceship import EnemySpaceship
from ..utils.enemybase import EnemyBase
from ..utils.animation import load_sprite_sheet, AnimatedSprite
ENEMY_COUNT = 0
class EnemyManager:
    def __init__(self, camera, earth, earth_bar):
        self.camera = camera
        self.earth = earth
        self.earth_bar = earth_bar

               

        base_path = "assets/Space_Stage_Assets/sprites/enemybase/base.png"
        base_size = (128, 128)
        corners = [
            (0, 0),  # Sol Üst
            (self.camera.map_width - base_size[0], 0),  # Sağ Üst
            (0, self.camera.map_height - base_size[1]),  # Sol Alt
            (self.camera.map_width - base_size[0], self.camera.map_height - base_size[1])  # Sağ Alt
        ]
        max_distance = -1
        base_pos = None
        for corner in corners:
            distance = ((corner[0] - earth.position[0]) ** 2 + (corner[1] - earth.position[1]) ** 2) ** 0.5
            if distance > max_distance:
                max_distance = distance
                base_pos = corner
        
        self.enemy_base = EnemyBase(base_path, base_size, base_pos)
        self.base_vulnerable = False

        self.enemies = []
        self.spawn_time = 2000
        self.last_spawn_time = pygame.time.get_ticks()
        self.wave = 1
        self.max_enemies = 10
        self.enemy_types = [
            {
                "image_path": "assets/Space_Stage_Assets/sprites/spaceship/enemy_fighter/fighter_base.png",
                "size": (64, 64),
                "engine_path": "assets/Space_Stage_Assets/sprites/spaceship/enemy_fighter/fighter_engine.png",
                "engine_size": (64, 64),
                "scale": 1.7
            },
            {
                "image_path": "assets/Space_Stage_Assets/sprites/spaceship/enemy_torpedo/torpedo_base.png",
                "size": (64, 64),
                "engine_path": "assets/Space_Stage_Assets/sprites/spaceship/enemy_torpedo/torpedo_engine.png",
                "engine_size": (64, 64),
                "scale": 2
            }
        ]

        self.enemies_this_wave = 0

    def spawn_enemy(self):   
            if self.wave >= 3:
                return

            if not self.enemy_base.alive:
                return
            
            if self.wave % 2 == 0:
                enemy_type = self.enemy_types[1]
            else:
                enemy_type = self.enemy_types[0]

            base = self.enemy_base
            size = (64, 64)
            base_center = (
                base.position[0] + base.size[0] * base.scale // 2,
                base.position[1] + base.size[1] * base.scale // 2
            )
            spawn_pos = (
                base_center[0] - size[0] // 2,
                base_center[1] - size[1] // 2
            )
            enemy_type = self.enemy_types[(self.wave - 1) % len(self.enemy_types)]

            enemy = EnemySpaceship(
                image_path=enemy_type["image_path"],
                size=size,
                position=spawn_pos,
                speed=3.2,
                target=self.earth,
                engine_path=enemy_type["engine_path"],
                engine_size=enemy_type["engine_size"],
                scale=enemy_type["scale"],
                enemy_type="torpedo" if (self.wave - 1) % len(self.enemy_types) == 1 else "fighter"
            )
            self.enemies.append(enemy)
            self.enemies_this_wave += 1

    def update(self, spaceship=None):
        #if not self.enemy_base.alive:
            #return
        self.enemy_base.update()
        now = pygame.time.get_ticks()
        if self.enemies_this_wave < self.max_enemies:
            if now - self.last_spawn_time > self.spawn_time:
                self.spawn_enemy()
                self.last_spawn_time = now

        enemies_to_remove = []
        for i, enemy in enumerate(self.enemies):
            enemy.update(spaceship)
            for j, other_enemy in enumerate(self.enemies):
                if i != j and enemy.get_rect().colliderect(other_enemy.get_rect()):
                    # Çarpışma varsa iki gemiyi hafifçe it
                    dx = enemy.position[0] - other_enemy.position[0]
                    dy = enemy.position[1] - other_enemy.position[1]
                    dist = max((dx**2 + dy**2) ** 0.5, 1)
                    push_strength = 8  # İtme kuvveti (deneyerek ayarlayabilirsin)
                    enemy.position[0] += (dx / dist) * push_strength
                    enemy.position[1] += (dy / dist) * push_strength
                    enemy.sprite.pos = tuple(enemy.position)
                    # Diğer gemiyi de ters yöne itmek istersen:
                    other_enemy.position[0] -= (dx / dist) * push_strength
                    other_enemy.position[1] -= (dy / dist) * push_strength
                    other_enemy.sprite.pos = tuple(other_enemy.position)
                    break
            if enemy.get_rect().colliderect(self.earth.get_rect()):
                enemies_to_remove.append(enemy)
                self.earth_bar -= 10
            for bullet in spaceship.bullets[:]:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    enemy.take_damage(1)
                    spaceship.bullets.remove(bullet)
                    break
            #mermi oyuncu gemisi çarpışması
            if spaceship:
                for bullet in enemy.bullets[:]:
                    if bullet.get_rect().colliderect(spaceship.get_rect()):
                        spaceship.take_damage(1)
                        enemy.bullets.remove(bullet)
                        break
        if spaceship:
            for bullet in spaceship.bullets[:]:
                if self.enemy_base.alive:
                    if self.base_vulnerable and bullet.get_rect().colliderect(self.enemy_base.get_rect()):
                        self.enemy_base.take_damage(1)
                        spaceship.bullets.remove(bullet)
                        break

        self.enemies = [enemy for enemy in self.enemies if enemy.health >= 0 and enemy not in enemies_to_remove]

         # --- DÜZELTİLMİŞ DALGA BİTİŞ KONTROLÜ ---
        if self.wave == 2 and self.enemies_this_wave == self.max_enemies and len(self.enemies) == 0:
            self.base_vulnerable = True
            print("Base artık vulnerable!")  # Debug için
        
        if len(self.enemies) == 0 and self.enemies_this_wave == self.max_enemies:
            self.wave += 1
            self.enemies_this_wave = 0
            self.last_spawn_time = now

    def draw(self, screen):
        self.enemy_base.draw(screen, self.camera.pos)
        for enemy in self.enemies:
            enemy.draw(screen, self.camera.pos)

    def get_enemy_count(self):
        return len(self.enemies)