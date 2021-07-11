from typing import List

import pygame
from src.settings import Settings


class Level:
    NAME: str = ''
    DEFAULT_MOVE: tuple = ()
    DEFAULT_POSITION: tuple = ()
    SCORE_GOAL: int = 10

    def __init__(self):
        self.walls: List[pygame.Rect] = []

    def get_walls_definition(self) -> List[List[tuple]]:
        return []

    def get_start_position(self, screen: pygame.Surface):
        percentage_x, percentage_y = self.DEFAULT_POSITION

        start_x = max(self._round_to_field_size((screen.get_width() / 100) * percentage_x, Settings.FIELD_SIZE) - Settings.FIELD_SIZE, 0)
        start_y = max(self._round_to_field_size((screen.get_height() / 100) * percentage_y, Settings.FIELD_SIZE) - Settings.FIELD_SIZE, 0)

        return start_x, start_y

    def render(self, screen: pygame.Surface):
        self.walls = []

        # create walls
        for definition in self.get_walls_definition():
            start, end = definition

            percentage_start_x, percentage_start_y = start
            percentage_end_x, percentage_end_y = end

            start_x = max(self._round_to_field_size((screen.get_width() / 100) * percentage_start_x, Settings.FIELD_SIZE), 0)
            start_y = max(self._round_to_field_size((screen.get_height() / 100) * percentage_start_y, Settings.FIELD_SIZE), 0)

            end_x = max(self._round_to_field_size((screen.get_width() / 100) * percentage_end_x, Settings.FIELD_SIZE), 0)
            end_y = max(self._round_to_field_size((screen.get_height() / 100) * percentage_end_y, Settings.FIELD_SIZE), 0)

            field_decrement = Settings.FIELD_SIZE

            if start_x == end_x and end_x != 0:
                end_x -= field_decrement

            if start_y == end_y and end_y != 0:
                end_y -= field_decrement

            diff_x = int((end_x - start_x) / Settings.FIELD_SIZE)
            diff_y = int((end_y - start_y) / Settings.FIELD_SIZE)

            positions = []

            for i in range(diff_x):
                positions.append((start_x + (Settings.FIELD_SIZE * i), end_y))

            index_exists = False
            for i in range(diff_y):
                try:
                    if positions[i]:
                        index_exists = True
                except IndexError:
                    index_exists = False

                if index_exists:
                    position_x, tmp = positions[i]
                    positions[i] = (position_x, start_y + (Settings.FIELD_SIZE * i))
                else:
                    positions.append((end_x, start_y + (Settings.FIELD_SIZE * i)))

            # render walls
            for position in positions:
                x, y = position
                self.walls.append(pygame.draw.rect(screen, Settings.WALL_COLOR, [x, y, Settings.FIELD_SIZE, Settings.FIELD_SIZE]))

    def _round_to_field_size(self, x: int, base: int) -> int:
        return base * round(x / base)


class FirstLevel(Level):
    NAME: str = 'First level'
    DEFAULT_MOVE: tuple = (0, 1)
    DEFAULT_POSITION: tuple = (50, 50)
    SCORE_GOAL: int = 3


class SecondLevel(Level):
    NAME: str = 'Second level'
    DEFAULT_MOVE: tuple = (0, 1)
    DEFAULT_POSITION: tuple = (50, 50)
    SCORE_GOAL: int = 3

    def get_walls_definition(self) -> List[List[tuple]]:
        return [
            [(0, 0), (100, 0)],
            [(0, 0), (0, 100)],
            [(100, 0), (100, 100)],
            [(0, 100), (100, 100)],
        ]


class LevelList:
    def get_levels(self) -> List:
        return [
            FirstLevel,
            SecondLevel,
        ]
