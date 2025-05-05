import pygame

class Bullet:
    def __init__(self, position, speed=10, image_path="assets/Space_Stage_Assets/sprites/spaceship/bullet.png"):
        self.position = list(position)
        self.speed = speed
        self.image = pygame.image.load(image_path).convert_alpha()
        self.size = self.image.get_size()


    def update(self):
        self.position[1] -= self.speed
    def draw(self, surface):
        surface.blit(self.image, self.position)
    def get_rect(self):
        return pygame.Rect(self.position, self.size)