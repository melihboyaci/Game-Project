import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE_SCALE

class Background:
    def __init__(self):
        # Arka plan görselini yükle
        self.image = pygame.image.load("assets/Rifle_Stage_Assets/images/map4.png").convert()
        self.rect = self.image.get_rect()
        
        # Blokları tutacak grup
        self.blocks = pygame.sprite.Group()
        
        # Başlangıç bloklarını oluştur
        self.create_initial_blocks()
    
    def create_initial_blocks(self):
        """Başlangıç bloklarını oluşturur"""
        from objects import Block1, Block2
        
        # Kullanıcının eklediği blokların konumları
        block_positions = [
            # Block1'ler
            (101, 164), (620, 158), (441, 510), (508, 514), (163, 398),
            (871, 327), (462, 91),
            
            # Block2'ler
            (68, 158), (330, 182), (332, 215), (335, 248), (660, 124),
            (695, 128), (496, 475), (498, 443), (129, 395), (203, 442),
            (849, 368), (653, 342)
        ]
        
        # Block1'leri ekle
        for x, y in block_positions[:7]:  # İlk 8 konum Block1 için
            block = Block1(x, y)
            self.blocks.add(block)
        
        # Block2'leri ekle
        for x, y in block_positions[7:]:  # Kalan konumlar Block2 için
            block = Block2(x, y)
            self.blocks.add(block)
    
    def draw(self, surface):
        """Arka planı ve blokları çizer"""
        # Arka planı çiz
        surface.blit(self.image, (0, 0))
        # Blokları çiz
        self.blocks.draw(surface)
    
    def get_blocks(self):
        """Blok grubunu döndürür"""
        return self.blocks