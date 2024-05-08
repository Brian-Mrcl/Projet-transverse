import pygame
from modules import bullet

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
