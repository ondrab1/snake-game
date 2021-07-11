import pygame
import time
from typing import List
from src.snake import Snake
from src.food import Food
from src.level import Level, LevelList, SecondLevel
from src.settings import Settings


class Game:
    END_GAME = 'end_game'
    END_LEVEL = 'end_level'

    def __init__(self):
        self.speed: float = 1.0
        self.score: int = 0
        self.level_index = 0

    def set_initial_state(self):
        self.speed: float = 1.0
        self.score: int = 0

    def run(self) -> None:
        level_list: LevelList = LevelList()
        level_index: int = 0
        play_again: bool = True

        total_levels: int = len(level_list.get_levels())

        while play_again:
            end_type = self.main(self.load_level(level_list.get_levels(), level_index))

            if end_type == self.END_GAME:
                play_again = False
            elif end_type == self.END_LEVEL:
                level_index += 1


    def main(self, level: Level):
        screen = self.prepare_screen()

        end = False
        end_type = None

        clock = pygame.time.Clock()

        move: tuple = level.DEFAULT_MOVE
        start_x, start_y = level.get_start_position(screen)

        snake: Snake = Snake(start_x, start_y)

        food: Food = Food()
        food.spawn(screen)

        while not end:
            clock.tick(Settings.FPS)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                    end_type = self.END_GAME

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
            level.render(screen)

            # on collision with food
            if snake.in_collision_with(food.spawned):
                snake.increase_length()
                food.destroy()
                food.spawn(screen)
                self.speed += 0.1
                self.score += 1
                if self.score == level.SCORE_GOAL:
                    end = True
                    end_type = self.END_LEVEL

                print('Score', self.score)

            # on collision with wall
            for wall in level.walls:
                if snake.in_collision_with(wall):
                    end = True
                    end_type = self.END_GAME

            # display it
            pygame.display.flip()

            # game speed
            time.sleep((300 / min(self.speed, Settings.MAX_SPEED)) / 1000)

        return end_type

    def load_level(self, levels: List, level_index: int):
        return levels[level_index]()

    def prepare_screen(self) -> pygame.Surface:
        pygame.init()

        pygame.display.set_caption("Snake by ondrab")

        size = [Settings.FIELD_SIZE * 50, Settings.FIELD_SIZE * 35]
        screen = pygame.display.set_mode(size)

        return screen
