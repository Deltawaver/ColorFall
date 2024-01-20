import random
import pygame

PLAYER = pygame.sprite.Group()
PLATFORMS = pygame.sprite.Group()
FPS = 60

#UNSTABLE - баг при нажатии на QUIT (программа закрывается но выдает ошибку)
class StartMenu:

    def __init__(self, screen, width, height):
        
        self.screen = screen
        self.width = width
        self.height = height
        self.running = True

        # STABLE - настройка параметров окна
        self.screen.fill((0, 0, 0))
        
        # STABLE - создание заголовка
        self.level1_button = pygame.Rect(
            (width // 2 - 100, height // 2 - 40), (200, 50)
        )
        self.level2_button = pygame.Rect(
            (width // 2 - 100, height // 2 + 40), (200, 50)
        )
        self.level3_button = pygame.Rect(
            (width // 2 - 100, height // 2 + 120), (200, 50)
        )
        self.quit_button = pygame.Rect(
            (width // 2 - 100, height // 2 + 200), (200, 50)
        )
        pygame.font.init()
        self.level1_text = pygame.font.SysFont("Arial", 30, bold=True).render("Hero Red", True, (255, 0, 0))
        self.level2_text = pygame.font.SysFont("Arial", 30, bold=True).render("Hero Green", True, (0, 255, 0))
        self.level3_text = pygame.font.SysFont("Arial", 30, bold=True).render("Hero BLue", True, (0, 0, 255))
        self.quit_text = pygame.font.SysFont("Arial", 30, bold=True).render("Quit", True, (255, 255, 255))

    def draw(self):
        while self.running:
            #STABLE - создание кнопок и настройка их внешнего вида
            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), self.level1_button, 5)
            pygame.draw.rect(self.screen, (255, 255, 255), self.level2_button, 5)
            pygame.draw.rect(self.screen, (255, 255, 255), self.level3_button, 5)
            pygame.draw.rect(self.screen, (255, 255, 255), self.quit_button, 5)

            text_x = self.level1_button.x + self.level1_button.width / 2 - self.level1_text.get_width() / 2
            text_y = self.level1_button.y + self.level1_button.height / 2 - self.level1_text.get_height() / 2
            self.screen.blit(self.level1_text, (text_x, text_y))
            
            text_x = self.level2_button.x + self.level2_button.width / 2 - self.level2_text.get_width() / 2
            text_y = self.level2_button.y + self.level2_button.height / 2 - self.level2_text.get_height() / 2
            self.screen.blit(self.level2_text, (text_x, text_y))
            
            text_x = self.level3_button.x + self.level3_button.width / 2 - self.level3_text.get_width() / 2
            text_y = self.level3_button.y + self.level3_button.height / 2 - self.level3_text.get_height() / 2
            self.screen.blit(self.level3_text, (text_x, text_y))

            text_x = self.quit_button.x + self.quit_button.width / 2 - self.quit_text.get_width() / 2
            text_y = self.quit_button.y + self.quit_button.height / 2 - self.quit_text.get_height() / 2
            self.screen.blit(self.quit_text, (text_x, text_y))
            
            font = pygame.font.SysFont("Arial", 80, bold=True)
            text = font.render("ColorFall", True, (255, 0, 0))
            
            frame = pygame.Rect(
                (width // 2 - text.get_width() // 2 - 20, height // 2 - text.get_height() // 2 - 300),
                (text.get_width() + 40, text.get_height() + 40),
            )

            text_x = width // 2 - text.get_width() // 2 - 120
            text_y = height // 2 - text.get_height() // 2 - 250

            pygame.draw.rect(screen, (255, 255, 255), frame, 5)
            screen.blit(text, (frame.x + 20, frame.y + 20))

            #STABLE - получение ввода от игрока
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.level1_button.collidepoint(event.pos):
                        startgame()
                    if self.level2_button.collidepoint(event.pos):
                        startgame()
                    if self.level3_button.collidepoint(event.pos):
                        startgame()
                    elif self.quit_button.collidepoint(event.pos):
                        self.running = False
                        exit()
            pygame.display.flip()
            
    def run(self):
        while self.running:
            # Обработка событий
            for event in pygame.event.get():
                self.handle_event(event)
            # Отрисовка экрана
            self.draw()
            pygame.display.flip()
            
#STABLE - класс окна конца игры
class GameOver:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.running = True
        
        self.restart_button = pygame.Rect(
            (width // 2 - 100, height // 2 - 50), (200, 50)
        )
        self.quit_button = pygame.Rect(
            (width // 2 - 100, height // 2 + 50), (200, 50)
        )
        pygame.font.init()
        self.restart_text = pygame.font.SysFont("Arial", 30, bold=True).render("Revive", True, (255, 255, 255))
        self.quit_text = pygame.font.SysFont("Arial", 30, bold=True).render("Quit", True, (255, 255, 255))

    def draw(self):    
        while self.running:
            #STABLE - создание кнопок и настройка их внешнего вида
            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), self.restart_button, 5)
            pygame.draw.rect(self.screen, (255, 255, 255), self.quit_button, 5)

            text_x = self.restart_button.x + self.restart_button.width / 2 - self.restart_text.get_width() / 2
            text_y = self.restart_button.y + self.restart_button.height / 2 - self.restart_text.get_height() / 2
            self.screen.blit(self.restart_text, (text_x, text_y))

            text_x = self.quit_button.x + self.quit_button.width / 2 - self.quit_text.get_width() / 2
            text_y = self.quit_button.y + self.quit_button.height / 2 - self.quit_text.get_height() / 2
            self.screen.blit(self.quit_text, (text_x, text_y))
            
            font = pygame.font.SysFont("Arial", 70, bold=True)
            text = font.render("Into the Void", True, (255, 0, 0))
            
            frame = pygame.Rect(
                (width // 2 - text.get_width() // 2 - 20, height // 2 - text.get_height() // 2 - 300),
                (text.get_width() + 40, text.get_height() + 40),
            )

            text_x = width // 2 - text.get_width() // 2 - 120
            text_y = height // 2 - text.get_height() // 2 - 250

            pygame.draw.rect(screen, (255, 255, 255), frame, 5)
            screen.blit(text, (frame.x + 20, frame.y + 20))

            #STABLE - получение ввода от игрока
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_button.collidepoint(event.pos):
                        #рестарт
                        self.running = False
                        self.restart()
                    elif self.quit_button.collidepoint(event.pos):
                        #выход
                        start_menu = StartMenu(screen, width, height)
                        start_menu.run()
            pygame.display.flip()
            
    #STABLE - перезапуск игры        
    def restart(self):
        self.screen.fill((0, 0, 0))
        player.restart()
        PLATFORMS.empty()
        platforms = []
        for _ in range(random.randint(5, 10)):
            platform = Platform(self.screen)
            platforms.append(platform)

#STABLE - добавлена функция для сброса всех переменных при рестарте
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

    # сброс скорости
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
        if self.rect.y > 900:
            self.vx = 0
            self.moving_left = False
            self.moving_right = False
            
    # STABLE - сброс всех переменных
    def restart(self):
        player.rect.x = 240
        player.rect.y = 10
        self.vx = 0
        self.vy = 0


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
    
    def restart(self):
        # Устанавливаем позицию платформы за пределами экрана
        self.rect.x = -1000
        self.rect.y = -1000

#STABLE - функция отвечающая за саму игру возможно требуется переработка под уровневую систему
def startgame():
    global moving_left
    global moving_right
    moving_left = False
    moving_right = False
    
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
                pygame.quit()

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
        
    moving_right = False
    moving_left = False
    pygame.quit()
    
if __name__ == '__main__':
    # STABLE - установка пресетов
    pygame.init()
    width = 480
    height = 920
    screen = pygame.display.set_mode((width, height))
    screen.fill((0, 0, 0))
    player = Player(screen)
    moving_left = False
    moving_right = False
    main_menu = StartMenu(screen, width, height)
    main_menu.draw()














'''
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
                pygame.quit()

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
'''