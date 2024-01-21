import random

import pygame

PLAYER = pygame.sprite.Group()
PLATFORMS = pygame.sprite.Group()
FPS = 60


# STABLE - добавлена функция для сброса всех переменных при рестарте
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
    def move_x(self, direction: int):
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

        collisions = pygame.sprite.spritecollide(self, PLATFORMS, False)  # проверяем, есть ли столкновение

        if collisions:
            print(collisions[0].rect, self.rect)
            platform = collisions[0].rect
            if self.rect.top < platform.top:
                self.rect.y = platform.y - self.rect.height + collisions[
                    0].vy  # чтобы избежать застревания, перемещаем игрока на верх платформы
            else:
                self.rect.top = platform.top + platform.height
            self.vy = -self.vy * 0.85
        else:
            self.vy += self.ay
            self.rect = self.rect.move(0, self.vy)

    # STABLE - сброс всех переменных
    def restart(self):
        self.rect.x = 240
        self.rect.y = 10

        self.vx = 0
        self.vy = 0


# STABLE - класс платформ(необходимо доработать их перемещение)
class Platform(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
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

#STABLE - счётчик
class ScoreCount:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.score = 0
        self.time = 0

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def update(self):
        self.score += 2 
        
    def clear(self):
        self.score = 0

    def draw(self):
        self.update()

        # Get the score text
        score_text = str(self.score)

        font = pygame.font.SysFont("Arial", 30, bold = True)
        text_size = font.size(score_text)

        text_x = 480 - text_size[0] - 20
        text_y = text_size[1] + 10

        score_text_rendered = font.render(score_text, True, (255, 255, 255))
        self.screen.blit(score_text_rendered, (text_x, text_y))

    def check_collision(self, player: Player):
        collisions = pygame.sprite.spritecollide(player, PLATFORMS, False)
        if collisions:
            self.score += 10