import pygame
import numpy as np

import random


pygame.init()
pygame.mixer.init()


TILE_SIZE = 32

import tile_assets 
import Player as Player
import Enemy as Enemy
import Portal as Portal

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
for _ in range(MAX_ACTIVE_ENEMY):
    pos = get_random_walkable_position()
    if pos:
        x, y = pos
        enemies.append(Enemy.Enemy(x * TILE_SIZE, y * TILE_SIZE))

total_spawned = len(enemies)


killed_enemies = 0
TARGET_KILL = 2

portal_wait_timer = None
PORTAL_WAIT_DURATION = 1000  # ms

solid_rects = tile_assets.create_solid_rects()  # Yürünemez alanları oluştur
all_characters = enemies  # Tüm karakterleri bir listeye ekle


game_over = False
continue_button_rect = pygame.Rect(tile_assets.screen.get_width() // 2 - 80, tile_assets.screen.get_height() // 2 + 40, 160, 50)

while running:
    dt = clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Oyun bittiyse butona tıklama kontrolü
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if continue_button_rect.collidepoint(event.pos):
                print("Devam Et butonuna tıklandı!")
                # Burada başka bir oyuna geçiş fonksiyonu çağırabilirsin
                running = False

    if not game_over:
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
        # Saydam overlay
        overlay = pygame.Surface(tile_assets.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # RGBA, alpha=180 ile yarı saydam siyah
        tile_assets.screen.blit(overlay, (0, 0))

        # Tebrikler mesajı
        font_big = pygame.font.Font(None, 64)
        congrats_text = font_big.render("Tebrikler!", True, (255, 255, 0))
        tile_assets.screen.blit(congrats_text, (tile_assets.screen.get_width() // 2 - congrats_text.get_width() // 2, tile_assets.screen.get_height() // 2 - 80))

        # Devam Et butonu
        pygame.draw.rect(tile_assets.screen, (50, 200, 50), continue_button_rect)
        font_btn = pygame.font.Font(None, 36)
        btn_text = font_btn.render("Devam Et", True, (255, 255, 255))
        tile_assets.screen.blit(btn_text, (continue_button_rect.centerx - btn_text.get_width() // 2, continue_button_rect.centery - btn_text.get_height() // 2))
     
    pygame.display.update()

pygame.quit()
