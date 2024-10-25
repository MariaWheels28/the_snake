from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

DEFAULT_COLOR = (0, 0, 0)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5  # 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Игра "Змейка"')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Основной класс игры."""

    def __init__(self) -> None:
        """Инициализация объектов класс GameObject."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = DEFAULT_COLOR

    def draw(self):
        """Пустая функция отрисовки объектов на поле."""
        pass


class Apple(GameObject):
    """Класс, который описывает объект Apple."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR

    # Метод draw класса Apple
    def draw(self):
        """Отрисовка объекта Apple на поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, positions):
        """Метод объекта класса Apple. Задает новое местоположения объекта."""
        self.position = (
            (randint(0, GRID_WIDTH - 1) * GRID_SIZE),
            (randint(0, GRID_HEIGHT - 1) * GRID_SIZE),
        )
        if self.position in positions:
            self.position = positions[len(positions) - 1]


class Snake(GameObject):
    """Класс, который описывает объект Snake."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    # Метод draw класса Snake.
    # Отрисовывает все, кроме последней ячейки.
    def draw(self):
        """Метод класса Snake. Отрисовывает объект на поле."""
        if len(self.positions) == 1:
            # Отрисовка головы змейки
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            # head_rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        else:
            # Отрисовка всего тела, кроме хвоста.
            for position in self.positions[:-1]:
                rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, self.body_color, rect)
                pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
            # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод объекта Snake. Возвращает первую позицию Змейки."""
        return self.positions[0]

    def reset(self):
        """Метод объекта Snake."""
        """Сброс игры. Возвращение игры в начало с начальными позициями."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([DOWN, UP, LEFT, RIGHT])

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Метод объекта Snake."""
        """Обновление направления движения объекта Snake."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод объекта Snake."""
        """Обновляет положение объекта, имитируя движение."""
        head = self.get_head_position()
        self.update_direction()
        if self.direction == RIGHT:
            if head[0] + 20 == SCREEN_WIDTH:
                self.positions.insert(0, (0, (head[1])))
            else:
                self.positions.insert(0, ((head[0] + 20), (head[1])))
        elif self.direction == LEFT:
            if head[0] == 0:
                self.positions.insert(0, ((SCREEN_WIDTH - 20), (head[1])))
            else:
                self.positions.insert(0, ((head[0] - 20), (head[1])))
        elif self.direction == UP:
            if head[1] == 0:
                self.positions.insert(0, ((head[0]), (SCREEN_HEIGHT - 20)))
            else:
                self.positions.insert(0, ((head[0]), (head[1] - 20)))
        elif self.direction == DOWN:
            if head[1] + 20 == SCREEN_HEIGHT:
                self.positions.insert(0, ((head[0]), 0))
            else:
                self.positions.insert(0, ((head[0]), (head[1] + 20)))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция запуска игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        # Если змейка 'стукнулась' сама в себя.
        if snake.length > 1 and snake.positions[0] in snake.positions[1:]:
            snake.reset()
        apple.draw()
        snake.draw()
        pygame.display.update()
        # Если змейка скушала яблоко.
        if apple.position == snake.positions[0]:
            snake.length += 1
            apple.randomize_position(snake.positions)


if __name__ == '__main__':
    main()
