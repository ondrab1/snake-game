import pygame
import time
from src.snake import Snake
from src.food import Food
from src.level import Level, TestLevel
from src.settings import Settings
from typing import Union


class Game:
    def __init__(self):
        self.speed: float = 1.0
        self.level: Union[Level, None] = None

    def run(self) -> None:
        self.load_level()

        screen = self.prepare_screen()

        end = False
        clock = pygame.time.Clock()

        move: tuple = self.level.DEFAULT_MOVE
        start_x, start_y = self.level.DEFAULT_POSITION

        snake: Snake = Snake(start_x, start_y)

        food: Food = Food()
        food.spawn(screen)

        while not end:
            clock.tick(Settings.FPS)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True

                # move set
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        move = (0, 1)
                    elif event.key == pygame.K_UP:
                        move = (0, -1)
                    elif event.key == pygame.K_RIGHT:
                        move = (1, 0)
                    elif event.key == pygame.K_LEFT:
                        move = (-1, 0)

            screen.fill(Settings.BACKGROUND)

            # render food
            food.render(screen)

            # render snake
            snake.render(screen, move)

            # render walls
            self.level.render(screen)

            # on collision with food
            if snake.in_collision_with(food.spawned):
                snake.increase_length()
                food.destroy()
                food.spawn(screen)
                self.speed += 0.1

            # on collision with wall
            for wall in self.level.walls:
                if snake.in_collision_with(wall):
                    print('wall collision')

            # display it
            pygame.display.flip()

            # game speed
            time.sleep((300 / min(self.speed, Settings.MAX_SPEED)) / 1000)

    def load_level(self):
        self.level = TestLevel()

    def prepare_screen(self) -> pygame.Surface:
        pygame.init()

        pygame.display.set_caption("Snake by ondrab")

        size = [Settings.FIELD_SIZE * 50, Settings.FIELD_SIZE * 35]
        screen = pygame.display.set_mode(size)

        return screen
