import pygame
import random

class PlayerObject:
    def __init__(self, screen):
        self.screen = screen

    def draw(self, x, y): 
        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 25, 5)
    
    #UNSTABLE - имеется баг с застреванием игрока в объектах, проверки нуждаются в корректировке
    def if_otskok(self, x, y,  v, delta_time, objects):
        otskok = False
        for obj in objects:
            obj_x, obj_y, obj_width, obj_height = obj
            if (y + 25 >= obj_y and y - 25 <= obj_y + obj_height) and (x + 25 >= obj_x and x - 25 <= obj_x + obj_width):
                if v > 0 and y - 25 < obj_y:
                    y = obj_y - 25
                    otskok = True
                elif v < 0 and y + 25 > obj_y + obj_height: 
                    y = obj_y + obj_height + 25  
                    otskok = True
        if otskok:
            v = -0.85 * v
            v += delta_time / 3000 
        else:
            v += delta_time / 3000
        return v
            
#STABLE - пресеты          
pygame.init()
width = 480
height = 920
screen = pygame.display.set_mode((width, height))
x, y = 240, 10
running = True
moving_left = False
moving_right = False
previous_time = pygame.time.get_ticks()
player_object = PlayerObject(screen)
v = 0

#UNSTABLE BASE - временная заглушка для отработки функции отскока. В будущем будет заменена на класс Objects
howmuch = 4
objects = []
for _ in range(howmuch):
    trai = False
    while not trai:
        obj_x = random.randint(100, 201)
        obj_y = random.randint(25, 895)
        if all(abs(obj_y - another[1]) > 75 for another in objects):
            trai = True
            objects.append((obj_x, obj_y, random.randint(10, 200), 20))

    


while running:
    #Часть, отвечающая за движения игрока по оси x - STABLE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
    if moving_left:
        x -= 0.2
    if moving_right:
        x += 0.2

    #timer - STABLE
    current_time = pygame.time.get_ticks()  # Получение текущего времени
    delta_time = current_time - previous_time  # Вычисление разницы во времени
    previous_time = current_time # Обновление предыдущего времени
    
    #изменение по оси y, нахождение "в рамках" - STABLE
    v = player_object.if_otskok(x, y, v, delta_time, objects)
    y += v  
    if x > width - 25:
        x = width - 25
    if x < 25:
        x = 25
    if y >= height - 25:
        running = False
    
    #STABLE - заполнение поля
    screen.fill((0, 0, 0))
    player_object.draw(x, y)
    for i in range(len(objects)):
        pygame.draw.rect(screen, (255, 255, 255), objects[i], 5)
    pygame.display.flip()
    
    
    
