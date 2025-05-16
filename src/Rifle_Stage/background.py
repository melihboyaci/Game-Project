import pygame

class Background:
    def __init__(self):
        # Arka plan görselini yükle
        self.image = pygame.image.load("assets/Rifle_Stage_Assets/images/newMap_NoStones.png").convert()
        self.rect = self.image.get_rect()
        
        # Blokları tutacak grup
        self.blocks = pygame.sprite.Group()
        
        # Başlangıç bloklarını oluştur
        self.create_initial_blocks()
    
    def create_initial_blocks(self):
        """Başlangıç bloklarını oluşturur"""
        from objects import (
            Block1, Block2, Stump, Tree1, Rock1, Rock2, 
            Rock3, Tower, Ruin1, Ruin2, Tower2, Ruin3
        )

        # Block1'leri ekle (x'e göre sıralı)
        for x, y in [
            (101, 164), (163, 398), (441, 510), (462, 91), (508, 514), (620, 158), (871, 327)
        ]:
            block = Block1(x, y)
            self.blocks.add(block)

        # Block2'leri ekle (x'e göre sıralı)
        for x, y in [
            (68, 158), (129, 395), (332, 215), (335, 248),
            (498, 443), (660, 124), (695, 128), (849, 368), (1100, 550)
        ]:
            block = Block2(x, y)
            self.blocks.add(block)

        # Rock1'leri ekle (x'e göre sıralı)
        for x, y in [
            (137, 192), (210, 520), (265, 370), (312, 225), (487, 278),
            (555, 180), (698, 312), (760, 480), (812, 195), (900, 410)
        ]:
            block = Rock1(x, y)
            self.blocks.add(block)

        # Rock2'leri ekle (x'e göre sıralı)
        for x, y in [
            (180, 145), (230, 430), (390, 210), (470, 260), (510, 490),
            (610, 230), (670, 530), (720, 320), (830, 570), (950, 370)
        ]:
            block = Rock2(x, y)
            self.blocks.add(block)

        # Rock3'leri ekle (x'e göre sıralı)
        for x, y in [
            (155, 260), (195, 470), (340, 295), (410, 540), (430, 495),
            (520, 340), (600, 570), (765, 610), (790, 370), (870, 420)
        ]:
            block = Rock3(x, y)
            self.blocks.add(block)

        # Stump'ları ekle (x'e göre sıralı)
        for x, y in [
            (81, 204), (143, 348), (418, 454)
        ]:
            block = Stump(x, y)
            self.blocks.add(block)

        # Tree1'leri ekle (x'e göre sıralı)
        for x, y in [
            (245, 287), (432, 589), (567, 423), (678, 234)
        ]:
            block = Tree1(x, y)
            self.blocks.add(block)

        # Tower'ları ekle
        for x, y in [
            (800, 545), (1100, 300)
        ]:
            block = Tower(x, y)
            self.blocks.add(block)

        # Ruin1'leri ekle
        for x, y in [
            (270, 55), (1000, 205)
        ]:
            block = Ruin1(x, y)
            self.blocks.add(block)

        # Ruin2'leri ekle
        for x, y in [
            (300, 50), (1030, 200)
        ]:
            block = Ruin2(x, y)
            self.blocks.add(block)

        # Tower2'leri ekle
        for x, y in [
            (100, 500),
        ]:
            block = Tower2(x, y)
            self.blocks.add(block)

        # Ruin3'leri ekle (x'e göre sıralı)
        for x, y in [
            
        ]:
            block = Ruin3(x, y)
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