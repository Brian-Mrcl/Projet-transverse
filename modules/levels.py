from modules import sprites
import pygame

def level1():
    # creating map
    map_group = pygame.sprite.Group()
    map_group.add(sprites.Map(100, 400))
    map_group.add(sprites.Map(500, 900))
    map_group.add(sprites.Map(1100, 1300, 500))
    map_group.add(sprites.Map(1400, 1900, 300))
    map_group.add(sprites.Map(2000, 2500))
    map_group.add(sprites.Map(2600, 2610))

    # creating enemy group and placing some enemys
    enemy_group = pygame.sprite.Group()
    big = 'big'
    small = 'small'
    enemy_group.add(sprites.Enemy(1100, 1300, big, 500))
    enemy_group.add(sprites.Enemy(1400, 1900, small, 300))
    return map_group, enemy_group