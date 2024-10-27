from random import choice, randint

import pygame as pg

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
SPEED = 4  # 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Игра "Змейка"')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Основной класс игры."""

    def __init__(self, body_color=DEFAULT_COLOR) -> None:
        """Инициализация объектов класс GameObject."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Пустая функция отрисовки объектов на поле."""
        raise NotImplementedError

    def draw_cell(self, position=None):
        """Отрисовка ячейки."""
        rect = pg.Rect(position if position else self.position,
                       (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, который описывает объект Apple."""

    def randomize_position(self, positions):
        """Установка нового местоположения объекта."""
        while True:
            self.position = (
                (randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                (randint(0, GRID_HEIGHT - 1) * GRID_SIZE),
            )
            if self.position not in positions:
                break


class Snake(GameObject):
    """Класс, который описывает объект Snake."""

    def __init__(self, body_color=DEFAULT_COLOR) -> None:
        super().__init__()
        self.reset()
        self.next_direction = None
        self.last = None
        self.body_color = body_color

    def draw(self, reset=False):
        """Отрисовывка объекта на поле."""
        if reset:
            screen.fill(BOARD_BACKGROUND_COLOR)
        for position in self.positions:
            self.draw_cell(position)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает первую позицию Змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс игры. Возвращение игры в начало с начальными позициями."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([DOWN, UP, LEFT, RIGHT])

    def update_direction(self):
        """Обновление направления движения объекта Snake."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление положения объекта, имитация движения."""
        self.update_direction()
        board_x, board_y = self.get_head_position()
        direction_x, direction_y = self.direction
        self.positions.insert(0, ((board_x + 20 * direction_x) % SCREEN_WIDTH,
                              (board_y + 20 * direction_y) % SCREEN_HEIGHT))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция запуска игры."""
    pg.init()
    apple = Apple(APPLE_COLOR)
    snake = Snake(SNAKE_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        # Если змейка 'стукнулась' сама в себя.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            snake.draw(True)
            apple.draw_cell()
        else:
            apple.draw_cell()
            snake.draw()
        pg.display.update()
        # Если змейка 'скушала' яблоко.
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position(snake.positions)


if __name__ == '__main__':
    main()
