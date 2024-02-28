import pygame
from sys import exit

from modules import sprites

# initialization
pygame.init()
screen = pygame.display.set_mode((1100,600))
pygame.display.set_caption("MarHess")
clock = pygame.time.Clock()
game_active = False

# importing font
text_font = pygame.font.Font('font/SuperMario256.ttf', 100)

# creating text surfaces
title_surf = text_font.render("MarHess",True, 'Red')
title_rect = title_surf.get_rect(center=(550,100))

# player initialization
player = pygame.sprite.GroupSingle()

# moving map
x_map = 0
#creating map
map_group = pygame.sprite.Group()
map_group.add(sprites.Map(100, 400))
map_group.add(sprites.Map(500, 900))
map_group.add(sprites.Map(1100, 1300,500))
map_group.add(sprites.Map(1400, 1900,300))

# creating enemy group and placing some enemys
enemy_group = pygame.sprite.Group()
enemy_group.add(sprites.Enemy(1150, 1100,1300,500))
enemy_group.add(sprites.Enemy(1500, 1400,1900,300))

while True:
    # events loop
    for event in pygame.event.get():
        # close window when asked
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #actions if a party is playing, for timers
        if game_active:
            pass
        # else if space is pressed, actions to start a new party
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.add(sprites.Player())
            game_active = True

    # actions if a party is playing
    if game_active:
        screen.fill('Grey')

        # Map
        map_group.draw(screen)
        map_group.update(x_map)

        # enemy
        enemy_group.draw(screen)
        enemy_group.update(x_map)

        # player
        player.draw(screen)
        collide_map = pygame.sprite.spritecollide(player.sprite, map_group, False)
        if collide_map:
            x_map, game_active = player.sprite.update(collide_map[0])
        else:
            x_map, game_active = player.sprite.update(collide_map)

        if game_active and pygame.sprite.spritecollide(player.sprite, enemy_group, False):
            game_active = False

    # actions if we are in the menu
    else:
        screen.fill((94, 129, 162))
        screen.blit(title_surf, title_rect)


    # update the screen and set 60 frame per seconds
    pygame.display.update()
    clock.tick(60)