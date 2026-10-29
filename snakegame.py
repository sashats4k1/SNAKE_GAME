import random
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 40
FPS = 6

BOARD_BACKGROUND_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 200, 0)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        center_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(center_pos, APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока."""
        x = random.randint(
            0, SCREEN_WIDTH // GRID_SIZE - 1
        ) * GRID_SIZE
        y = random.randint(
            0, SCREEN_HEIGHT // GRID_SIZE - 1
        ) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(
            self.position[0], self.position[1],
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        center_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(center_pos, SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        start_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        start_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        self.positions = [(start_x, start_y)]
        self.last = None
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.direction = random.choice(directions)
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения."""
        if self.next_direction:
            if (self.direction[0] != -self.next_direction[0] or
                    self.direction[1] != -self.next_direction[1]):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Передвигает змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def draw(self, surface):
        """Отрисовывает змейку."""
        if self.last:
            rect = pygame.Rect(
                self.last[0], self.last[1],
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)

        for segment in self.positions:
            rect = pygame.Rect(
                segment[0], segment[1],
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, self.body_color, rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                snake.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT:
                snake.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = (1, 0)


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position()

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
