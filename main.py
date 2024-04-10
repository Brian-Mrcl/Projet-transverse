import pygame
from sys import exit

from modules import sprites
from modules import levels
from modules import functions

# initialization
pygame.init()
screen = pygame.display.set_mode((1100,600))
pygame.display.set_caption("MarHess")
clock = pygame.time.Clock()

# (GAMES STATES: -1: menu;   0: game over;    1: game active)
game_state = 0

# importing fonts
mario_text_font = pygame.font.Font('font/SuperMario256.ttf', 100)

# creating text surfaces
title_surf = mario_text_font.render("MarHess", True, 'Red')
title_rect = title_surf.get_rect(center=(550,100))

# player initialization
player = pygame.sprite.GroupSingle()

# moving map
x_map = 0

level = 0
achieved_level = [0,0,0,0]

sky_surface = pygame.transform.scale(pygame.image.load('graphics/sky.png').convert(), (1100, 600))

while True:
    # events loop
    for event in pygame.event.get():
        # close window when asked
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #actions if a party is playing, for timers
        if game_state:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        # else if space is pressed, actions to start a new party
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.add(sprites.Player())
                if level == 0:
                    map_group, enemy_group, background_group, end_point = levels.intro()
                if level == 1:
                    map_group, enemy_group, background_group, end_point = levels.level1()
                game_state = 1
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # actions if a party is playing
    if game_state == 1:
        #pygame.mouse.set_visible(False)

        # Putting the sky
        screen.blit(sky_surface, (0,0))

        # Background
        background_group.draw(screen)
        background_group.update(x_map)

        # Map
        map_group.draw(screen)
        map_group.update(x_map)

        # enemy
        end_point.draw(screen)
        end_point.update(x_map)

        # End Point
        enemy_group.draw(screen)
        enemy_group.update(x_map)

        # player
        player.draw(screen)
        # Updating the player, giving him the collision with the map, he return the shift of the map du to his movement and if he's dead
        collide_map = pygame.sprite.spritecollide(player.sprite, map_group, False)
        x_map, game_state = player.sprite.update(collide_map)
        # updating the collisions of the player with enemys, return if he died
        enemy_collide = pygame.sprite.spritecollide(player.sprite, enemy_group, False)
        if game_state == 1:
            game_state = player.sprite.colliding_enemy(enemy_collide)


        if game_state != 1:
            player.sprite.kill()
            map_group.empty()
            enemy_group.empty()

    elif game_state == 0:
        pygame.mouse.set_visible(True)
        font = pygame.font.Font('font/SuperMario256.ttf', 150)  # the police chracter for the word game over
        game_over_text = font.render("Game Over", True, (255,0,0))

        text_dim = game_over_text.get_rect()  # dimension of the text
        text_dim.center = (1100 // 2, 600 // 2)  # center of the image going modifying text_dim
        screen.blit(game_over_text, text_dim)


    # actions if we are in the menu
    elif game_state == -1:
        pygame.mouse.set_visible(True)
        screen.fill((94, 129, 162))
        screen.blit(title_surf, title_rect)


    # update the screen and set 60 frame per seconds
    pygame.display.update()
    clock.tick(60)
