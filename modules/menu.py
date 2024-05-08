import pygame

WIDTH = 1100
LENGTH = 600

def Menu():
    button_group = pygame.sprite.Group()
    button_group.add(Button("Intro", WIDTH // 2, 200, 50, 200))
    button_group.add(Button("Level 1", WIDTH//2, 300, 50, 200))
    button_group.add(Button("Level 2", WIDTH // 2, 400, 50, 200))
    button_group.add(Button("Level 3", WIDTH // 2, 500, 50, 200))
    '''
    button_group.add(Button("Start", 475, 625, 300, 70, 'red'))
    button_group.add(Button("Start", 475, 625, 400, 70, 'green'))
    button_group.add(Button("Start", 475, 625, 500, 70, 'purple'))
    '''
    return button_group


class Button(pygame.sprite.Sprite):
    def __init__(self, display_txt: str, x, y, height, width, bg_color='green', text_color='red'):
        super().__init__()
        self.display_txt = display_txt

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.bg_color = bg_color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect(center=(x, y))

        self.font = pygame.font.Font('font/SuperMario256.ttf', 40)
        self.text_surface = self.font.render(display_txt, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def update(self, screen):
        # Draw the background rectangle
        screen.blit( self.image, self.rect)

        # Draw the text on top of the background rectangle
        screen.blit(self.text_surface, self.text_rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            match self.display_txt:
                case 'Intro':
                    return 0
                case 'Level 1':
                    return 1
                case 'Level 2':
                    return 2
                case 'Level 3':
                    return 3
