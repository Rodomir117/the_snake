from random import randint

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

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет камня
ROCK_COLOR = (100, 100, 100)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Содержит общие атрибуты игровых объектов."""

    def __init__(self) -> None:
        """Инициализирует базовые атрибуты объекта,такие как позиция и цвет."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Будет определен в дочерних классах."""


class Apple(GameObject):
    """Атрибуты игрового объекта яблока."""

    def __init__(self) -> None:
        super().__init__()
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self) -> tuple[int, int]:
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Атрибуты игрового объекта змейка."""

    def __init__(self) -> None:
        super().__init__()
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.positions = [(self.position[0], self.position[1])]
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Oбновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Oбновляет позицию змейки."""
        self.update_direction()
        head_x, head_y = self.get_head_position()
        x, y = self.direction
        new_head = (
            (head_x + x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            pygame.draw.rect(
                screen, self.body_color,
                (*position, GRID_SIZE, GRID_SIZE)
            )

        head_position = self.get_head_position()
        left_eye_position = (
            head_position[0] + GRID_SIZE // 3,
            head_position[1] + GRID_SIZE // 3
        )
        right_eye_position = (
            head_position[0] + 2 * GRID_SIZE // 3,
            head_position[1] + GRID_SIZE // 3
        )

        if self.direction == LEFT:
            pygame.draw.circle(
                screen, BOARD_BACKGROUND_COLOR,
                left_eye_position, 3
            )
        elif self.direction == RIGHT:
            pygame.draw.circle(
                screen, BOARD_BACKGROUND_COLOR,
                right_eye_position, 3
            )
        else:
            pygame.draw.circle(
                screen, BOARD_BACKGROUND_COLOR,
                right_eye_position, 3
            )
            pygame.draw.circle(
                screen, BOARD_BACKGROUND_COLOR,
                left_eye_position, 3
            )

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [(self.position[0], self.position[1])]
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для движения змейки."""
    direction_list = {
        (pygame.K_UP, DOWN): UP,
        (pygame.K_DOWN, UP): DOWN,
        (pygame.K_LEFT, RIGHT): LEFT,
        (pygame.K_RIGHT, LEFT): RIGHT,
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            for keys, value in direction_list.items():
                if event.key == keys[0] and game_object.direction != keys[1]:
                    game_object.next_direction = value


class Rock(GameObject):
    """Атрибуты игрового объекта камень."""

    def __init__(self) -> None:
        super().__init__()
        self.randomize_position()
        self.body_color = ROCK_COLOR

    def randomize_position(self) -> tuple[int, int]:
        """Устанавливает случайное положение камня на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовывает камень на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def main():
    """Бесконечный цикл игры, пока пользователь не закроет окно."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    rock = Rock()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()
            rock.randomize_position()
        elif snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif snake.get_head_position() == rock.position:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        rock.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
