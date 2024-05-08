# file containing the sprites: Player, Map, Enemy

import pygame

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


