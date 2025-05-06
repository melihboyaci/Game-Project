import pygame
from utils.animation import AnimatedSprite, load_sprite_sheet
import random
class Planet:
    SCALE_WITHOUT_ALPHA = 1.5  # Scale value where alpha transparency is not applied

    def __init__(self, image_path, size, position, scale):
        self.frames = load_sprite_sheet(image_path, *size)
        self.sprite = AnimatedSprite(self.frames, position)
        self.size = size
        self.position = position
        self.scale = scale

    def update(self):
        self.sprite.update()
    
    def draw(self, surface, camera_offset):
        surface_pos = (self.position[0] - camera_offset[0], self.position[1] - camera_offset[1])
        image = self.sprite.image.copy()
        new_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
        image = pygame.transform.scale(image, new_size)
        if self.scale != self.SCALE_WITHOUT_ALPHA:
            image.set_alpha(130)
        surface.blit(image, surface_pos)
    
    def get_rect(self):
        scaled_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
        return pygame.Rect(self.position, scaled_size)