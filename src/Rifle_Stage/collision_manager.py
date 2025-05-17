import pygame
from settings import SPRITE_SCALE, PLAYER_DAMAGE, PLAYER_HEADSHOT_DAMAGE

class CollisionManager:
    @staticmethod
    def check_player_block_collision(player, blocks):
        """Oyuncu ve bloklar arasındaki çarpışmayı kontrol eder"""
        for block in blocks:
            if block.collidable and player.collision_rect.colliderect(block.rect):
                return True
        return False

    @staticmethod
    def check_enemy_bullet_player_collision(enemy, player):
        """Düşman mermisi ve oyuncu arasındaki çarpışmayı kontrol eder"""
        if enemy.firing:
            if enemy.facing_right:
                bullet_start = (enemy.rect.left + 11.5*SPRITE_SCALE, enemy.rect.top + 6*SPRITE_SCALE)
                bullet_end = (bullet_start[0] + 73*SPRITE_SCALE, bullet_start[1])
            else:
                bullet_start = (enemy.rect.left + 0, enemy.rect.top + 6*SPRITE_SCALE)
                bullet_end = (bullet_start[0] - 73*SPRITE_SCALE, bullet_start[1])
            
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
            is_headshot = enemy.collision_rect.top-10 <= bullet.rect.centery <= enemy.collision_rect.top + 5*SPRITE_SCALE
            if is_headshot:
                print("Kafa vuruşu!")
            damage = PLAYER_HEADSHOT_DAMAGE if is_headshot else PLAYER_DAMAGE
            return True, damage
        return False, 0

    @staticmethod
    def check_bullet_block_collision(bullet, blocks):
        """Mermi sprite'ı ve bloklar arasındaki çarpışmayı kontrol eder"""
        for block in blocks:
            if block.collidable and bullet.rect.colliderect(block.rect):
                return True
        return False 
    
    @staticmethod
    def check_enemy_block_collision(enemy, blocks):
        """Düşman sprite'ı ve bloklar arasındaki çarpışmayı kontrol eder"""
        for block in blocks:
            if block.collidable and enemy.collision_rect.colliderect(block.rect):
                return True
        return False
