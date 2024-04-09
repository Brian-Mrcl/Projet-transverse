import pygame
from sys import exit

from modules import sprites
from modules import levels
from modules import menu

# initialization
pygame.init()
screen = pygame.display.set_mode((1100, 600), flags=pygame.RESIZABLE)
pygame.display.set_caption("MarHess")
clock = pygame.time.Clock()
game_state = 0
# (GAMES STATES: -1: menu;   0: game over;    1: game active)

# importing font
text_font = pygame.font.Font('font/SuperMario256.ttf', 100)

# creating text surfaces
title_surf = text_font.render("MarHess", True, 'Red')
title_rect = title_surf.get_rect(center=(550, 100))

# player initialization
player = pygame.sprite.GroupSingle()

# moving map
x_map = 0

level = 1

sky_surface = pygame.image.load('graphics/sky.png').convert()

# menu
button_group = menu.Menu()

while True:
    # events loop
    for event in pygame.event.get():
        # close window when asked
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # actions if a party is playing, for timers
        if game_state:
            pass
        # else if space is pressed, actions to start a new party
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.add(sprites.Player())
            if level == 1:
                map_group, enemy_group = levels.level1()
            game_state = 1

    # actions if a party is playing
    if game_state == 1:
        # Putting the sky
        screen.blit(sky_surface, (0, 0))

        # Map
        map_group.draw(screen)
        map_group.update(x_map)

        # enemy
        enemy_group.draw(screen)
        enemy_group.update(x_map)

        # player
        player.draw(screen)
        collide_map = pygame.sprite.spritecollide(player.sprite, map_group, False)
        x_map, game_state = player.sprite.update(collide_map)

        if game_state == 1:
            enemy_collide = pygame.sprite.spritecollide(player.sprite, enemy_group, False)
            if enemy_collide:
                if player.sprite.get_bottom() <= enemy_collide[0].get_top() + 20:
                    enemy_collide[0].kill()
                    if pygame.key.get_pressed()[pygame.K_SPACE]:
                        player.sprite.forced_jump()
                    else:
                        player.sprite.rebond()
                else:
                    game_state = 0

        if game_state != 1:
            player.sprite.kill()
            map_group.empty()
            enemy_group.empty()

    elif game_state == 0:
        font = pygame.font.Font('font/SuperMario256.ttf', 150)  # the police character for the word game over
        game_over_text = font.render("Game Over", True, (255, 0, 0))

        text_dim = game_over_text.get_rect()  # dimension of the text
        text_dim.center = (1100 // 2, 600 // 2)  # center of the image going modifying text_dim
        screen.blit(game_over_text, text_dim)


    # actions if we are in the menu
    elif game_state == -1:
        screen.fill('Dark grey')
        button_group.draw(screen)
        button_group.update(x_map)
        for event in pygame.event.get():
            # close window when asked
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and button_group.typeB == "Start" and button_group.colliderect(
                    pygame.MOUSEMOTION):
                game_state = 0

    # update the screen and set 60 frame per seconds
    pygame.display.update()
    clock.tick(60)
