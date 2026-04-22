import sys
from random import choice, randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цветовая гамма - Мега Неон
BOARD_BACKGROUND_COLOR = (30, 30, 60)
BORDER_COLOR = (255, 0, 0)
APPLE_COLOR = (0, 255, 255)
SNAKE_COLOR = (255, 0, 255)
DIGEST_COLOR = (255, 255, 0)  # Съеденное яблоко

POISON_APPLE_COLOR = (139, 0, 0)  # Ядовитое яблоко

# Скорость движения змейки:
SPEED = 22

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Создание родительского класса."""

    def __init__(self, color=None, position=SCREEN_CENTER):
        self.body_color = color
        self.position = position

    def draw(self):
        """Создание пустого метода отрисовки объектов."""
        raise NotImplementedError('Метод draw() надо переопределить в классе '
                                  f'{self.__class__.__name__}!')

    @staticmethod
    def draw_rect(position, color, is_need_border=True):
        """Метод, создающий объект rect, отрисовка."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        if is_need_border:
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Создание дочернего класса для объекта яблоко."""

    def __init__(self, all_positions=None, color=APPLE_COLOR):
        super().__init__(color)
        self.randomize_position(all_positions or [])

    def randomize_position(self, all_positions):
        """Метод, который генерирует рандомную позицию."""
        while all_positions:
            self.position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                             randrange(0, SCREEN_HEIGHT, GRID_SIZE))
            if self.position not in all_positions:
                break

    def draw(self):
        """Метод, который отрисовывает объект яблока."""
        self.draw_rect(self.position, self.body_color)


class PoisonApple(Apple):
    """Создание дочернего класса для ядовитого яблока."""


class Snake(GameObject):
    """Создание дочернего класса для змейки."""

    def __init__(self, color=SNAKE_COLOR):
        super().__init__(color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.digesting = []

    def update_direction(self):
        """Метод, который обновляет направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, отвечающий за движение."""
        current_x, current_y = self.get_head_position()
        new_pos = ((current_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                   (current_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_pos)

        self.digesting = [i + 1 for i in self.digesting
                          if i + 1 < len(self.positions)]
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Метод, который отрисовывает объект."""
        for index, position in enumerate(self.positions):
            color = (DIGEST_COLOR if index in self.digesting
                     else self.body_color)
            self.draw_rect(position, color)

        # Затирание последнего сегмента
        if self.last:
            self.draw_rect(self.last, BOARD_BACKGROUND_COLOR, False)

    def get_head_position(self):
        """Метод, который возвращает координаты головы змеи."""
        return self.positions[0]

    def eat_apple(self):
        """Метод, при котором яблоко съедено."""
        self.length += 1
        self.digesting.append(0)

    def eat_poison_apple(self):
        """Метод, при котором ядовитое яблоко съедено."""
        self.length -= 1
        self.positions.pop()

    def reset(self):
        """Метод, который отвечает за обнуление поля."""
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.length = 1
        self.last = None
        self.digesting = []


def handle_keys(game_object):
    """Функция, которая передаёт пользовательские действия."""
    game_object.update_direction()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def main():
    """Основная функция, которая запускает игру и включает логику."""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    poison_apple = PoisonApple([*snake.positions, apple.position],
                               POISON_APPLE_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        # Основная логика игры.
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.eat_apple()
            apple.randomize_position([*snake.positions, poison_apple.position])
        elif snake.get_head_position() in set(snake.positions[4:]):
            snake.reset()
            screen.fill((0, 0, 0))
            apple.randomize_position([*snake.positions, poison_apple.position])
            poison_apple.randomize_position([*snake.positions, apple.position])
        elif snake.get_head_position() == poison_apple.position:
            if len(snake.positions) <= 1:
                snake.reset()
                screen.fill((0, 0, 0))
                apple.randomize_position([*snake.positions,
                                          poison_apple.position])
                poison_apple.randomize_position([*snake.positions,
                                                 apple.position])
            else:
                snake.eat_poison_apple()
                poison_apple.randomize_position([*snake.positions,
                                                 apple.position])

        snake.draw()
        apple.draw()
        poison_apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
