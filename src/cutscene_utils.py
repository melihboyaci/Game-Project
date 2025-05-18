import pygame
import time

def play_cutscene(screen, image_path, music_path=None, duration=3, subtitle=None, title=None):
    """
    Ekranda bir cutscene (görsel) ve opsiyonel olarak müzik ve altyazı gösterir.
    :param screen: pygame ekranı
    :param image_path: Gösterilecek görselin yolu
    :param music_path: Çalınacak müzik dosyasının yolu (isteğe bağlı)
    :param duration: Cutscene süresi (saniye)
    :param subtitle: Altyazı metni (isteğe bağlı)
    """
    # Müzik çal
    if music_path:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()
    
    # Görseli yükle ve ekrana ortala
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, screen.get_size())
    screen.blit(image, (0, 0))

    if title:
        font = pygame.font.Font(None, 50)
        title_surface = font.render(title, True, (255, 255, 255))
        x = screen.get_width() // 6 - title_surface.get_width() // 2 - 20
        y = 40
        # Hafif siyah gölge
        shadow = font.render(title, True, (0,0,0))
        screen.blit(shadow, (x+2, y+2))
        screen.blit(title_surface, (x, y))


    # Altyazı varsa ekrana yaz
    if subtitle:
        font = pygame.font.Font(None, 36)
        lines = subtitle.split('\n')
        total_height = len(lines) * 40
        y_start = screen.get_height() - 100 - total_height // 2
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (255, 255, 255))
            x = screen.get_width() // 2 - text_surface.get_width() // 2
            y = y_start + i * 40
            # Hafif siyah gölge
            shadow = font.render(line, True, (0,0,0))
            screen.blit(shadow, (x+2, y+2))
            screen.blit(text_surface, (x, y))
    pygame.display.flip()

    # Belirtilen süre boyunca cutscene göster
    start_time = time.time()
    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys; sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            break
        pygame.time.delay(100) 