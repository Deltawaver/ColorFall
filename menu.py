import os
import sqlite3
import sys

from objects import *


def load_image(name):
    fullname = os.path.join('', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# STABLE - создание меню
class StartMenu:
    def __init__(self, screen, width, height):

        self.screen = screen
        self.width = width
        self.height = height
        self.running = True

        # STABLE - настройка параметров окна и очистка поля
        self.screen.fill((0, 0, 0))
        PLAYER.empty()
        PLATFORMS.empty()

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
        AnimatedSprite(load_image("logo.png"), 3, 1, 50, 50)
        pygame.font.init()
        self.level1_text = pygame.font.SysFont("Arial", 30, bold=True).render("Level Red", True, (255, 0, 0))
        self.level2_text = pygame.font.SysFont("Arial", 30, bold=True).render("Level Green", True, (0, 255, 0))
        self.level3_text = pygame.font.SysFont("Arial", 30, bold=True).render("Level Blue", True, (0, 0, 255))
        self.quit_text = pygame.font.SysFont("Arial", 30, bold=True).render("Quit", True, (255, 255, 255))

    def draw(self):
        clock = pygame.time.Clock()
        count_animation = 0
        while self.running:
            # STABLE - создание кнопок и настройка их внешнего вида
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

            # STABLE - обновляем анимацию
            if count_animation % 45 == 0:
                LOGO.update()
            LOGO.draw(self.screen)

            # STABLE - получение ввода от игрока
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.level1_button.collidepoint(event.pos):
                        startgame(self.screen, 1)
                    if self.level2_button.collidepoint(event.pos):
                        startgame(self.screen, 2)
                    if self.level3_button.collidepoint(event.pos):
                        startgame(self.screen, 3)
                    elif self.quit_button.collidepoint(event.pos):
                        self.running = False
                        exit()
            clock.tick(FPS)
            count_animation += 1
            pygame.display.flip()

    def run(self):
        while self.running:
            # Отрисовка экрана
            self.draw()

            pygame.display.flip()


def generate_platforms(screen, vy, vx):
    obj_y = 150
    for _ in range(10):
        obj_x = random.randint(10, 280)
        Platform(screen, obj_y, obj_x, vy, vx)
        obj_y += random.randint(100, 150)


def startgame(screen, mode=1):
    moving_left = False
    moving_right = False

    player = Player(screen, mode)

    pygame.display.flip()

    score_count = ScoreCount(screen)

    running = True
    clock = pygame.time.Clock()

    match mode:
        case 1:  # hero red
            generate_platforms(screen, -1, 0)
        case 2:  # hero green
            generate_platforms(screen, -2, random.choice([1, -1]))
        case 3:  # hero blue
            generate_platforms(screen, -3, random.choice([1, -1, 2, -2]))

    # STABLE - основной цикл
    while running:
        # STABLE - окончание игры при падении игрока вниз. в будущем отсюда реализуем вызов окна окончания игры
        if player.rect.y > 920 or player.rect.y < -50:
            # Создаем окно Game Over
            your_score = score_count.get_score()
            game_over = GameOver(player.screen, player.screen.get_rect().width, player.screen.get_rect().height,
                                 your_score, mode)

            moving_left = False
            moving_right = False

            # Показываем окно Game Over
            game_over.draw()

            score_count.clear()
            screen.fill((0, 0, 0))
            PLAYER.empty()
            PLATFORMS.empty()
            player = Player(screen, mode)

            # STABLE - выбираем уровень игрока
            match mode:
                case 1:  # hero red
                    generate_platforms(screen, -1, 0)
                case 2:  # hero green
                    generate_platforms(screen, -2, random.choice([1, -1]))
                case 3:  # hero blue
                    generate_platforms(screen, -3, random.choice([1, -1, 2, -2]))

        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            # нажатие клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.reset_vx()
                    moving_left = False
                if event.key == pygame.K_d:
                    player.reset_vx()
                    moving_right = False

        # перемещение по оси x
        if moving_left:
            player.move_x(-1)
        if moving_right:
            player.move_x(1)

        # отрисовка всего
        screen.fill((0, 0, 0))
        score_count.draw()
        PLAYER.draw(screen)
        PLATFORMS.draw(screen)

        # обновление спрайтов
        PLAYER.update()
        PLATFORMS.update()

        score_count.update()
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


# STABLE - класс окна конца игры
class GameOver:
    def __init__(self, screen, width, height, your_score, level_n):
        self.screen = screen
        self.width = width
        self.height = height
        self.running = True
        self.score = your_score
        self.ifhighscore = add_score_to_database(self.score, f"level{level_n}")

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
            # STABLE - создание кнопок и настройка их внешнего вида
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
                (self.width // 2 - text.get_width() // 2 - 20, self.height // 2 - text.get_height() // 2 - 300),
                (text.get_width() + 40, text.get_height() + 40),
            )

            pygame.draw.rect(self.screen, (255, 255, 255), frame, 5)
            self.screen.blit(text, (frame.x + 20, frame.y + 20))

            score_text = "Your score: " + str(self.score)
            score_font = pygame.font.SysFont("Arial", 30, bold=True)
            textsc = score_font.render(score_text, True, (255, 255, 255))
            textsc_x = self.width // 2 - textsc.get_width() // 2
            textsc_y = self.height // 2 - textsc.get_height() // 2 - 100
            self.screen.blit(textsc, (textsc_x, textsc_y))

            if self.ifhighscore:
                textsc_x = self.width // 2 - textsc.get_width() // 2
                textsc_y = self.height // 2 - textsc.get_height() // 2 - 150
                textsc = score_font.render("New highscore!", True, (255, 255, 255))
                self.screen.blit(textsc, (textsc_x, textsc_y))

            # STABLE - получение ввода от игрока
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_button.collidepoint(event.pos):
                        # рестарт
                        self.running = False
                        self.restart()
                    elif self.quit_button.collidepoint(event.pos):
                        # выход
                        start_menu = StartMenu(self.screen, self.width, self.height)
                        self.running = False
                        start_menu.run()
            pygame.display.flip()

    # STABLE - перезапуск игры
    def restart(self):
        self.running = False


# STABLE - работа с базой данных рекордов
def add_score_to_database(score, level):
    conn = sqlite3.connect("highscores.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM scores ORDER BY {level} DESC")
    results = cursor.fetchall()
    if score not in results:
        # Вставьте новый счет в колонку level1
        cursor.execute(f"INSERT INTO scores ({level}) VALUES (?)", (score,))

    # Отсортируйте колонку level1 по убыванию
    cursor.execute(f"SELECT * FROM scores ORDER BY {level} DESC")
    results = cursor.fetchall()

    print(results)
    # Проверьте, является ли первый элемент новым рекордом
    if results[0][int(level[-1]) - 1] == score:
        conn.commit()
        conn.close()
        return True
    else:
        conn.commit()
        conn.close()
        return False
