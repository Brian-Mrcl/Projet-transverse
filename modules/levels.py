from modules import sprites
import pygame


# first level (not finish)
def level1():
    # creating map
    map_group = pygame.sprite.Group()
    # creating enemy group and placing some enemys
    enemy_group = pygame.sprite.Group()
    big = 'big'
    small = 'small'
    fly = 'fly'

    background_group = pygame.sprite.Group()

    # big block
    bb = 200

    map_group.add(sprites.Map(100, 400))
    map_group.add(sprites.Map(500, 1000))
    map_group.add(sprites.Map(1200, 1500, 350))

    map_group.add(sprites.Map(2050, 2400, 210))
    enemy_group.add(sprites.Enemy(1700, 2050, small, 350))
    map_group.add(sprites.Map(1700, 2150,350))
    map_group.add(sprites.Map(2300, 2600, 400))
    enemy_group.add(sprites.Enemy(2500, 2700, fly, 200))

    map_group.add(sprites.Map(2800+0.5*bb, 3000+bb, 300))
    map_group.add(sprites.Map(2700+0.5*bb, 2800+bb, 350))
    enemy_group.add(sprites.Enemy(2800+0.5*bb, 3000+bb, big, 300))


    enemy_group.add(sprites.Enemy(5000, 130000, big, 500))
    enemy_group.add(sprites.Enemy(140000, 190000, small, 300))
    return map_group, enemy_group, background_group



# second level (not finish)
def level2():
    background_group = pygame.sprite.Group()

    # creating map
    map_group = pygame.sprite.Group()
    map_group.add(sprites.Map(100, 400))
    map_group.add(sprites.Map(500, 900))
    map_group.add(sprites.Map(700, 755, -100))
    map_group.add(sprites.Map(900, 1000, 100))
    map_group.add(sprites.Map(1100, 1300, 500))
    map_group.add(sprites.Map(1400, 1900, 300))
    map_group.add(sprites.Map(2000, 2500))
    map_group.add(sprites.Map(2700, 2710))
    map_group.add(sprites.Map(2900, 2910))
    map_group.add(sprites.Map(3000, 3500))

    # creating enemy group and placing some enemys
    enemy_group = pygame.sprite.Group()
    big = 'big'
    small = 'small'
    enemy_group.add(sprites.Enemy(1100, 1300, big, 500))
    enemy_group.add(sprites.Enemy(1400, 1900, small, 300))
    return map_group, enemy_group, background_group


