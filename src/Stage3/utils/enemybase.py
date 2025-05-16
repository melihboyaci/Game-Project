import pygame
from ..utils.animation import AnimatedSprite, load_sprite_sheet

class EnemyBase:
    def __init__(self, image_path, size, position, engine_path=None, engine_size=None,
                 weapon_path=None, weapon_size=None, shield_path=None, shield_size=None):
        """Düşman üssü için bir sınıf."""
        self.frames = load_sprite_sheet(image_path, *size)
        self.sprite = AnimatedSprite(self.frames, position, frame_delay=100)
        self.size = size
        self.position = list(position)
        engine_path = "assets/Space_Stage_Assets/sprites/enemybase/engine.png"
        engine_size = (128, 128)
        weapon_path = "assets/Space_Stage_Assets/sprites/enemybase/weapons.png"
        weapon_size = (128, 128)
        shield_path = "assets/Space_Stage_Assets/sprites/enemybase/shield.png"
        shield_size = (128, 128)
        self.map_width = 2000
        self.map_height = 2000
        self.scale = 4
        self.health = 10
        self.alive = True
        
        # Engine animasyonu
        if engine_path and engine_size:
            frames = load_sprite_sheet(engine_path, *engine_size)
            self.engine_anim = AnimatedSprite(frames, position, frame_delay=90)
        else:
            self.engine_anim = None

        # Weapon animasyonu
        if weapon_path and weapon_size:
            frames = load_sprite_sheet(weapon_path, *weapon_size)
            self.weapon_anim = AnimatedSprite(frames, position, frame_delay=90)
        else:
            self.weapon_anim = None

        # Shield animasyonu
        if shield_path and shield_size:
            frames = load_sprite_sheet(shield_path, *shield_size)
            self.shield_anim = AnimatedSprite(frames, position, frame_delay=90)
        else:
            self.shield_anim = None

        # Destruction animasyonu
        self.destruction_frames = load_sprite_sheet("assets/Space_Stage_Assets/sprites/enemybase/destruction.png", 128, 128)
        self.destruction_sprite = AnimatedSprite(self.destruction_frames, position, frame_delay=100)
        self.destruction = False
        self.destruction_time = 0 
        self.destruction_duration = 1800

    def update(self):
        speed = 2
        self.position[0] -= speed
        if self.position[0] + self.size[0] * self.scale < 0:
            self.position[0] = self.map_width

        self.position[1] = max(0, min(self.position[1], self.map_height - self.size[1]))
        self.sprite.pos = tuple(self.position)
        self.sprite.update()
        if self.engine_anim:
            self.engine_anim.pos = tuple(self.position)
            self.engine_anim.update()
        if self.weapon_anim:
            self.weapon_anim.pos = tuple(self.position)
            self.weapon_anim.update()
        if self.shield_anim:
            self.shield_anim.pos = tuple(self.position)
            self.shield_anim.update()
        if self.destruction:
            self.destruction_sprite.pos = tuple(self.position)
            self.destruction_sprite.update()
            if pygame.time.get_ticks() - self.destruction_time > len(self.destruction_frames) * self.destruction_sprite.frame_delay:
                self.destruction = False
                self.alive = False

    def draw(self, surface, camera_offset):
        # düşman rectini göster
        #pygame.draw.rect(surface, (255,0,0), self.get_rect().move(-camera_offset[0], -camera_offset[1]), 2)
        surface_pos = (self.position[0] - camera_offset[0], self.position[1] - camera_offset[1])
        new_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
        
        if self.destruction:
            destruction_image = self.destruction_sprite.image.copy()
            destruction_image = pygame.transform.scale(destruction_image, new_size)
            destruction_image = pygame.transform.rotate(destruction_image, 90)
            surface.blit(destruction_image, surface_pos)
            self.sprite.image = pygame.Surface((0, 0))
            self.engine_anim.image = pygame.Surface((0, 0))
            self.weapon_anim.image = pygame.Surface((0, 0))
            self.shield_anim.image = pygame.Surface((0, 0))

            return
        
        if not self.alive:
            return
        
        image = self.sprite.image.copy()        
        image = pygame.transform.scale(image, new_size)
        image = pygame.transform.rotate(image, 90)
        surface.blit(image, surface_pos)
        def draw_anim(anim):
            if anim:
                image = anim.image.copy()
                new_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
                image = pygame.transform.scale(image, new_size)
                image = pygame.transform.rotate(image, 90)
                surface.blit(image, surface_pos)

        draw_anim(self.engine_anim)
        draw_anim(self.weapon_anim)
        draw_anim(self.shield_anim)

    def take_damage(self, damage):
        # Hasar alındığında yapılacak işlemler
        self.health -= damage
        sound = pygame.mixer.Sound("assets/Space_Stage_Assets/sounds/hit1.mp3")
        sound.set_volume(0.8)
        sound.play()
        if self.health <= 0:
            self.destroy()
            self.alive = False

    def destroy(self):
        self.destruction = True
        self.destruction_time = pygame.time.get_ticks()

    def get_rect(self):
        x = self.position[0] + 30
        y = self.position[1] + 20
        width = int(self.size[0] * 3)
        height = int(self.size[1] * 3)
        return pygame.Rect(x, y, width, height)

    def get_healthbar_pos(self):
        # Base'in üst kısmının biraz altında, base ile beraber hareket eden bir nokta
        x = self.position[0]
        y = self.position[1] + 10  # üstten 10 piksel aşağıda
        return (x, y)