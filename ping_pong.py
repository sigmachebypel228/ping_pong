import pygame
import sys
import math  # Импортируем модуль для вычисления длины вектора скорости

# Инициализация Pygame
pygame.init()

# Загрузка звукового файла
bounce_sound = pygame.mixer.Sound('otskok-myacha.wav')

# Настройки экрана
SCR_WIDTH = 1280
SCR_HEIGHT = 720
screen = pygame.display.set_mode([SCR_WIDTH, SCR_HEIGHT])
pygame.display.set_caption("Пинг-понг")

# Размеры и параметры объектов
PADDLE_WIDTH = 25
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10

BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

MAX_BALL_SPEED = 15  # Максимальная скорость мяча

# Координаты объектов
paddle_1_rect = pygame.Rect(0, SCR_HEIGHT // 2 - PADDLE_HEIGHT // 2,
                            PADDLE_WIDTH, PADDLE_HEIGHT)

paddle_2_rect = pygame.Rect(SCR_WIDTH - PADDLE_WIDTH,
                            SCR_HEIGHT // 2 - PADDLE_HEIGHT // 2,
                            PADDLE_WIDTH, PADDLE_HEIGHT)

ball_rect = pygame.Rect(SCR_WIDTH // 2 - BALL_SIZE // 2,
                        SCR_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Счетчики очков
score_1 = 0
score_2 = 0
font = pygame.font.SysFont(None, 32)

# Режим игры (человек против компьютера)
ai_mode = False
if len(sys.argv) > 1:
    if sys.argv[1] == '--human':
        ai_mode = False


# Функция обновления положения компьютерной ракетки
def update_ai():
    if ball_rect.x > SCR_WIDTH // 2:
        if ball_rect.centery < paddle_2_rect.centery:
            paddle_2_rect.y -= PADDLE_SPEED
        elif ball_rect.centery > paddle_2_rect.centery:
            paddle_2_rect.y += PADDLE_SPEED
        if paddle_2_rect.top <= 0:
            paddle_2_rect.top = 0
        if paddle_2_rect.bottom > SCR_HEIGHT:
            paddle_2_rect.bottom = SCR_HEIGHT
    else:
        paddle_2_rect.centery += (SCR_HEIGHT // 2 - paddle_2_rect.centery) / PADDLE_SPEED


# Основные цвета
BACKGROUND = (0, 0, 0)  # Черный фон
WHITE = (255, 255, 255)  # Белый цвет для элементов

# Частота кадров
FPS = 60
clock = pygame.time.Clock()

# Основной цикл игры
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:  # Движение вверх для игрока 1
        paddle_1_rect.y -= PADDLE_SPEED
        if paddle_1_rect.top <= 0:
            paddle_1_rect.top = 0
    if keys[pygame.K_s]:  # Движение вниз для игрока 1
        paddle_1_rect.y += PADDLE_SPEED
        if paddle_1_rect.bottom >= SCR_HEIGHT:
            paddle_1_rect.bottom = SCR_HEIGHT

    if keys[pygame.K_UP]:  # Движение вверх для игрока 2
        paddle_2_rect.y -= PADDLE_SPEED
        if paddle_2_rect.top <= 0:
            paddle_2_rect.top = 0
    if keys[pygame.K_DOWN]:  # Движение вниз для игрока 2
        paddle_2_rect.y += PADDLE_SPEED
        if paddle_2_rect.bottom >= SCR_HEIGHT:
            paddle_2_rect.bottom = SCR_HEIGHT

    # Движение мяча
    ball_rect.x += BALL_SPEED_X
    ball_rect.y += BALL_SPEED_Y

    # Отражение мяча от верхней и нижней границ
    if ball_rect.top <= 0 or ball_rect.bottom >= SCR_HEIGHT:
        BALL_SPEED_Y *= -1

    # Столкновение мяча с ракеткой
    if ball_rect.colliderect(paddle_1_rect) or ball_rect.colliderect(paddle_2_rect):
        bounce_sound.play()  # Воспроизводим звук столкновения
        BALL_SPEED_X *= -1.05  # Увеличиваем скорость по оси X
        BALL_SPEED_Y *= -1.05  # Увеличиваем скорость по оси Y

        # Ограничение скорости
        if abs(BALL_SPEED_X) > MAX_BALL_SPEED:
            BALL_SPEED_X = MAX_BALL_SPEED if BALL_SPEED_X > 0 else -MAX_BALL_SPEED
        if abs(BALL_SPEED_Y) > MAX_BALL_SPEED:
            BALL_SPEED_Y = MAX_BALL_SPEED if BALL_SPEED_Y > 0 else -MAX_BALL_SPEED

    # Проверка выхода мяча за пределы поля
    if ball_rect.left <= 0:
        ball_rect = pygame.Rect(SCR_WIDTH // 2 - BALL_SIZE // 2,
                                SCR_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        score_2 += 1
    if ball_rect.right >= SCR_WIDTH:
        ball_rect = pygame.Rect(SCR_WIDTH // 2 - BALL_SIZE // 2,
                                SCR_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        score_1 += 1

    # Логика компьютерного игрока
    if ai_mode:
        update_ai()

    # Расчет текущей скорости мяча
    current_speed = int(math.sqrt(BALL_SPEED_X ** 2 + BALL_SPEED_Y ** 2))

    # Отрисовка фона и объектов
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, WHITE, paddle_1_rect)
    pygame.draw.rect(screen, WHITE, paddle_2_rect)
    pygame.draw.ellipse(screen, WHITE, ball_rect)
    pygame.draw.line(screen, WHITE, (SCR_WIDTH // 2, 0), (SCR_WIDTH // 2, SCR_HEIGHT), 5)

    # Отображаем счет
    score_text = font.render(f'{score_1} : {score_2}', True, WHITE)
    screen.blit(score_text, (SCR_WIDTH // 2 - score_text.get_width() // 2, 10))

    # Отображаем табло скорости
    speed_text = font.render(f'Скорость: {current_speed}', True, WHITE)
    screen.blit(speed_text, (SCR_WIDTH - 200, 10))

    # Проверка условия окончания игры
    if score_1 >= 10 or score_2 >= 10:
        running = False

    # Обновление экрана
    pygame.display.flip()

    # Ограничение частоты кадров
    clock.tick(FPS)

# Завершение работы Pygame
pygame.quit()