# file using sprites/Map and sprites/Enemy classes to creates the different maps

from modules import sprites
import pygame


def import_level(level):
    match level:
        case 0:
            return intro(level)
        case 1:
            return level1(level)
        case 2:
            return level2(level)
        case 3:
            return level3(level)



# first level (not finish)

def intro(level):

    # creating map
    map_group = pygame.sprite.Group()
    # creating enemy group and placing some enemys
    enemy_group = pygame.sprite.Group()
    big = 'big'

    background_group = pygame.sprite.Group()
    end_point = pygame.sprite.GroupSingle()

    # big block
    bb = 200

    #first platform
    map_group.add(sprites.Map(0, 1500))

    # displaying the help
    background_group.add(sprites.Decoration(150, 'tuto_display', -10, 0.8))
    # incentive to move
    background_group.add(sprites.Decoration(300, 'text_Try to move!', 200, 20,1))

    # new platform to jump on
    map_group.add(sprites.Map(1700, 1900))
    # incentive to jump on it
    background_group.add(sprites.Decoration(1700, 'text_Now try to jump!', 150, 20, 1))
    # new platform to jump on
    map_group.add(sprites.Map(2100, 3200))

    # Explaining for enemies
    background_group.add(sprites.Decoration(2800, 'text_They\'ll kill you', 100, 20, 301))
    background_group.add(sprites.Decoration(3000, 'text_Except if you jump on them!', 150, 20, 501))
    # Enemy to face
    enemy_group.add(sprites.Enemy(2800, 3200, big))
    # Platform
    map_group.add(sprites.Map(3400, 4000))

    background_group.add(sprites.Decoration(3800, 'text_I let you discover wall jump!', 30, 20, 1))
    background_group.add(sprites.Decoration(4000, 'text_And death by fall', 60, 20, 201))
    # Platform to wall jump
    map_group.add(sprites.Map(4000, 4100,150))
    # Platforme de récéption
    map_group.add(sprites.Map(4100, 5000))

    end_point.add(sprites.End_point(4800,350))

    return map_group, enemy_group, background_group, end_point

def level1(level):

    # creating map
    map_group = pygame.sprite.Group()
    # creating enemy group and placing some enemys
    enemy_group = pygame.sprite.Group()
    big, small, fly = 'big','small','fly'

    background_group = pygame.sprite.Group()

    end_point = pygame.sprite.GroupSingle()


    # big block
    bb = 200

    map_group.add(sprites.Map(100, 400))
    map_group.add(sprites.Map(500, 1000))
    map_group.add(sprites.Map(1200, 1500, 350))

    map_group.add(sprites.Map(2050, 2400, 210))
    enemy_group.add(sprites.Enemy(1700, 2050, small,level, 350))
    map_group.add(sprites.Map(1700, 2150,350))
    map_group.add(sprites.Map(2300, 2600, 400))
    enemy_group.add(sprites.Enemy(2500, 2700, fly,level, 200))

    map_group.add(sprites.Map(2800+0.5*bb, 3000+bb, 300))
    map_group.add(sprites.Map(2700+0.5*bb, 2800+bb, 350))
    enemy_group.add(sprites.Enemy(2800+0.5*bb, 3000+bb, big,level, 300))

    map_group.add(sprites.Map(3000+2*bb, 3000 + 4*bb, 425))
    map_group.add(sprites.Map(4200 , 4500, 425))
    enemy_group.add(sprites.Enemy(3000+ 4*bb, 4200, fly, level,425))

    end_point.add(sprites.End_point(4350, 375))

    return map_group, enemy_group, background_group, end_point



# second level (not finish)
def level2(level):

    background_group = pygame.sprite.Group()

    end_point = pygame.sprite.GroupSingle()

    # creating enemy group
    enemy_group = pygame.sprite.Group()
    big, small, fly = 'big','small','fly'

    # creating map
    map_group = pygame.sprite.Group()

    # placing everything
    map_group.add(sprites.Map(100, 400))
    map_group.add(sprites.Map(500, 900))
    map_group.add(sprites.Map(700, 755, -170))
    map_group.add(sprites.Map(900, 1000, 100))
    map_group.add(sprites.Map(1100, 1300, 500))
    enemy_group.add(sprites.Enemy(1100, 1300, big,level, 500))


    map_group.add(sprites.Map(1400, 1900, 300))
    enemy_group.add(sprites.Enemy(1400, 1900, small,level, 300))
    map_group.add(sprites.Map(2000, 2500, 450))
    # the two stilts
    map_group.add(sprites.Map(2700, 2710,450))
    map_group.add(sprites.Map(2900, 2910, 500))

    map_group.add(sprites.Map(3000, 3500, 550))
    # forced jump on the fly to acceed to the platform
    enemy_group.add(sprites.Enemy(3000, 3400, fly,level,450))
    map_group.add(sprites.Map(3400, 3700, 200, 25))
    # some floating islands
    map_group.add(sprites.Map(3900, 4000, 250, 50))
    map_group.add(sprites.Map(4200, 4400, 250, 50))

    map_group.add(sprites.Map(4500, 5000))

    end_point.add(sprites.End_point(4800, 350))

    return map_group, enemy_group, background_group, end_point


def level3(level):
    background_group = pygame.sprite.Group()

    end_point = pygame.sprite.GroupSingle()

    # creating enemy group
    enemy_group = pygame.sprite.Group()
    big, small, fly = 'big', 'small', 'fly'

    # creating map
    map_group = pygame.sprite.Group()

    # placing everything
    map_group.add(sprites.Map(100, 400))
    map_group.add(sprites.Map(500, 1500))

    enemy_group.add(sprites.Enemy(100, 300, big,level,400))
    enemy_group.add(sprites.Enemy(800, 1200, small, level, 400))
    enemy_group.add(sprites.Enemy(1200, 1600, fly, level, 300))

    end_point.add(sprites.End_point(1600, 350))

    return map_group, enemy_group, background_group, end_point
