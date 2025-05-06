import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        img_original = pygame.image.load("assets/Rifle_Stage_Assets/sprites/soldier/rifle/soldier-rifle.png").convert_alpha()
        self.img_right = pygame.transform.scale(img_original, (img_original.get_width() * 2, img_original.get_height() * 2))
        self.img_left = pygame.transform.flip(self.img_right, True, False)
        self.image = self.img_right
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.facing_right = True

    def update(self, keys, screen_width, screen_height):
        if keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.x -= self.speed
            self.image = self.img_left
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            if self.rect.right < screen_width:
                self.rect.x += self.speed
            self.image = self.img_right
            self.facing_right = True

        if keys[pygame.K_UP]:
            if self.rect.top > 0:
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            if self.rect.bottom < screen_height:
                self.rect.y += self.speed

    def draw(self, surface):
        # Sola bakarken hizalamak için x pozisyonunu ayarla
        if not self.facing_right:
            surface.blit(self.image, (self.rect.x - 132, self.rect.y))
        else:
            surface.blit(self.image, self.rect.topleft)