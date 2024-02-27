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

while True:
    # events loop
    for event in pygame.event.get():
        # close window when asked
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #actions if a party is playing, for timers
        if game_active:
            print("Playing")
        # else if space is pressed, actions to start a new party
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True

    # actions if a party is playing
    if game_active:
        screen.fill((255, 255, 255))
    # actions if we are in the menu
    else:
        screen.fill((94, 129, 162))
        screen.blit(title_surf, title_rect)


    # update the screen and set 60 frame per seconds
    pygame.display.update()
    clock.tick(60)