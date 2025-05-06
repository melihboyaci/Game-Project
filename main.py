import pygame

from utils.views import start_screen
from game_loop import game_loop


screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

def main():
    pygame.init()
    start_screen(screen, clock)

    game = game_loop(screen, clock)
    
    game.run() 

    pygame.quit()


if __name__ == "__main__": #tanım: 
    main()
 