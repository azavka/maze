import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабиринт")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)

# Настройки лабиринта
TILE_SIZE = 40
COLS, ROWS = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]

# Настройки игрока
PLAYER_SIZE = TILE_SIZE // 2
player_x, player_y = TILE_SIZE // 4, TILE_SIZE // 4  # Начальная позиция игрока
player_speed = 5

def generate_maze(x=0, y=0):
    """Генерация лабиринта с помощью Backtracking."""

    # Список направлений движения
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)  # Перемешивание направлений для случайности
    maze[y][x] = 0  # Текущая ячейка становится пустой

    for dx, dy in directions:
        nx, ny = x + dx * 2, y + dy * 2  # Соседняя клетка через одну
        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
            # Убираем стену между текущей и соседней ячейкой
            maze[y + dy][x + dx] = 0
            generate_maze(nx, ny)

# Генерация лабиринта
generate_maze()

# Определение финиша (в самой дальней доступной клетке)
finish_y, finish_x = ROWS - 1, COLS - 1
while maze[finish_y][finish_x] == 1:
    if finish_x > 0:
        finish_x -= 1
    elif finish_y > 0:
        finish_y -= 1

finish_x, finish_y = finish_x * TILE_SIZE + TILE_SIZE // 4, finish_y * TILE_SIZE + TILE_SIZE // 4

# Список стен для отрисовки
walls = []
for row_idx, row in enumerate(maze):
    for col_idx, tile in enumerate(row):
        if tile == 1:
            walls.append(pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Основной игровой цикл
clock = pygame.time.Clock()
running = True
winner = False

while running:
    WINDOW.fill(WHITE)

    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получение нажатых клавиш
    keys = pygame.key.get_pressed()
    prev_x, prev_y = player_x, player_y
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Создаем прямоугольник для игрока
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

    # Проверка столкновений со стенами
    for wall in walls:
        if player_rect.colliderect(wall):
            player_x, player_y = prev_x, prev_y  # Возврат позиции игрока при столкновении

    # Проверка победы
    if abs(player_x - finish_x) < TILE_SIZE // 2 and abs(player_y - finish_y) < TILE_SIZE // 2:
        winner = True
        running = False

    # Отрисовка лабиринта
    for wall in walls:
        pygame.draw.rect(WINDOW, BLUE, wall)

    # Отрисовка финиша
    pygame.draw.rect(WINDOW, GREEN, (finish_x, finish_y, TILE_SIZE // 2, TILE_SIZE // 2))

    # Отрисовка игрока
    pygame.draw.rect(WINDOW, RED, player_rect)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(30)

# Сообщение о победе
if winner:
    print("Поздравляем! Вы прошли лабиринт!")

pygame.quit()
sys.exit()
