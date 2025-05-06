import pygame
class AnimatedSprite:
    def __init__(self, frames, pos, frame_delay=60): #self: animasyonun kendisi, frames: kareler, pos: konum, frame_delay: her bir kare için bekleme süresi
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.pos = pos
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = frame_delay

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.last_update = now

    def draw(self, surface, pos):
        surface.blit(self.image, pos)

def load_sprite_sheet(path, frame_width, frame_height):
    """Spritesheet'i yükler ve her kareyi bir listeye ayırır."""
    sheet = pygame.image.load(path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()
        
    frames = []
    for i in range(sheet_width // frame_width):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
        
    return frames