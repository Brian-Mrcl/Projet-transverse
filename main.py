import pygame
from sys import exit

from modules import sprites
from modules import levels

# initialization
pygame.init()
screen = pygame.display.set_mode((1100,600), flags= pygame.RESIZABLE)
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

level = 1

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
            if level == 1:
                map_group, enemy_group = levels.level1()
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

        if game_active:
            enemy_collide = pygame.sprite.spritecollide(player.sprite, enemy_group, False)
            if enemy_collide:
                if player.sprite.get_bottom() <= enemy_collide[0].get_top()+20:
                    enemy_collide[0].kill()
                    player.sprite.forced_jump()
                else:
                    game_active = False

        if not game_active:
            map_group.empty()
            enemy_group.empty()
    # actions if we are in the menu
    else:
        screen.fill((94, 129, 162))
        screen.blit(title_surf, title_rect)


    # update the screen and set 60 frame per seconds
    pygame.display.update()
    clock.tick(60)