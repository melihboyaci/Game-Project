import pygame
from utils.planet import Planet
from utils.animation import load_sprite_sheet, AnimatedSprite

class Earth(Planet):
    def __init__(self, image_path, size, position, scale):
        super().__init__(image_path, size, position, scale)
        self.health = 100
        self.alive = True
        
        self.explosion_frames = load_sprite_sheet("assets/Space_Stage_Assets/sprites/explosion/earth_explosion.png", 48, 48)
        self.explosion_sprite = AnimatedSprite(self.explosion_frames, position, frame_delay=150)
        self.explosion_time = 0
        self.explosion_duration = 1200
        self.exploding = False
        self.destroyed = False
        
    def draw(self, surface, camera_offset):
        if self.destroyed:
            return
        if self.exploding:
            explosion_img = self.explosion_sprite.image.copy()
            new_size = (int(self.size[0] * (self.scale * 0.8)), int(self.size[1] * (self.scale * 0.8)))
            explosion_img = pygame.transform.scale(explosion_img, new_size)
            surface.blit(explosion_img, (self.position[0] - camera_offset[0], self.position[1] - camera_offset[1]))
            sound = pygame.mixer.Sound("assets/Space_Stage_Assets/sounds/bigexplosion.flac")
            sound.set_volume(1.8)
            sound.play()
            return
        if self.health > 0:            
            super().draw(surface, camera_offset)

    def update(self):
        if self.health <= 0 and not self.exploding and not self.destroyed:
            self.exploding = True
            self.explosion_time = pygame.time.get_ticks()
            self.alive = False  
            self.sprite.image = pygame.Surface((0, 0))              
        if self.exploding:    
            self.explosion_sprite.pos = tuple(self.position)
            self.explosion_sprite.update()
            if pygame.time.get_ticks() - self.explosion_time > self.explosion_duration:
                self.exploding = False
                self.destroyed = True
            return
        if not self.destroyed:
            super().update()

    def get_rect(self):
        if self.destroyed:
            return pygame.Rect(0, 0, 0, 0)
        return super().get_rect()