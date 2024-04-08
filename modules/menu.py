import pygame
from sys import exit

from modules import levels


def Menu():
    button_group = pygame.sprite.Group()
    button_group.add(Button("Start", 450, 650, 200, 100, 'yellow'))
    button_group.add(Button("Start", 475, 625, 300, 70, 'red'))
    button_group.add(Button("Start", 475, 625, 400, 70, 'green'))
    button_group.add(Button("Start", 475, 625, 500, 70, 'purple'))
    return button_group


class Button(pygame.sprite.Sprite):
    def __init__(self, typeB: str, begin_coord, end_coord, y, height, color):
        super().__init__()
        self.typeB = typeB
        self.begin = begin_coord
        self.end = end_coord
        self.y = y
        self.height = height
        self.color = color
        font = pygame.font.Font('font/SuperMario256.ttf', 40)
        self.font = font.render(typeB, False, 'red')
        text_dim = self.font.get_rect()
        text_dim.center = (1100 // 2, 600 // 2)
        self.txt = pygame.Surface((self.end - self.begin), self.height)
        self.image = pygame.Surface((self.end - self.begin, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(self.begin, self.y))
