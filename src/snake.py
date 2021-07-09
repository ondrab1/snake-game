import pygame
from src.settings import Settings
from typing import List


class Snake:
    def __init__(self, x: int, y: int):
        self.snake: List[SnakePart] = [SnakeHead(x, y)]
        self.move_direction = None
        self.x = x
        self.y = y

    def get_rect(self) -> pygame.Rect:
        return self.snake[0].get_rect()

    def in_collision_with(self, rect: pygame.Rect) -> bool:
        if self.get_rect().colliderect(rect):
            return True

        return False

    def increase_length(self, length: int = 1):
        for i in range(length):
            last = self.snake[-1]
            x, y = last.last_move

            self.snake.append(
                SnakeTail(last.x + (-x), last.y + (-y))
            )

    def render(self, screen: pygame.Surface, move: tuple):
        last_move = None

        for snake_part in self.snake:
            if last_move:
                loc = last_move
            else:
                loc = snake_part.get_move(move)

            last_move = snake_part.last_move

            snake_part.move(loc)

            if not snake_part.is_in_screen(screen):
                snake_part.set_position(
                    snake_part.get_new_position(screen)
                )

            snake_part.render(screen)


class SnakePart:
    TYPE = ''

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.last_move = None
        self.rect = None

    def get_new_position(self, screen: pygame.Surface) -> tuple:
        if self.x >= screen.get_width():
            return 0, self.y
        elif self.x < 0:
            return screen.get_width() - Settings.FIELD_SIZE, self.y
        elif self.y >= screen.get_height():
            return self.x, 0
        elif self.y < 0:
            return self.x, screen.get_height() - Settings.FIELD_SIZE

    def is_in_screen(self, screen: pygame.Surface) -> bool:
        return not (self.x >= screen.get_width() or self.y >= screen.get_height() or self.x < 0 or self.y < 0)

    def set_position(self, position: tuple):
        self.x, self.y = position

    def get_move(self, move: tuple) -> tuple:
        move_x, move_y = move

        x = move_x * Settings.FIELD_SIZE
        y = move_y * Settings.FIELD_SIZE

        return x, y

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_color(self) -> tuple:
        return 0, 0, 0

    def move(self, move: tuple):
        x, y = move

        self.last_move = move

        self.x += x
        self.y += y

    def render(self, screen: pygame.Surface):
        self.rect = pygame.draw.rect(screen, self.get_color(), [self.x, self.y, Settings.FIELD_SIZE, Settings.FIELD_SIZE])


class SnakeHead(SnakePart):
    TYPE = 'head'


class SnakeTail(SnakePart):
    TYPE = 'tail'

    def get_color(self) -> tuple:
        return 47, 79, 79
