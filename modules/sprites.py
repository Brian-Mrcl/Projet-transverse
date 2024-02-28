import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 70))
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
            if self.rect.bottom <= collide_map.get_height() +30:
                self.rect.bottom = collide_map.get_height() +1
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
    def __init__(self, begin_coordinate, end_coordinate, height=400):
        super().__init__()
        self.begin = begin_coordinate
        self.end = end_coordinate
        self.image = pygame.Surface((self.end - self.begin, 200))
        self.image.fill('Green')
        self.rect = self.image.get_rect(topleft=(self.begin, height))
        self.height = height

    def get_center(self):
        return self.rect.center
    def get_height(self):
        return self.height
    def update(self,xmap):
        self.rect.x = self.begin - xmap


class Enemy(pygame.sprite.Sprite):
    def __init__(self, spawn_x, min_x,max_x, type='big', height=400):
        super().__init__()
        if type == 'big':
            self.image = pygame.Surface((25, 50))
            self.image.fill('Blue')
        elif type == 'small':
            self.image = pygame.Surface((25, 25))
            self.image.fill('Pink')
        self.rect = self.image.get_rect(bottomleft=(spawn_x, height))

        self.min_x = min_x
        self.max_x = max_x
        self.moving_side = 1
        self.x_map = 0
        # x_pos is the theorical position, whithout considering the map movement
        self.x_pos = spawn_x

    def moving(self):
        if self.rect.left< self.min_x-self.x_map:
            self.moving_side = 1
        if self.rect.right> self.max_x-self.x_map:
            self.moving_side = -1
        self.x_pos += self.moving_side* 2
        self.rect.x = self.x_pos - self.x_map
    def update(self, x_map):
        self.x_map = x_map
        self.moving()
