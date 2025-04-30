import pygame
import sys

# Pygame'i başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Animasyonlu Arkaplan")

# FPS kontrolü
clock = pygame.time.Clock()
FPS = 30

# Arkaplan frame dosya şablonu ve sayısı
BG_FRAME_COUNT = 10  # Toplam frame sayısı (0'dan başlar, 11 frame için 0-10 arası)
BG_FRAME_PATH = "assets/city 4/{}.png"  # Örnek: bg_0.png, bg_1.png, ... bg_7.png

# Tek tek PNG frame'leri yükle
bg_frames = []
for i in range(BG_FRAME_COUNT):
    path = BG_FRAME_PATH.format(i+1)
    frame = pygame.image.load(path).convert_alpha()
    # Eğer frame boyutu ekranla uyumlu değilse, ölçekle
    if frame.get_size() != (WIDTH, HEIGHT):
        frame = pygame.transform.scale(frame, (WIDTH, HEIGHT))
    bg_frames.append(frame)

# Animasyon kontrol değişkeni ve hızı
bg_index = 0.0
BG_SPEED = 0.1   # arkaplan animasyon hızı

# Oyun döngüsü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Arkaplan frame index'ini güncelle
    bg_index = (bg_index + BG_SPEED) % BG_FRAME_COUNT

    # O anki arkaplan frame'ini çiz
    bg_frame = bg_frames[int(bg_index)]
    screen.blit(bg_frame, (0, 0))

    # Ekranı güncelle
    pygame.display.flip()

    # FPS sınırı
    clock.tick(FPS)

# Pygame'i kapat
pygame.quit()
sys.exit()
