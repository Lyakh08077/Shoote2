import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Простой шутер")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Игровые параметры
bullet_speed = 3
enemy_speed = 0.5
enemy_spawn_rate = 0.005
enemy_bullet_speed = 1.5
enemy_shoot_timer = 180
enemy_shoot_interval = 180
enemy_movement_delay = 300
bullets = []
enemies = []
enemy_bullets = []
frame_count = 0
game_started = False  # Переменная для отслеживания начала игры

# Игрок
player_size = 50
player_speed = 1
player = pygame.Rect(WIDTH / 2 - player_size / 2, HEIGHT - player_size, player_size, player_size)

# Функция для отрисовки пуль
def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

# Функция для отрисовки врагов
def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, WHITE, enemy)

# Функция для отрисовки пуль врагов
def draw_enemy_bullets():
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, RED, bullet)

# Функция для завершения игры
def game_over():
    pygame.quit()
    sys.exit()

# Основной игровой цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = pygame.Rect(player.centerx - 2, player.top, 4, 10)
            bullets.append(bullet)
            game_started = True  # Начало игры после выстрела игрока

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_d] and player.right < WIDTH:
        player.x += player_speed
    if keys[pygame.K_w] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_s] and player.bottom < HEIGHT:
        player.y += player_speed

    # Движение пуль игрока
    for bullet in bullets:
        bullet.y -= bullet_speed

    if game_started:
        # Создание новых врагов
        if random.random() < enemy_spawn_rate:
            enemy = pygame.Rect(random.randint(0, WIDTH - player_size), 0, player_size, player_size)
            enemies.append(enemy)

        # Увеличиваем счетчик кадров
        frame_count += 1

        # Если достигнута задержка для начала движения врагов
        if frame_count >= enemy_movement_delay:
            # Движение врагов и выстрелы
            for enemy in enemies:
                enemy.y += enemy_speed

                # Проверяем, прошло ли достаточно времени для следующего выстрела врага
                if enemy_shoot_timer <= 0:
                    enemy_bullet = pygame.Rect(enemy.centerx - 2, enemy.bottom, 4, 10)
                    enemy_bullets.append(enemy_bullet)
                    enemy_shoot_timer = enemy_shoot_interval
                else:
                    enemy_shoot_timer -= 1

        # Движение пуль врагов
        for bullet in enemy_bullets:
            bullet.y += enemy_bullet_speed

    # Проверка столкновения пуль игрока с врагами
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)

    # Проверка столкновения пуль врагов с игроком
    for bullet in enemy_bullets:
        if bullet.colliderect(player):
            enemy_bullets.remove(bullet)
            game_over()

    # Проверка столкновения игрока с врагами
    for enemy in enemies:
        if player.colliderect(enemy):
            game_over()

    # Отрисовка
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), player)
    draw_bullets()
    draw_enemies()
    draw_enemy_bullets()
    
    pygame.display.flip()
