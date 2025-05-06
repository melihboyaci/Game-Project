import pygame
from utils.animation import AnimatedSprite, load_sprite_sheet
import random
class Planet:
    def __init__(self, image_path, size, position):
        self.frames = load_sprite_sheet(image_path, *size)
        self.sprite = AnimatedSprite(self.frames, position)
        self.size = size
        self.position = position

    def update(self):
        self.sprite.update()
    
    def draw(self, surface, camera_offset):
        surface_pos = (self.position[0] - camera_offset[0], self.position[1] - camera_offset[1])
        self.sprite.draw(surface, surface_pos)
    
    def get_rect(self):
        return pygame.Rect(self.position, self.size)