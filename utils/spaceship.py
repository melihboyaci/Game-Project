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
            frames = load_sprite_sheet(engine_path, *engine_size)
            self.engine_anim = AnimatedSprite(frames, position, frame_delay=90)
        else:
            self.engine_anim = None

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

        if self.engine_anim:
            self.engine_anim.update()



    def draw(self, screen):
        # Yöne göre sprite'ı flip et
        image = self.sprite.image
        if self.direction == "left":
            image = pygame.transform.flip(image, True, False)
        screen.blit(image, self.sprite.pos)
        
        if self.engine_anim:
            frame_width = self.engine_anim.frames[0].get_width()
            frame_height = self.engine_anim.frames[0].get_height()
            # Motoru geminin alt ortasına hizala
            engine_pos = (
                self.position[0] + self.size[0] // 2 - frame_width // 2,
                self.position[1] + self.size[1] - frame_height // 2
            )
            self.engine_anim.flipped = (self.direction == "left")
            self.engine_anim.pos = engine_pos
            self.engine_anim.draw(screen)


    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])