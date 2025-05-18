import pygame

def main():
    pygame.init()
    pygame.font.init()
    from game_loop import start_game
    start_game()

if __name__ == "__main__":
    main()
