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
    
    def draw(self, surface):
        self.sprite.draw(surface)