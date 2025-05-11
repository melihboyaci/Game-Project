import pygame, random
from utils.enemy_spaceship import EnemySpaceship
from utils.enemybase import EnemyBase

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

        self.enemies = []
        self.spawn_time = 4000
        self.last_spawn_time = pygame.time.get_ticks()

    def spawn_enemy(self):
        if not self.enemy_base.alive:
            return
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

        enemy = EnemySpaceship(
            image_path="assets/Space_Stage_Assets/sprites/spaceship/2.png",
            size=size,
            position=spawn_pos,
            speed=3.5,
            target=self.earth,
        )
        self.enemies.append(enemy)

    def update(self, spaceship=None):
        if not self.enemy_base.alive:
            return
        self.enemy_base.update()
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time > self.spawn_time:
            self.spawn_enemy()
            self.last_spawn_time = now

        enemies_to_remove = []
        for enemy in self.enemies:
            enemy.update()
            if enemy.get_rect().colliderect(self.earth.get_rect()):
                enemies_to_remove.append(enemy)
                self.earth_bar -= 10
            if spaceship:
                for bullet in spaceship.bullets:
                    for enemy in self.enemies:
                        if bullet.get_rect().colliderect(enemy.get_rect()):
                            enemy.take_damage(1)
                            spaceship.bullets.remove(bullet)
                            break

        self.enemies = [enemy for enemy in self.enemies if enemy.health >= 0]

        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)
            if enemy in self.enemies:
                self.enemies.remove(enemy)

    def draw(self, screen):
        if self.enemy_base.alive:
            self.enemy_base.draw(screen, self.camera.pos)
        for enemy in self.enemies:
            enemy.draw(screen, self.camera.pos)