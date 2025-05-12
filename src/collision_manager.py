import pygame
from settings import ENEMY_DAMAGE

class CollisionManager:
    @staticmethod
    def check_player_block_collision(player, blocks):
        """Oyuncu ve bloklar arasındaki çarpışmayı kontrol eder"""
        for block in blocks:
            if player.collision_rect.colliderect(block.rect):
                return True
        return False

    @staticmethod
    def check_enemy_bullet_player_collision(enemy, player):
        """Düşman mermisi ve oyuncu arasındaki çarpışmayı kontrol eder"""
        if enemy.firing:
            if enemy.facing_right:
                bullet_start = (enemy.rect.left + 23, enemy.rect.top + 12)
                bullet_end = (bullet_start[0] + 146, bullet_start[1])
            else:
                bullet_start = (enemy.rect.left + 0, enemy.rect.top + 12)
                bullet_end = (bullet_start[0] - 146, bullet_start[1])
            
            bullet_rect = pygame.Rect(
                min(bullet_start[0], bullet_end[0]), 
                min(bullet_start[1], bullet_end[1]),
                abs(bullet_end[0] - bullet_start[0]),
                abs(bullet_end[1] - bullet_start[1])
            )
            
            if bullet_rect.colliderect(player.collision_rect):
                return True
        return False

    @staticmethod
    def check_bullet_enemy_collision(bullet, enemy):
        """Mermi sprite'ı ve düşman arasındaki çarpışmayı kontrol eder"""
        if bullet.rect.colliderect(enemy.collision_rect):
            # Kafa vuruşu kontrolü - düşmanın üst 10 piksellik kısmı
            is_headshot = enemy.collision_rect.top <= bullet.rect.centery <= enemy.collision_rect.top + 10
            if is_headshot:
                print("Kafa vuruşu!")
            damage = 100 if is_headshot else ENEMY_DAMAGE
            return True, damage
        return False, 0

    @staticmethod
    def check_bullet_block_collision(bullet, blocks):
        """Mermi sprite'ı ve bloklar arasındaki çarpışmayı kontrol eder"""
        for block in blocks:
            if bullet.rect.colliderect(block.rect):
                return True
        return False 