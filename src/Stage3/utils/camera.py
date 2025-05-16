import pygame
class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height
        self.pos = [0, 0]

    def update(self, target_pos, target_size):
        self.pos[0] = target_pos[0] + target_size[0] // 1 - self.width // 2
        self.pos[1] = target_pos[1] + target_size[1] // 1 - self.height // 2
        self.pos[0] = max(0, min(self.pos[0], self.map_width - self.width))
        self.pos[1] = max(0, min(self.pos[1], self.map_height - self.height))