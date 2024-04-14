# file containing the sprites: Player, Map, Enemy

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.import_image()
        self.anim_index = 0
        self.in_walk = False
        self.image = self.stand_img

        self.rect = self.image.get_rect(midbottom=(550,400))

        self.speed = 5
        self.xmap = 0
        self.smooth_cam = 5
        self.gravity = 0
        self.game_active =1

        self.wall_shift = 0
        self.wall_shift_to_left = bool

        self.cheat_mode = False

    def import_image(self):
        # one pixel is 3 pixel *3 ratio
        ratio = 3

        self.stand_img = pygame.transform.scale(pygame.image.load("graphics/owl/standing_23-31.png").convert_alpha(),
                                                (23 * ratio, 31 * ratio))

        self.jump_imgs = [0, 0]
        self.jump_imgs[0] = pygame.transform.scale(pygame.image.load("graphics/owl/jump1_23-31.png").convert_alpha(),
                                                   (23 * ratio, 31 * ratio))
        self.jump_imgs[1] = pygame.transform.scale(pygame.image.load("graphics/owl/jump2_23-31.png").convert_alpha(),
                                                   (23 * ratio, 31 * ratio))

        self.wall_right_img = pygame.transform.scale(pygame.image.load("graphics/owl/wall_23-31.png").convert_alpha(),
                                                     (23 * ratio, 31 * ratio))
        self.wall_left_img = pygame.transform.flip(self.wall_right_img, True, False)


        self.aside_right_imgs = [0, 0]
        self.aside_right_imgs[0] = pygame.transform.scale(
            pygame.image.load("graphics/owl/aside1_23-31.png").convert_alpha(), (23 * ratio, 31 * ratio))
        self.aside_right_imgs[1] = pygame.transform.scale(
            pygame.image.load("graphics/owl/aside2_23-31.png").convert_alpha(), (23 * ratio, 31 * ratio))
        self.aside_left_imgs = [0, 0]
        self.aside_left_imgs[0] = pygame.transform.flip(self.aside_right_imgs[0], True, False)
        self.aside_left_imgs[1] = pygame.transform.flip(self.aside_right_imgs[1], True, False)

        self.walk_imgs = [0, 0]
        self.walk_imgs[0] = pygame.transform.scale(pygame.image.load("graphics/owl/walk1_23-31.png").convert_alpha(),
                                                   (23 * ratio, 31 * ratio))
        self.walk_imgs[1] = pygame.transform.scale(pygame.image.load("graphics/owl/walk2_23-31.png").convert_alpha(),
                                                   (23 * ratio, 31 * ratio))



    def jumping(self):
        # if space is pressed
        if self.pressed_keys['space']:
            # if we touch the floor and not touch a wall
            if self.can_moove['down'] == False and not self.can_moove['left'] == False and not self.can_moove['right'] == False:
                self.gravity = -20
            # if we touch a wall on the left
            elif self.can_moove['left'] == False:
                self.wall_shift = 16
                self.wall_shift_to_left = False
            # if we touch a wall on the right
            elif self.can_moove['right'] == False:
                self.wall_shift = 16
                self.wall_shift_to_left = True
        # if we are doing a wall jump
        if self.wall_shift:
            if self.wall_shift_to_left:
                # only if there's nothing on our left
                if self.can_moove['left'] == True:
                    self.rect.x -= 5
                    self.wall_shift -= 1
                else:
                    self.wall_shift = 0
            else:
                # only if there's nothing on our right
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
        self.in_walk = False
        if self.pressed_keys['left'] and self.can_moove['left'] and not(self.wall_shift and self.wall_shift_to_left):
            self.in_walk = True
            if self.rect.x - self.speed <= 450:
                if self.smooth_cam:
                    self.smooth_cam -= 1
                    self.xmap -= 3
                    self.rect.x -=2
                else:
                    if self.xmap>-300:
                        self.xmap -= self.speed
            else:
                self.smooth_cam = self.speed
                self.rect.x -= self.speed
        if self.pressed_keys['right'] and self.can_moove['right'] and not(self.wall_shift and not self.wall_shift_to_left):
            if self.in_walk:self.in_walk = False
            else: self.in_walk = True
            if self.rect.x + self.speed >= 600:
                self.xmap += self.speed
            else:
                self.rect.x += self.speed

    def moving_collision(self):
        # finding if the player can move in each direction based on the collisions
        self.can_moove = {'up':True, 'down':True, 'left':True, 'right': True}
        self.index_map_down = 0
        i=0

        for collide_map in self.collide_list:
            # if we are over the map item
            if self.rect.bottom <= collide_map.get_height() + 30:
                # death by fall
                if self.gravity > 28:
                    self.destroy()
                self.rect.bottom = collide_map.get_height() + 1
                self.can_moove['down'] = False
                self.index_map_down = i
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
            i+=1

    def pressed_input(self):
        keys = pygame.key.get_pressed()
        self.pressed_keys = {'left': False, 'right': False, 'space': False}

        if not self.wall_shift and (keys[pygame.K_LEFT] or keys[pygame.K_q]):
            self.pressed_keys['left'] = True
        if not self.wall_shift and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.pressed_keys['right'] = True
        if keys[pygame.K_SPACE]:
            self.pressed_keys['space'] = True
    def cheat(self):
        if self.cheat_mode:
            self.cheat_mode = False
            self.speed = 5
            self.rect.y = 200
        else:
            self.cheat_mode = True
            self.rect.y = 100
            self.speed = 20

    def animation(self):
        ratio = 3
        # if no collision
        if not self.collide_list:
            if self.gravity<0:
                self.anim_index += 2
                if self.anim_index >= 20:
                    self.anim_index =0
                self.image = self.jump_imgs[self.anim_index // 10]
            else:
                self.image = self.jump_imgs[0]
        else:
            if self.in_walk:
                self.anim_index += 1
                if self.anim_index >= 20:
                    self.anim_index = 0
                self.image = self.walk_imgs[self.anim_index // 10]
            elif not self.can_moove['right']:
                self.image = self.wall_right_img
            elif not self.can_moove['left']:
                self.image = self.wall_left_img
            elif not self.can_moove['down'] and (self.collide_list[self.index_map_down].get_right() < self.rect.centerx  or self.collide_list[self.index_map_down].get_left() > self.rect.centerx):
                # moving index for animation
                self.anim_index += 2
                if self.anim_index >= 20:
                    self.anim_index = 0
                # animating aside of a platform
                if self.collide_list[self.index_map_down].get_right() < self.rect.centerx:
                    self.image = self.aside_right_imgs[self.anim_index // 10]
                else:
                    self.image = self.aside_left_imgs[self.anim_index // 10]
            else:
                self.image = self.stand_img

    def update(self,collide_map):
        self.collide_list = collide_map

        self.pressed_input()
        if not self.cheat_mode:
            self.moving_collision()

            self.jumping()
            self.apply_gravity()

        self.walking()

        self.animation()
        return (self.xmap, self.game_active)

    #getter and external actions
    def colliding_enemy(self, enemy_collide):
        if enemy_collide:
            if self.rect.bottom <= enemy_collide[0].get_top() + 20:
                enemy_collide[0].kill()
                if self.pressed_keys['space']:
                    self.forced_jump()
                else:
                    self.rebond()
            else:
                self.game_active = 0
        return self.game_active
    def get_bottom(self):
        return self.rect.bottom
    def forced_jump(self):
        # applyed when you kill an enemy
        self.gravity=-20
    def rebond(self):
        # applied when you kill an enemy
        self.gravity=-10

class Map(pygame.sprite.Sprite):
    def __init__(self, begin_coordinate, end_coordinate, height=400, depth = 450):
        super().__init__()
        self.begin = begin_coordinate
        self.end = end_coordinate

        #self.image = pygame.Surface((self.end - self.begin, 400))
        #self.image.fill('Green')
        self.full_ground = pygame.image.load("graphics/ground.png")
        self.image = self.full_ground.subsurface((1, 0, self.end - self.begin, depth))

        self.rect = self.image.get_rect(topleft=(self.begin, height))
        self.height = height

    def get_center(self): return self.rect.center
    def get_height(self): return self.height

    def get_bottom(self): return self.rect.bottom

    def get_left(self): return self.rect.left

    def get_right(self): return self.rect.right

    def update(self,xmap):
        self.rect.x = self.begin - xmap

class Decoration(pygame.sprite.Sprite):
    def __init__(self, begin, type, height=400,scale=1,flow_end =0):
        super().__init__()
        self.height = height
        self.begin = begin
        self.flow_end = flow_end
        if type == 'mountain':
            pass
        elif type == 'tree':
            pass
        elif type == 'castle':
            pass
        elif type == 'tuto_display':
            self.image = pygame.image.load("graphics/tuto/tuto_display.png").convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, scale)
            self.rect = self.image.get_rect(topleft=(begin, height))
        elif type == 'bar':
            self.image = pygame.Surface((1, scale))
            self.image.fill('blue')
            self.rect = self.image.get_rect(topleft=(begin, height))
        elif 'text_' in type:
            clean_text_font = pygame.font.Font('font/pixeled.ttf', int(scale))
            self.image = clean_text_font.render(type[5:], True, '#424340')
            self.rect = self.image.get_rect()

    def update(self, xmap):
        current_x = self.begin - xmap
        if self.flow_end==0:
            self.rect.x = current_x
        else:
            if current_x < 1100 and current_x-self.flow_end >0:
                self.rect.center = (1100//2, self.height)
            else: self.rect.x=1200

class Enemy(pygame.sprite.Sprite):
    def __init__(self, min_x,max_x, type='big', level = 0, height=400):
        super().__init__()
        self.min_x = min_x
        self.max_x = max_x

        self.moving_side = 1

        self.x_map = 0

        self.level = level

        self.import_img(type)

        self.rect = self.image.get_rect(bottomleft=((min_x+max_x)//2, height))


        # x_pos is the theorical position, without considering the map movement
        self.x_pos = (min_x+max_x)//2
    def import_img(self, type):
        match self.level:
            case 0:
                match type:
                    case 'big':
                        self.image = pygame.image.load('graphics/enemies/intro/computer-192_191.png').convert_alpha()
                        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
                    case _:
                        raise ValueError('Unrecognized enemy type')
            case 1:
                match type:
                    case 'big':
                        self.image = pygame.image.load('graphics/enemies/computer/computer-192_191.png').convert_alpha()
                        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
                    case 'small':
                        self.image = pygame.image.load('graphics/enemies/computer/book-229_199.png').convert_alpha()
                        self.image = pygame.transform.rotozoom(self.image, 0, 0.2)
                    case 'fly':
                        self.image = pygame.image.load('graphics/enemies/computer/folder-104_86.png').convert_alpha()
                        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
                    case _:
                        raise ValueError('Unrecognized enemy type')
            case 2:
                match type:
                    case 'big':
                        self.image = pygame.image.load('graphics/enemies/math/2-216_324.png').convert_alpha()
                        self.image = pygame.transform.rotozoom(self.image, 0, 0.25)
                    case 'small':
                        self.image = pygame.image.load('graphics/enemies/math/sum-143_157.png').convert_alpha()
                        self.image = pygame.transform.rotozoom(self.image, 0, 0.2)
                    case 'fly':
                        self.image = pygame.image.load('graphics/enemies/math/pi-322_266.png').convert_alpha()
                        self.image = pygame.transform.rotozoom(self.image, 0, 0.2)
                    case _:
                        raise ValueError('Unrecognized enemy type')
            case 3:
                match type:
                    case 'big':
                        self.image = pygame.image.load('graphics/enemies/physic/dna-67_143.png').convert_alpha()
                        self.image = pygame.transform.rotozoom(self.image, 0, 0.6)
                    case 'small':
                        self.image = pygame.image.load('graphics/enemies/physic/bottle-58_66.png').convert_alpha()
                        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
                    case 'fly':
                        self.image = pygame.image.load('graphics/enemies/physic/atom-352_396.png').convert_alpha()
                        self.image = pygame.transform.rotozoom(self.image, 0, 0.2)
                    case _:
                        raise ValueError('Unrecognized enemy type')
            case _:
                raise Exception('trying to import enemy of non-existing level')



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

class End_point(pygame.sprite.Sprite):
    def __init__(self, xleft, ybottom):
        super().__init__()
        self.xleft = xleft
        self.ybottom = ybottom

        self.image = pygame.image.load("graphics/endPoint.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.rect = self.image.get_rect(bottomleft=(xleft,ybottom))

        self.anim_state = 1

    def animation(self):
        self.rect.y += self.anim_state
        if self.rect.bottom - self.ybottom == 15 or self.rect.bottom - self.ybottom == -15:
            self.anim_state *=-1

    def update(self, xmap):
        self.rect.x = self.xleft - xmap
        self.animation()


class Button(pygame.sprite.Sprite):
    def __init__(self, text, height, width):
        super().__init__()
        self.text = text
        self.height = height
        self.width = width

    def get_bottom(self):
        return self.rect.bottom
