import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 50))
        self.image.fill('Red')
        self.rect = self.image.get_rect(midbottom=(200,400))
        self.xmap = 0
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 400:
            self.gravity = -20
        if keys[pygame.K_LEFT]:
            if self.rect.x -5<=100:
                self.xmap -= 5
            else:
                self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            if self.rect.x + 5 >= 1000:
                self.xmap += 5
            else:
                self.rect.x += 5
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 400:
            self.rect.bottom = 400
    def update(self):
        self.player_input()
        self.apply_gravity()
        return (self.xmap)


class Map(pygame.sprite.Sprite):
    def __init__(self, begin_coordinate, end_coordinate):
        super().__init__()
        self.begin = begin_coordinate
        self.end = end_coordinate
        self.image = pygame.Surface((self.end - self.begin, 200))
        self.image.fill('Green')
        self.rect = self.image.get_rect(topleft=(self.begin, 400))
    def update(self,xmap):
        self.rect.x = self.begin - xmap


# class Enemy():