import pygame
from game import *

def main():
    pygame.init()

    screenSize = (1280, 720)
    mainScreen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Pac-Man V2")
    pygame.display.set_icon(pygame.image.load("Static/Sprites/Pacman/Pacman-Open-R.png"))
    frame_rate = pygame.time.Clock()
    
    game = Application()
    
    running = True
    while running:
        events = pygame.event.get()
        user_input = pygame.key.get_pressed()
        running = stopchecking()
        mainScreen.fill((18, 18, 18))
        frame_rate.tick(60)
        game.updating(user_input, events)
        mainScreen.blit(game.screen, (0, 0))
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
