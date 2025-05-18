import pygame
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random


pygame.init()
pygame.mixer.init()


TILE_SIZE = 32

import tile_assets 
import Player as Player
import Enemy as Enemy
import Portal as Portal
from cutscene_utils import play_cutscene  # Cutscene fonksiyonunu ekle

pygame.display.set_caption("Tile Map Test") 


# Bu fonksiyon, haritadaki yürünebilir pozisyonları bulur ve bunlardan rastgele birini döndürür.
def get_random_walkable_position(enemy_size=(4,4)):
    walkable_positions = []
    map_h, map_w = tile_assets.map_data.shape
    solid_rects = tile_assets.create_solid_rects()
    for y in range(map_h - enemy_size[1] + 1):
        for x in range(map_w - enemy_size[0] + 1):
            # Enemy'nin kaplayacağı alanı rect olarak oluştur
            enemy_rect = pygame.Rect(
                x * TILE_SIZE,
                y * TILE_SIZE,
                enemy_size[0] * TILE_SIZE,
                enemy_size[1] * TILE_SIZE
            )
            # Eğer bu alan solid_rects ile çakışıyorsa spawn etme
            collision = False
            for solid in solid_rects:
                if enemy_rect.colliderect(solid):
                    collision = True
                    break
            if not collision:
                walkable_positions.append((x, y))
    if walkable_positions:
        return random.choice(walkable_positions)
    else:
        return None




enemies= []
MAX_TOTAL_ENEMY = 200
MAX_ACTIVE_ENEMY = 10
SPAWN_INTERVAL = 2000  # ms
last_spawn_time = pygame.time.get_ticks()
total_spawned = len(enemies)


# Portal ve player başlatma
player_start_x = 100
player_start_y = 100
player = Player.Player(player_start_x, player_start_y)
portal = Portal.Portal(
    player_start_x + player.rect.width // 4, 
    player_start_y + (player.rect.height // 4)-20, 
    scale_factor=2
)

# Sağ alt köşe için konum (portal boyutunu dikkate al)
END_PORTAL_SIZE = 64  
end_portal_x = tile_assets.screen.get_width() - 260
end_portal_y = tile_assets.screen.get_height() - 200

end_portal = None
end_portal_active = False

END_PORTAL_HITBOX_W = 25
END_PORTAL_HITBOX_H = 70


player_visible = True
player_in_end_portal = False
end_portal_idle_timer = None
END_PORTAL_IDLE_AFTER_PLAYER = 1200  # ms, karakter girdikten sonra portalın idle'da kalacağı süre


player.auto_walk = True
clock = pygame.time.Clock()
running = True

# Başlangıç Enemy spawn
for _ in range(MAX_ACTIVE_ENEMY-5):
    pos = get_random_walkable_position()
    if pos:
        x, y = pos
        enemies.append(Enemy.Enemy(x * TILE_SIZE, y * TILE_SIZE))

total_spawned = len(enemies)


killed_enemies = 0
TARGET_KILL = 1

portal_wait_timer = None
PORTAL_WAIT_DURATION = 1000  # ms

solid_rects = tile_assets.create_solid_rects()  # Yürünemez alanları oluştur
all_characters = enemies  # Tüm karakterleri bir listeye ekle


game_over = False
continue_button_rect = pygame.Rect(tile_assets.screen.get_width() // 2 - 80, tile_assets.screen.get_height() // 2 + 40, 160, 50)

death_menu_active = False
death_menu_timer = None

def start_middle_age():
    TILE_SIZE = 32
    running = True
    clock = pygame.time.Clock()
    enemies = []
    MAX_TOTAL_ENEMY = 200
    MAX_ACTIVE_ENEMY = 10
    SPAWN_INTERVAL = 2000  # ms
    last_spawn_time = pygame.time.get_ticks()
    total_spawned = len(enemies)
    player_start_x = 100
    player_start_y = 100
    player = Player.Player(player_start_x, player_start_y)
    portal = Portal.Portal(
        player_start_x + player.rect.width // 4, 
        player_start_y + (player.rect.height // 4)-20, 
        scale_factor=2
    )
    END_PORTAL_SIZE = 64  
    end_portal_x = tile_assets.screen.get_width() - 260
    end_portal_y = tile_assets.screen.get_height() - 200
    end_portal = None
    end_portal_active = False
    END_PORTAL_HITBOX_W = 25
    END_PORTAL_HITBOX_H = 70
    player_visible = True
    player_in_end_portal = False
    end_portal_idle_timer = None
    END_PORTAL_IDLE_AFTER_PLAYER = 1200  # ms
    player.auto_walk = True
    # Başlangıç Enemy spawn
    for _ in range(MAX_ACTIVE_ENEMY-5):
        pos = get_random_walkable_position()
        if pos:
            x, y = pos
            enemies.append(Enemy.Enemy(x * TILE_SIZE, y * TILE_SIZE))
    total_spawned = len(enemies)
    killed_enemies = 0
    TARGET_KILL = 1
    portal_wait_timer = None
    PORTAL_WAIT_DURATION = 1000  # ms
    solid_rects = tile_assets.create_solid_rects()  # Yürünemez alanları oluştur
    all_characters = enemies  # Tüm karakterleri bir listeye ekle
    game_over = False
    continue_button_rect = pygame.Rect(tile_assets.screen.get_width() // 2 - 80, tile_assets.screen.get_height() // 2 + 40, 160, 50)
    death_menu_active = False
    death_menu_timer = None
    while running:
        if death_menu_active:
            # Ölümden sonra 1 saniye bekle
            if death_menu_timer is not None and pygame.time.get_ticks() - death_menu_timer < 1000:
                continue
            def draw_game():
                tile_assets.screen.fill((0, 0, 0))
                tile_assets.draw_map()
                if not portal.finished:
                    portal.draw(tile_assets.screen)
                if end_portal_active and end_portal is not None:
                    end_portal.update()
                    end_portal.draw_flipped(tile_assets.screen)
                for enemy in enemies:
                    enemy.draw(tile_assets.screen)
                font = pygame.font.Font(None, 36)
                text = font.render(f"{killed_enemies}/{TARGET_KILL}", True, (255, 255, 255))
                tile_assets.screen.blit(text, (tile_assets.screen.get_width() // 2 - 40, 20))
            result = game_over_menu(tile_assets.screen, draw_game)
            if result == 'restart':
                return start_middle_age()
            elif result == 'quit':
                pygame.quit()
                import sys; sys.exit()
            continue

        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys; sys.exit()

            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button_rect.collidepoint(event.pos):
                    print("Devam Et butonuna tıklandı!")
                    running = False

        if not game_over and not death_menu_active:

            if player.state == "death":
                # Ölüm animasyonu bittiyse menüyü aç
                if player.frame_index >= len(player.animations["death"][player.direction]) - 1:
                    if not death_menu_active:
                        death_menu_active = True
                        death_menu_timer = pygame.time.get_ticks()

            # --- Oyun güncellemeleri ---
            if not end_portal_active and killed_enemies >= TARGET_KILL:
                end_portal = Portal.Portal(end_portal_x, end_portal_y, scale_factor=2)
                end_portal_active = True
                print("Tebrikler! 200 düşman öldürdünüz.")
                

            # --- Otomatik düşman spawn kontrolü ---
            if len(enemies) < MAX_ACTIVE_ENEMY and total_spawned < MAX_TOTAL_ENEMY and now - last_spawn_time > SPAWN_INTERVAL:
                pos = get_random_walkable_position()
                if pos:
                    x, y = pos
                    enemies.append(Enemy.Enemy(x * TILE_SIZE, y * TILE_SIZE))
                    total_spawned += 1
                    last_spawn_time = now

            # --- PORTAL VE PLAYER ANİMASYONLARI ---
            if not portal.finished:
                portal.update()

            # PORTAL "idle" durumuna geçtiyse sadece portal_wait_timer başlat
            if portal.state == "idle" and portal_wait_timer is None:
                portal_wait_timer = pygame.time.get_ticks()

            # --- OYUN BAŞLANGIÇ AKIŞI ---
            if player.auto_walk:
                player.auto_walk_forward(distance=64)

            # PORTAL_WAIT_DURATION sadece portalı etkiler, oyun akışı devam eder
            if portal_wait_timer is not None:
                elapsed = pygame.time.get_ticks() - portal_wait_timer
                if elapsed >= PORTAL_WAIT_DURATION:
                    print("Portal kapanıyor!")
                    portal.state = "close"
                    portal.frame_index = 0
                    portal_wait_timer = None

            # Oyun her zamanki gibi devam eder
            if player.can_control:
                player.handle_input(solid_rects, all_characters)
                player.attack(enemies)
            player.update()

            # Enemy update ve animasyonları
            for enemy in enemies[:]:
                if not enemy.alive:
                    enemies.remove(enemy)
                    killed_enemies += 1
                else:
                    other_enemies = [e for e in enemies if e is not enemy]
                    chars = [player] + other_enemies
                    enemy.update(player, solid_rects, chars)
                    enemy.update_animation()

        # --- ÇİZİM ---
        tile_assets.screen.fill((0, 0, 0))
        tile_assets.draw_map()

        if not portal.finished:
            portal.draw(tile_assets.screen)

        if end_portal_active and end_portal is not None:
            end_portal.update()
            end_portal.draw_flipped(tile_assets.screen)

            # Küçük hitbox ile çarpışma kontrolü
            portal_hitbox = pygame.Rect(
                end_portal.x + end_portal.animations["idle"][0].get_width() // 2 - END_PORTAL_HITBOX_W // 2,
                end_portal.y + end_portal.animations["idle"][0].get_height() // 2 - END_PORTAL_HITBOX_H // 2,
                END_PORTAL_HITBOX_W,
                END_PORTAL_HITBOX_H
            )
            if portal_hitbox.colliderect(player.rect) and end_portal.state == "idle" and not player_in_end_portal:
                player_visible = False
                player_in_end_portal = True
                end_portal_idle_timer = pygame.time.get_ticks()

            if player_in_end_portal and end_portal_idle_timer is not None:
                elapsed = pygame.time.get_ticks() - end_portal_idle_timer
                if elapsed >= END_PORTAL_IDLE_AFTER_PLAYER and end_portal.state == "idle":
                    end_portal.state = "close"
                    end_portal.frame_index = 0
                    end_portal_idle_timer = None

            if end_portal.state == "close" and end_portal.finished:
                if not game_over:
                    print("Tebrikler! Bölüm bitti.")
                    game_over = True
            # pygame.draw.rect(tile_assets.screen, (255,0,0), portal_hitbox, 2)  # hitbox'ı görsel olarak test etmek için


        

        if player_visible:
            player.draw(tile_assets.screen)

            
        for enemy in enemies:
            enemy.draw(tile_assets.screen)

        font = pygame.font.Font(None, 36)
        text = font.render(f"{killed_enemies}/{TARGET_KILL}", True, (255, 255, 255))
        tile_assets.screen.blit(text, (tile_assets.screen.get_width() // 2 - 40, 20))

        # --- Oyun bitti overlay ve buton ---
        if game_over:
            def draw_game():
                tile_assets.screen.fill((0, 0, 0))
                tile_assets.draw_map()
                if not portal.finished:
                    portal.draw(tile_assets.screen)
                if end_portal_active and end_portal is not None:
                    end_portal.update()
                    end_portal.draw_flipped(tile_assets.screen)
                if player_visible:
                    player.draw(tile_assets.screen)
                for enemy in enemies:
                    enemy.draw(tile_assets.screen)
                font = pygame.font.Font(None, 36)
                text = font.render(f"{killed_enemies}/{TARGET_KILL}", True, (255, 255, 255))
                tile_assets.screen.blit(text, (tile_assets.screen.get_width() // 2 - 40, 20))
            result = stage_complete_menu(tile_assets.screen, draw_game)
            if result == 'next':
                return 'next'
            elif result == 'restart':
                return start_middle_age()
            elif result == 'quit':
                pygame.quit()
                import sys; sys.exit()

        pygame.display.update()

    return "next"

# Eğer bu dosya doğrudan çalıştırılırsa eski davranış devam etsin
def main():
    start_middle_age()

# --- STAGE COMPLETE MENU ---
def stage_complete_menu(screen, draw_game_callback):
    options = ['Continue', 'Try Again', 'Quit']
    selected = 0
    box_width = screen.get_width()
    box_height = screen.get_height()
    box_color = (0, 0, 0, 180)
    font = pygame.font.Font("assets/fonts/menu.TTF", 48)
    btn_font = pygame.font.Font("assets/fonts/menu.TTF", 36)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if options[selected] == 'Continue':
                        return 'next'
                    elif options[selected] == 'Try Again':
                        return 'restart'
                    elif options[selected] == 'Quit':
                        return 'quit'
        # Draw game background first
        if draw_game_callback:
            draw_game_callback()
        # Draw overlay
        overlay = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        overlay.fill(box_color)
        screen.blit(overlay, (0, 0))
        # Title
        title_text = font.render('STAGE COMPLETED', True, (0, 255, 0))
        title_x = screen.get_width() // 2 - title_text.get_width() // 2
        title_y = screen.get_height() // 2 - 120
        screen.blit(title_text, (title_x, title_y))
        # Options
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            option_text = btn_font.render(option, True, color)
            option_x = screen.get_width() // 2 - option_text.get_width() // 2
            option_y = screen.get_height() // 2 + i * 40
            screen.blit(option_text, (option_x, option_y))
        pygame.display.flip()
        pygame.time.Clock().tick(30)

# --- GAME OVER MENU ---
def game_over_menu(screen, draw_game_callback):
    options = ['Try Again', 'Quit']
    selected = 0
    box_width = screen.get_width()
    box_height = screen.get_height()
    box_color = (0, 0, 0, 180)
    font = pygame.font.Font("assets/fonts/menu.TTF", 48)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if options[selected] == 'Try Again':
                        return 'restart'
                    elif options[selected] == 'Quit':
                        return 'quit'
        if draw_game_callback:
            draw_game_callback()
        overlay = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        overlay.fill(box_color)
        screen.blit(overlay, (0, 0))
        title_text = font.render('GAME OVER', True, (255, 0, 0))
        title_x = screen.get_width() // 2 - title_text.get_width() // 2
        title_y = screen.get_height() // 2 - 120
        screen.blit(title_text, (title_x, title_y))
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            option_text = font.render(option, True, color)
            option_x = screen.get_width() // 2 - option_text.get_width() // 2
            option_y = screen.get_height() // 2 + i * 40
            screen.blit(option_text, (option_x, option_y))
        pygame.display.flip()
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()