import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE_SCALE

class Background:
    def __init__(self):
        # Arka plan görselini yükle
        self.image = pygame.image.load("assets/Rifle_Stage_Assets/images/map_TEST.png").convert()
        self.rect = self.image.get_rect()
        
        # Blokları tutacak grup
        self.blocks = pygame.sprite.Group()
        
        # Başlangıç bloklarını oluştur
        self.create_initial_blocks()
    
    def create_initial_blocks(self):
        """Başlangıç bloklarını oluşturur"""
        from objects import Block1, Block2, Stump, Tree1, Rock1, Rock2, Rock3
        
        # Kullanıcının eklediği blokların konumları
        block_positions = [
            # Block1'ler
            (101, 164), (620, 158), (441, 510), (508, 514), (163, 398),
            (871, 327), (462, 91),
            # Block2'ler
            (68, 158), (330, 182), (332, 215), (335, 248), (660, 124),
            (695, 128), (496, 475), (498, 443), (129, 395), (203, 442),
            (849, 368), (653, 342),
            # Rock1'ler
            (137, 192), (265, 370), (312, 225), (487, 278), (555, 180),
            (698, 312), (812, 195), (900, 410), (760, 480), (210, 520),
            # Rock2'ler
            (180, 145), (390, 210), (470, 260), (610, 230), (720, 320),
            (950, 370), (230, 430), (510, 490), (670, 530), (830, 570),
            # Rock3'ler
            (155, 260), (340, 295), (520, 340), (790, 370), (870, 420),
            (195, 470), (410, 540), (430, 495), (600, 570), (765, 610),
            # Stump'lar
            (81, 204), (600, 118), (670, 460), (418, 454), (143, 348),
            # Tree1'ler
            (101, 164), (245, 287), (567, 423), (789, 156), (432, 589),
            (678, 234)
        ]
        
        # Block1'leri ekle
        for x, y in block_positions[:7]:  # 0-7 arası konumlar Block1 için
            block = Block1(x, y)
            self.blocks.add(block)
        
        # Block2'leri ekle
        for x, y in block_positions[7:19]:  # 7-19 arası konumlar Block2 için
            block = Block2(x, y)
            self.blocks.add(block)

        # Rock1'leri ekle
        for x, y in block_positions[19:29]:  # 19-29 arası konumlar Rock1 için
            block = Rock1(x, y)
            self.blocks.add(block)

        # Rock2'leri ekle
        for x, y in block_positions[29:39]:  # 29-39 arası konumlar Rock2 için
            block = Rock2(x, y)
            self.blocks.add(block)

        # Rock3'leri ekle
        for x, y in block_positions[39:49]:  # 39-49 arası konumlar Rock3 için
            block = Rock3(x, y)
            self.blocks.add(block)

        # Stump'ları ekle
        for x, y in block_positions[49:54]:  # 49-54 arası konumlar Stump için
            block = Stump(x, y)
            self.blocks.add(block)
        
        # Tree1'leri ekle
        for x, y in block_positions[54:60]:  # 54-55 arası konumlar Tree1 için
            block = Tree1(x, y)
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