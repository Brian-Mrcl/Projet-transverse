import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1100,600))
pygame.display.set_caption("MarHess")
clock = pygame.time.Clock()
game_active = False

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
        print("Playing")
    # actions if we are in the menu
    else:
        screen.fill((94, 129, 162))


    # update the screen and set 60 frame per seconds
    pygame.display.update()
    clock.tick(60)