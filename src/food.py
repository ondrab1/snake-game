from typing import Union
import pygame
import math
import random
from src.settings import Settings


class Food:
    def __init__(self):
        self.spawned: Union[pygame.Rect, None] = None

    def get_rect(self) -> Union[pygame.Rect, None]:
        return self.spawned

    def spawn(self, screen: pygame.Surface):
        if self.spawned:
            return

        # find food position - should not be in collision with snake OR with wall

        x, y = self.get_random_position(screen)

        self.spawned = pygame.draw.rect(screen, (255, 255, 255), [x, y, Settings.FIELD_SIZE, Settings.FIELD_SIZE])

    def render(self, screen: pygame.Surface):
        if self.spawned:
            pygame.draw.rect(screen, (255, 255, 255), self.spawned)
        else:
            self.spawn(screen)

    def destroy(self):
        self.spawned = None

    def get_random_position(self, screen: pygame.Surface) -> tuple:
        x = random.randrange(0, math.ceil(screen.get_width() / Settings.FIELD_SIZE)) * Settings.FIELD_SIZE
        y = random.randrange(0, math.ceil(screen.get_height() / Settings.FIELD_SIZE)) * Settings.FIELD_SIZE

        return x, y

