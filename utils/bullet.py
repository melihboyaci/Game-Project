import pygame
from utils.animation import AnimatedSprite, load_sprite_sheet

class Bullet:
    def __init__(self, image_path, size, position, speed=5):
        self.position = list(position)
        self.size = size
        self.speed = speed
        self.frames = load_sprite_sheet(image_path, *size)
        self.sprite = AnimatedSprite(self.frames, position, frame_delay=100)


    def update(self):
        self.position[1] -= self.speed
    def draw(self, surface):
        width, height = int(self.size[0]), int(self.size[1])
        image = self.sprite.image.copy()
        pos = (self.position[0] - width // 2, self.position[1] - height // 2)
        surface.blit(image, pos)

    def get_rect(self):
        return pygame.Rect(self.position, self.size)