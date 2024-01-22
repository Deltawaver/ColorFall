from config import *
from menu import StartMenu

if __name__ == '__main__':
    # STABLE - установка пресетов
    pygame.init()
    width = 480
    height = 920
    screen = pygame.display.set_mode((width, height))
    screen.fill((0, 0, 0))

    main_menu = StartMenu(screen, width, height)
    main_menu.draw()
