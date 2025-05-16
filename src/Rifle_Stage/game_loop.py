import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    PLAYER_START_X, PLAYER_START_Y, PLAYER_SPEED, PLAYER_BULLETS,
    ENEMY_COUNT, ENEMY_MIN_DISTANCE
)
from soldier import Player
from enemy import EnemyManager
from background import Background
from ui import draw_ui
from collision_manager import CollisionManager
from settings import ENEMY_DAMAGE
from objects import Portal

def start_game():
    while True:
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

        bullet_icon = pygame.image.load("assets/Rifle_Stage_Assets/images/bullet_icon.png")
        hp_icon = pygame.image.load("assets/Rifle_Stage_Assets/images/hp_icon.png")
        enemy_icon = pygame.image.load("assets/Rifle_Stage_Assets/images/enemy_icon.png")
        ultimate_icon = pygame.image.load("assets/Rifle_Stage_Assets/images/ultimate_icon.png")
        font = pygame.font.SysFont(None, 36)

        background = Background()
        # Düşmanlar baştan oluşturulacak ve sahnede bekleyecek
        enemy_manager = EnemyManager(num_enemies=ENEMY_COUNT, min_distance=ENEMY_MIN_DISTANCE)
        enemy_manager.spawn_enemies(background.get_blocks())
        # Portal ile giriş
        portal_x = PLAYER_START_X + 40  # Karakterin ortasına göre ayarla
        portal_y = PLAYER_START_Y + 30
        portal = Portal(portal_x, portal_y, scale=2)
        player = None
        portal_group = pygame.sprite.Group(portal)
        portal_sequence_done = False
        clock = pygame.time.Clock()
        sequence_timer = 0
        sequence_state = 'portal_opening'  # 'portal_opening', 'player_spawn', 'portal_closing', 'done'
        while not portal_sequence_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            background.draw(screen)
            enemy_manager.draw(screen, background.get_blocks())  # Düşmanlar sadece çizilecek, hareket etmeyecek
            portal_group.update()
            portal_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
            if sequence_state == 'portal_opening' and portal.state == 'idle':
                player = Player(PLAYER_START_X, PLAYER_START_Y, PLAYER_SPEED, PLAYER_BULLETS)
                sequence_timer = pygame.time.get_ticks()
                sequence_state = 'player_spawn'
            elif sequence_state == 'player_spawn' and pygame.time.get_ticks() - sequence_timer > 700:
                portal.start_closing()
                sequence_state = 'portal_closing'
            elif sequence_state == 'portal_closing' and portal.state == 'finished':
                portal_sequence_done = True
        result = game_loop(screen, background, player, enemy_manager, font, bullet_icon, hp_icon, enemy_icon, ultimate_icon, FPS)
        if result == 'quit':
            break

def game_loop(screen, background, player, enemy_manager, font, bullet_icon, hp_icon, enemy_icon, ultimate_icon, FPS):
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 'quit'
        keys = pygame.key.get_pressed()
        old_rect = player.rect.copy()
        old_collision_rect = player.collision_rect.copy()
        player.update(keys, screen.get_width(), screen.get_height())
        if getattr(player, 'death_animation_finished', False):
            return 'restart'
        enemy_manager.update(player, background.get_blocks())
        if CollisionManager.check_player_block_collision(player, background.get_blocks()):
            player.rect = old_rect
            player.collision_rect = old_collision_rect
        for enemy in enemy_manager.enemies:
            for bullet in enemy.bullet_sprites.sprites():
                if player.collision_rect.colliderect(bullet.rect):
                    player.take_damage(ENEMY_DAMAGE)
                    bullet.kill()
        for bullet in player.bullet_sprites.sprites():
            if CollisionManager.check_bullet_block_collision(bullet, background.get_blocks()):
                bullet.kill()
                continue
            for enemy in enemy_manager.enemies:
                collision, damage = CollisionManager.check_bullet_enemy_collision(bullet, enemy)
                if collision:
                    if enemy.take_damage(damage):
                        pass
                    bullet.kill()
                    break
        background.draw(screen)
        player.draw(screen, background.get_blocks())
        enemy_manager.draw(screen, background.get_blocks())
        draw_ui(screen, player, enemy_manager, bullet_icon, hp_icon, enemy_icon, ultimate_icon, font)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit() 