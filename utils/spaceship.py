import pygame
from utils.animation import AnimatedSprite, load_sprite_sheet

class Spaceship:
    def __init__(self, image_path, size, position, speed, engine_path=None, engine_size=None):
        self.frames = load_sprite_sheet(image_path, *size)
        self.sprite = AnimatedSprite(self.frames, position, frame_delay=10000)
        self.size = size
        self.position = list(position)
        self.speed = speed
        self.direction = "right"  # "right" veya "left"

        # Motor efekti için
        if engine_path and engine_size:
            self.engine_image = pygame.image.load(engine_path).convert_alpha()
            self.engine_image = pygame.transform.scale(self.engine_image, engine_size)
            self.engine_size = engine_size
        else:
            self.engine_image = None

    def update(self, keys, screen_width, screen_height):
        if keys[pygame.K_LEFT]:
            self.position[0] -= self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.position[0] += self.speed
            self.direction = "right"
        if keys[pygame.K_UP]:
            self.position[1] -= self.speed
        if keys[pygame.K_DOWN]:
            self.position[1] += self.speed

        # Ekranın dışına çıkmaması için sınırları kontrol et
        self.position[0] = max(0, min(self.position[0], screen_width - self.size[0]))
        self.position[1] = max(0, min(self.position[1], screen_height - self.size[1]))
        self.sprite.pos = tuple(self.position)
        self.sprite.update()

    def draw(self, screen):
        # Yöne göre sprite'ı flip et
        image = self.sprite.image
        if self.direction == "left":
            image = pygame.transform.flip(image, True, False)
        screen.blit(image, self.sprite.pos)

        # Motor efekti varsa önce onu çiz
        if self.engine_image:
            # Motorun pozisyonunu geminin arkasına göre ayarla
            if self.direction == "right":
                engine_pos = (self.sprite.pos[0] - self.engine_size[0] + 10, self.sprite.pos[1] + self.size[1] // 2 - self.engine_size[1] // 2)
            else:
                engine_pos = (self.sprite.pos[0] + self.size[0] - 10, self.sprite.pos[1] + self.size[1] // 2 - self.engine_size[1] // 2)
            engine_img = self.engine_image
            if self.direction == "left":
                engine_img = pygame.transform.flip(self.engine_image, True, False)
            screen.blit(engine_img, engine_pos)

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])