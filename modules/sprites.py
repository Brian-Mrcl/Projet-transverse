import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 70))
        self.image.fill('Red')
        self.rect = self.image.get_rect(midbottom=(550,400))

        self.xmap = 0
        self.smooth_cam = 5
        self.gravity = 0
        self.game_active =1

        self.wall_shift = 0
        self.wall_shift_to_left = bool

    def input_jumping(self):
        space_pressed = pygame.key.get_pressed()[pygame.K_SPACE]

        if space_pressed:
            if self.can_moove['down'] == False:
                self.gravity = -20
            elif self.can_moove['left'] == False:
                self.wall_shift = 20
                self.rect.x += 5
                self.wall_shift_to_left = False
            elif self.can_moove['right'] == False:
                self.wall_shift = 20
                self.rect.x -= 5
                self.wall_shift_to_left = True

        if self.wall_shift:
            if self.wall_shift_to_left:
                self.rect.x -= 5
                self.wall_shift -= 1
            else:
                self.rect.x += 5
                self.wall_shift -= 1


    def apply_gravity(self):
        if self.can_moove['left'] == False or self.can_moove['right'] == False:
            self.gravity = 3

        if self.gravity < 0:
            if self.can_moove['up']:
                self.rect.y += self.gravity
                self.gravity += 1
            else:
                self.gravity = 0
        else:
            if self.can_moove['down']:
                self.rect.y += self.gravity
                self.gravity += 1
            else:
                self.gravity = 0


    def destroy(self):
        self.game_active = 0

    def walking(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and self.can_moove['left'] and not(self.wall_shift and self.wall_shift_to_left):
            if self.rect.x -5 <= 450:
                if self.smooth_cam:
                    self.smooth_cam -= 1
                    self.xmap -= 3
                    self.rect.x -=2
                else:
                    self.xmap -= 5

            else:
                self.smooth_cam = 5
                self.rect.x -= 5
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.can_moove['right'] and not(self.wall_shift and not self.wall_shift_to_left):
            if self.rect.x + 5 >= 650:
                self.xmap += 5
            else:
                self.rect.x += 5

    def moving(self):
        # dying if we are under the map
        if self.rect.top > 600:
            self.destroy()
            return 0

        # finding if the player can move in each direction based on the collisions
        self.can_moove = {'up':True, 'down':True, 'left':True, 'right': True}

        for collide_map in self.collide_list:
            if collide_map:
                # if we are over the map item
                if self.rect.bottom <= collide_map.get_height() + 30:
                    # death by fall
                    if self.gravity > 28:
                        self.destroy()
                    self.rect.bottom = collide_map.get_height() + 1
                    self.can_moove['down'] = False
                # if the element is over
                elif self.rect.bottom >= collide_map.get_bottom() - 10:
                    self.can_moove['up'] = False
                # the two last are for an element on right the on the left
                elif self.rect.center < collide_map.get_center():
                    self.can_moove['right'] = False
                else:
                    self.can_moove['left'] = False


        self.input_jumping()
        self.apply_gravity()
        self.walking()

    def update(self,collide_map):
        self.collide_list = collide_map
        self.moving()
        return (self.xmap, self.game_active)
    def get_bottom(self):
        return self.rect.bottom
    def forced_jump(self):
        # applyed when you kill an enemy
        self.gravity=-20
    def rebond(self):
        # applied when you kill an enemy
        self.gravity=-10

class Map(pygame.sprite.Sprite):
    def __init__(self, begin_coordinate, end_coordinate, height=400):
        super().__init__()
        self.begin = begin_coordinate
        self.end = end_coordinate
        self.image = pygame.Surface((self.end - self.begin, 400))
        self.image.fill('Green')
        self.rect = self.image.get_rect(topleft=(self.begin, height))
        self.height = height

    def get_center(self): return self.rect.center
    def get_height(self): return self.height

    def get_bottom(self): return self.rect.bottom

    def update(self,xmap):
        self.rect.x = self.begin - xmap


class Enemy(pygame.sprite.Sprite):
    def __init__(self, min_x,max_x, type='big', height=400):
        super().__init__()
        if type == 'big':
            self.image = pygame.Surface((25, 50))
            self.image.fill('Blue')
        elif type == 'small':
            self.image = pygame.Surface((25, 25))
            self.image.fill('Pink')
        self.rect = self.image.get_rect(bottomleft=((min_x+max_x)//2, height))

        self.min_x = min_x
        self.max_x = max_x
        self.moving_side = 1
        self.x_map = 0
        # x_pos is the theorical position, without considering the map movement
        self.x_pos = (min_x+max_x)//2

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
    def get_top(self):
        return self.rect.top




class Button(pygame.sprite.Sprite):
    def __init__(self, text, height, width):
        super().__init__()
        self.text = text
        self.height = height
        self.width = width

    def get_bottom(self):
        return self.rect.bottom
