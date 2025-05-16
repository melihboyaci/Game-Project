def draw_ui(surface, player, enemy_manager, bullet_icon, hp_icon, enemy_icon, font):
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