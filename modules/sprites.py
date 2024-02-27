import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 50))
        self.image.fill('Red')
        self.rect = self.image.get_rect(midbottom=(550,400))
        self.xmap = 0
        self.gravity = 0
        self.game_active =True
        self.wall_shift = 0

    def input_jumping(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -20
        else:
            self.gravity = 0
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 800:
            self.game_active = False
            self.kill()

    def walking(self, left, right):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and left:
            if self.rect.x -5<=450:
                self.xmap -= 5
            else:
                self.rect.x -= 5
        if keys[pygame.K_RIGHT] and right:
            if self.rect.x + 5 >= 650:
                self.xmap += 5
            else:
                self.rect.x += 5

    def moving(self,collide_map):
        left, right = True, True
        if collide_map:
            if self.rect.bottom<=410:
                self.rect.bottom = 401
                self.input_jumping()
            else:
                if self.rect.center < collide_map.get_center():
                    right = False
                else:
                    left = False


        self.apply_gravity()
        self.walking(left,right)

    def update(self,collide_map):
        self.moving(collide_map)
        return (self.xmap, self.game_active)


class Map(pygame.sprite.Sprite):
    def __init__(self, begin_coordinate, end_coordinate):
        super().__init__()
        self.begin = begin_coordinate
        self.end = end_coordinate
        self.image = pygame.Surface((self.end - self.begin, 200))
        self.image.fill('Green')
        self.rect = self.image.get_rect(topleft=(self.begin, 400))

    def get_center(self):
        return self.rect.center
    def update(self,xmap):
        self.rect.x = self.begin - xmap


# class Enemy():