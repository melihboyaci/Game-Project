import pygame
def start_screen(screen, clock, WINDOW_WIDTH=1280, WINDOW_HEIGHT=720):
    
    pygame.mixer.music.load("assets/Space_Stage_Assets/sounds/2.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    backgrounds = []
    for i in range(1, 11):
        background = pygame.image.load(f"assets/Space_Stage_Assets/ui/start_background/{i}.png").convert_alpha()
        background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        backgrounds.append(background)

    
    font = pygame.font.Font("assets/Space_Stage_Assets/fonts/altroned.ttf", 50)
    title = render_text_with_shadow(font, "My Game", (255, 255, 255), (50,50,50), (6, 6))
    subtitle = render_text_with_stroke(font, "Press SPACE to Start", (255, 255, 255), (0, 0, 0), 6)

    # Geçiş süreleri
    alpha_values = [0] * len(backgrounds)
    current_idx = 0
    fade_duration = 100
    switch_time = 250
    last_switch_time = pygame.time.get_ticks()

    # Metinlerin gecikme süreleri
    title_delay = 1000
    subtitle_delay = 1500
    title_start_time = pygame.time.get_ticks() + title_delay
    subtitle_start_time = title_start_time + subtitle_delay

    # Subtitle görünürlük durumu
    subtitle_visible = True
    visible_time = 700
    last_time = pygame.time.get_ticks()


    waiting = True

    while waiting:
        now = pygame.time.get_ticks()

        # Alfa değerlerini güncelle
        dt = max(clock.get_time(), 1)
        if current_idx < len(backgrounds):
            alpha_values[current_idx] += 255 / (fade_duration / dt)
            if alpha_values[current_idx] >= 255:
                alpha_values[current_idx] = 255
                if now - last_switch_time > switch_time:
                    current_idx += 1
                    last_switch_time = now
        
        if now - visible_time > last_time:
            subtitle_visible = not subtitle_visible
            last_time = now

        # Görseller
        screen.fill((0, 0, 0))
        for i in range(len(backgrounds)):
            if alpha_values[i] > 0:
                background = backgrounds[i].copy()
                background.set_alpha(int(alpha_values[i]))
                screen.blit(background, (0, 0))

        # Metinler
        if now > title_start_time:
            screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 70))
        if now > subtitle_start_time and subtitle_visible:
            screen.blit(subtitle, (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, WINDOW_HEIGHT // 2 - subtitle.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.music.stop()
                waiting = False 

        clock.tick(60)

def render_text_with_stroke(font, text, text_color, stroke_color, stroke_width):
    # Metni kenarlık rengiyle farklı yönlere kaydırarak çizin
    base_surface = font.render(text, True, stroke_color)
    text_surface = font.render(text, True, text_color)
    width, height = text_surface.get_size()
    surface = pygame.Surface((width + stroke_width * 2, height + stroke_width * 2), pygame.SRCALPHA)

    # Kenarlık için metni farklı yönlere kaydırarak çizin
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx != 0 or dy != 0:  # Merkezdeki metni çizme
                surface.blit(base_surface, (dx + stroke_width, dy + stroke_width))

    # Asıl metni üstüne çizin
    surface.blit(text_surface, (stroke_width, stroke_width))
    return surface

def render_text_with_shadow(font, text, text_color, shadow_color, shadow_offset):
    # Gölgeyi oluştur
    shadow_surface = font.render(text, True, shadow_color)
    text_surface = font.render(text, True, text_color)
    width, height = text_surface.get_size()
    surface = pygame.Surface((width + shadow_offset[0], height + shadow_offset[1]), pygame.SRCALPHA)

    # Gölgeyi çizin
    surface.blit(shadow_surface, shadow_offset)

    # Asıl metni çizin
    surface.blit(text_surface, (0, 0))
    return surface

def draw_background(screen, layers, alpha=255):
    for layer in layers:
        image_path = layer.get("image_path")
        alpha = layer.get("alpha", 255)
        position = layer.get("position", (0, 0))

        # Görseli yükle ve ayarları uygula
        background = pygame.image.load(image_path).convert_alpha()
        background = pygame.transform.scale(background, (800, 600))
        background.set_alpha(alpha)
        screen.blit(background, position)

def draw_scrolling_bg(screen, bg_image, offset, speed):
    """
    screen      : pygame.Surface — hedef surface
    bg_image    : pygame.Surface — senin space arka planın
    offset      : dict — {'x': float, 'y': float}, güncellenen kaydırma ofseti
    speed       : dict — {'x': float, 'y': float}, piksel/frame kayma hızı
    """
    w, h = bg_image.get_size()

    # Ofset'u float olarak güncelle, sonra modulo ile döngüye al
    offset['x'] = (offset['x'] + speed['x'] * 3) % w
    offset['y'] = (offset['y'] + speed['y'] * 3) % h

    # Tam sayıya çevir (yarım piksel kaymaları önler)
    ox = int(offset['x'])
    oy = int(offset['y'])

    # 2x2 lef–top blokları çiz
    screen.blit(bg_image, ( -ox,   -oy   ))
    screen.blit(bg_image, ( w-ox,  -oy   ))
    screen.blit(bg_image, ( -ox,   h-oy  ))
    screen.blit(bg_image, ( w-ox,  h-oy  ))

def draw_earth_bar(screen, earth_bar):
    bar_width = 300
    bar_height = 20
    bar_x = (screen.get_width() - bar_width) // 2
    bar_y = 20
    earth_bar = earth_bar

    pygame.draw.rect(screen, (100, 100 ,100), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width * (earth_bar / 100), bar_height))

    font = pygame.font.Font(None, 24)
    text = render_text_with_stroke(font, f"Dünya: {earth_bar}%", (255, 255, 255), (0, 0, 0), 2)
    text_rect = text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
    screen.blit(text, text_rect)

def draw_health_bar(screen, health, max_health=15):

    health = max(0, min(int(health), max_health))
    bar_image = pygame.image.load(f"assets/Space_Stage_Assets/sprites/spaceship/health_bar/{health}.png").convert_alpha()
    bar_image = pygame.transform.scale(bar_image, (204, 61))
    bar_x = 20
    bar_y = screen.get_height() - bar_image.get_height() - 20
    screen.blit(bar_image, (bar_x, bar_y))

    font = pygame.font.Font(None, 32)
    text = render_text_with_stroke(font, "HP", (0, 255, 0), (0, 0, 0), 2)
    text_rect = text.get_rect(center=(bar_x + bar_image.get_width() // 2, bar_y - 7))
    screen.blit(text, text_rect)

def draw_base_health_bar(screen, base, camera, health, max_health=10):
    if not base.alive:
        return
    pos = base.get_healthbar_pos()
    bar_width = 300
    bar_height = 20
    health = max(0, min(int(health), max_health))
    bar_image = pygame.image.load(f"assets/Space_Stage_Assets/sprites/enemybase/health_bar/{health}.png").convert_alpha()
    bar_image = pygame.transform.scale(bar_image, (bar_width, bar_height))
    bar_x = pos[0] + 70
    bar_y = pos[1] + 50
    bar_x -= camera.pos[0]
    bar_y -= camera.pos[1]
    screen.blit(bar_image, (bar_x, bar_y))
