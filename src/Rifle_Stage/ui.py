import pygame

def draw_ui(surface, player, enemy_manager, bullet_icon, hp_icon, enemy_icon, ultimate_icon, font):
    # Mermi ikonu ve sayısı
    surface.blit(bullet_icon, (1200, 10))
    bullet_text = font.render(f"{player.bullets}", True, (255, 255, 255))
    surface.blit(bullet_text, (1230, 10))

    # Can ikonu ve sayısı
    surface.blit(hp_icon, (1200, 35))
    health_text = font.render(f"{player.health}", True, (255, 255, 255))
    surface.blit(health_text, (1230, 35))

    # Düşman ikonu ve sayısı
    surface.blit(enemy_icon, (1200, 60))
    enemies_text = font.render(f"{enemy_manager.get_enemy_count()}", True, (255, 255, 255))
    surface.blit(enemies_text, (1230, 60))

    # Ulti sayacı ve READY
    surface.blit(ultimate_icon, (1200, 85))
    icon_rect = ultimate_icon.get_rect(topleft=(1200, 85))
    if player.ulti_ready:
        small_font = pygame.font.Font(None, 20)
        ulti_text = small_font.render("READY", True, (0, 255, 0))
        text_rect = ulti_text.get_rect()
        # Dikey olarak ikonun ortasına hizala
        y_pos = icon_rect.top + (icon_rect.height - text_rect.height) // 2
        surface.blit(ulti_text, (1230, y_pos))
    else:
        ulti_text = font.render(f"{player.ulti_counter}", True, (255, 255, 255))
        surface.blit(ulti_text, (1230, 85))