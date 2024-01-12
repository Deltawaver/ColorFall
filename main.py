import random
import pygame

PLAYER = pygame.sprite.Group()
PLATFORMS = pygame.sprite.Group()
FPS = 60

import pygame

class GameOver:

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.running = True
        # Создаем кнопки
        self.restart_button = pygame.Rect(
            (width // 2 - 100, height // 2 - 50), (200, 50)
        )
        self.quit_button = pygame.Rect(
            (width // 2 - 100, height // 2 + 50), (200, 50)
        )

        # Задаем текст на кнопках
        pygame.font.init()
        self.restart_text = pygame.font.SysFont("Arial", 30).render("Restart", True, (255, 255, 255))
        self.quit_text = pygame.font.SysFont("Arial", 30).render("Quit", True, (255, 255, 255))

    def draw(self):
        while self.running:
            # Fill the screen with black
            self.screen.fill((0, 0, 0))

            # Draw buttons
            pygame.draw.rect(self.screen, (0, 0, 0), self.restart_button)
            pygame.draw.rect(self.screen, (0, 0, 0), self.quit_button)

            # Draw text on buttons
            self.screen.blit(self.restart_text, (self.restart_button.x + 50, self.restart_button.y + 20))
            self.screen.blit(self.quit_text, (self.quit_button.x + 50, self.quit_button.y + 20))

            # Get user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Check for button presses
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_button.collidepoint(event.pos):
                        # Restart the game
                        self.running = False
                    elif self.quit_button.collidepoint(event.pos):
                        # Завершаем игру
                        self.running = False
                        exit()

            # Update the display
            pygame.display.flip()



class Player(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        super().__init__(PLAYER)
        # STABLE - настройка параметров игрока
        self.screen = screen
        self.radius = 25

        self.base_vx = 4  # базовая скорость игрока по оси x(необходима для сброса после ускорения)
        self.vx = self.base_vx  # скорость игрока по оси x
        self.ax = 0.1  # ускорение игрока по оси x

        self.vy = 2  # скорость игрока по оси y
        self.ay = 0.4  # ускорение игрока по оси y

        # STABLE - спавн игрока
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (self.radius, self.radius), self.radius)

        self.rect = pygame.Rect(self.screen.get_rect().width // 2 - 25, 10, 2 * self.radius, 2 * self.radius)

    # STABLE - передвижение игрока по оси x
    def move_x(self, direction : int):
        self.vx += self.ax

        self.rect = self.rect.move(self.vx * direction, 0)

    def reset_vx(self):
        self.vx = self.base_vx

    # STABLE - передвижение игрока по оси y
    def update(self):
        # STABLE ON FIRST TIME - исключение возможности вылета игрока за поле. временно по той причине, что тело по непонятной мне причине тпшит примерно на 10 пикселей от краев, позже буду фиксить
        if self.rect.x < 10:
            self.rect.x = 10
        elif self.rect.x > self.screen.get_rect().width - 60:
            self.rect.x = self.screen.get_rect().width - 60
            
        collisions = pygame.sprite.spritecollide(self, PLATFORMS, False) # проверяем, есть ли столкновение
        if collisions:
            self.rect.y = collisions[0].rect.y - self.rect.height + collisions[0].vy # чтобы избежать застревания, перемещаем игрока на верх платформы
            self.vy = -self.vy * 0.85 + collisions[0].vy
        else:
            self.vy += self.ay
            self.rect = self.rect.move(0, self.vy)
        # STABLE - окончание игры при падении игрока вниз. в будущем отсюда реализуем вызов окна окончания игры
        if self.rect.y > 920 or self.rect.y < -50:
            # Создаем окно Game Over
            game_over = GameOver(self.screen, self.screen.get_rect().width, self.screen.get_rect().height)

            # Показываем окно Game Over
            game_over.draw()


# STABLE - класс платформ(необходимо доработать их перемещение)
class Platform(pygame.sprite.Sprite):
    def __init__(self, screen : pygame.Surface):
        super().__init__(PLATFORMS)

        self.screen = screen
        self.vy = -1
        self.ay = -0.005


        obj_width = random.randint(50, 200)
        obj_height = 20

        self.image = pygame.Surface((obj_width, obj_height))
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        obj_x = random.randint(10, 201)
        self.rect.x = obj_x
        obj_y = random.randint(25, 895)
        self.rect.y = obj_y


    def update(self):
        if self.vy <= -4:
            self.ay = 0

        self.vy += self.ay
        self.rect = self.rect.move(0, self.vy)


if __name__ == '__main__':
    # STABLE - установка пресетов
    pygame.init()
    width = 480
    height = 920
    screen = pygame.display.set_mode((width, height))
    screen.fill((0, 0, 0))
    moving_left = False
    moving_right = False

    # UNSTABLE - создание объектов спрайтов(необходимо создать цикл размещения платформ)

    player = Player(screen)
    platform_count = random.randint(5, 10)
    for _ in range(platform_count):
        platform = Platform(screen)
        

    pygame.display.flip()

    running = True
    clock = pygame.time.Clock()

    # STABLE - основной цикл
    while running:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False

            # нажатие клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_RIGHT:
                    moving_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.reset_vx()
                    moving_left = False
                if event.key == pygame.K_RIGHT:
                    player.reset_vx()
                    moving_right = False

        # перемещение по оси x
        if moving_left:
            player.move_x(-1)
        if moving_right:
            player.move_x(1)

        # отрисовка всего
        screen.fill((0, 0, 0))
        PLAYER.draw(screen)
        PLATFORMS.draw(screen)

        # обновление спрайтов
        PLAYER.update()
        PLATFORMS.update()

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()
