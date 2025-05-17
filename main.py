import sys
import pygame

from src.Space_Stage.utils.views import start_screen
from src.Space_Stage.stage3 import game_loop


screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

def main():
    pygame.init()
    """start_screen(screen, clock)"""
    
    while True:
        clock.tick(60)
        game = game_loop(screen, clock)
        result = game.run()
        if result != "restart":
            break 
    pygame.quit()
    sys.exit()


if __name__ == "__main__": 
    main()
     