import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #one pixel is 3 pixel *3 ratio
        ratio = 3

        self.stand_img = pygame.transform.scale(pygame.image.load("graphics/owl/standing_23-30.png").convert_alpha(),(23 * ratio, 30 * ratio))

        self.jump_imgs = [0,0]
        self.jump_imgs[0] = pygame.transform.scale(pygame.image.load("graphics/owl/jump1_23-30.png").convert_alpha(), (23*ratio,30*ratio))
        self.jump_imgs[1] = pygame.transform.scale(pygame.image.load("graphics/owl/jump2_27-30.png").convert_alpha(),(27*ratio, 30*ratio))
        self.jump_img_i = 0

        self.image = self.stand_img
        self.rect = self.image.get_rect(midbottom=(550,400))

        self.xmap = 0
        self.smooth_cam = 5
        self.gravity = 0
        self.game_active =1

        self.wall_shift = 0
        self.wall_shift_to_left = bool

    def jumping(self):
        if self.pressed_keys['space']:
            if self.can_moove['down'] == False:
                self.gravity = -20
            elif self.can_moove['left'] == False:
                self.wall_shift = 16
                self.wall_shift_to_left = False
            elif self.can_moove['right'] == False:
                self.wall_shift = 16
                self.wall_shift_to_left = True

        if self.wall_shift:
            if self.wall_shift_to_left:
                if self.can_moove['left'] == True:
                    self.rect.x -= 5
                    self.wall_shift -= 1
                else:
                    self.wall_shift = 0
            else:
                if self.can_moove['right'] == True:
                    self.rect.x += 5
                    self.wall_shift -= 1
                else:
                    self.wall_shift = 0

    def apply_gravity(self):
        if self.can_moove['left'] == False or self.can_moove['right'] == False:
            self.gravity = 3

        if self.wall_shift == 15:
            self.gravity = -20

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

        # dying if we are under the map
        if self.rect.top > 600:
            self.destroy()
            return 0

    def destroy(self):
        self.game_active = 0

    def walking(self):
        keys = pygame.key.get_pressed()
        if self.pressed_keys['left'] and self.can_moove['left'] and not(self.wall_shift and self.wall_shift_to_left):
            if self.rect.x -5 <= 450:
                if self.smooth_cam:
                    self.smooth_cam -= 1
                    self.xmap -= 3
                    self.rect.x -=2
                else:
                    if self.xmap>-300:
                        self.xmap -= 5

            else:
                self.smooth_cam = 5
                self.rect.x -= 5
        if self.pressed_keys['right'] and self.can_moove['right'] and not(self.wall_shift and not self.wall_shift_to_left):
            if self.rect.x + 5 >= 650:
                self.xmap += 5
            else:
                self.rect.x += 5

    def moving_collision(self):
        # finding if the player can move in each direction based on the collisions
        self.can_moove = {'up':True, 'down':True, 'left':True, 'right': True}

        for collide_map in self.collide_list:
            # if we are over the map item
            if self.rect.bottom <= collide_map.get_height() + 30:
                # death by fall
                if self.gravity > 28:
                    self.destroy()
                self.rect.bottom = collide_map.get_height() + 1
                self.can_moove['down'] = False
            # if the element is over
            elif self.rect.bottom >= collide_map.get_bottom() - 10 and not( self.rect.right < collide_map.get_left() +5 or self.rect.left > collide_map.get_right() - 5):
                self.can_moove['up'] = False
            # the two last are for an element on right the on the left
            elif self.rect.center[0] < collide_map.get_center()[0]:
                self.can_moove['right'] = False
                self.rect.right = collide_map.get_left()+1
            else:
                self.can_moove['left'] = False
                self.rect.left = collide_map.get_right() - 1

    def pressed_input(self):
        keys = pygame.key.get_pressed()
        self.pressed_keys = {'left': False, 'right': False, 'space': False}

        if not self.wall_shift and (keys[pygame.K_LEFT] or keys[pygame.K_q]):
            self.pressed_keys['left'] = True
        if not self.wall_shift and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.pressed_keys['right'] = True
        if keys[pygame.K_SPACE]:
            self.pressed_keys['space'] = True

    def animation(self):
        ratio = 3
        # if no collision
        if not self.collide_list:
            if self.gravity<0:
                self.jump_img_i += 2
                if self.jump_img_i == 20:
                    self.jump_img_i =0
                self.image = self.jump_imgs[self.jump_img_i//10]
            else:
                self.image = self.jump_imgs[0]
        else:
            self.image = self.stand_img

    def update(self,collide_map):
        self.collide_list = collide_map

        self.pressed_input()
        self.moving_collision()

        self.jumping()
        self.apply_gravity()

        self.walking()

        self.animation()
        return (self.xmap, self.game_active)

    #getter and external actions
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

        #self.image = pygame.Surface((self.end - self.begin, 400))
        #self.image.fill('Green')
        self.full_ground = pygame.image.load("graphics/ground.png")
        self.image = self.full_ground.subsurface((1, 0, self.end - self.begin, 400))

        self.rect = self.image.get_rect(topleft=(self.begin, height))
        self.height = height

    def get_center(self): return self.rect.center
    def get_height(self): return self.height

    def get_bottom(self): return self.rect.bottom

    def get_left(self): return self.rect.left

    def get_right(self): return self.rect.right

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
