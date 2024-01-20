from menu import StartMenu
import pygame

PLAYER = pygame.sprite.Group()
PLATFORMS = pygame.sprite.Group()
FPS = 60





if __name__ == '__main__':
    # STABLE - установка пресетов
    pygame.init()
    width = 480
    height = 920
    screen = pygame.display.set_mode((width, height))
    screen.fill((0, 0, 0))

    main_menu = StartMenu(screen, width, height)
    main_menu.draw()