# file assisting the main.py file
import pygame

# the goal of those two functions is to outine the text, we used it for the game over text
# it comes from https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame
# it's for aestetic use
_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor=pygame.Color('dodgerblue'), ocolor=(255, 255, 255), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


# the rest of the code is made by us

# importing font
pygame.font.init()
mario_text_font = pygame.font.Font('font/SuperMario256.ttf', 130)


class Text(pygame.sprite.Sprite):
    def __init__(self, utilitie):
        pygame.sprite.Sprite.__init__(self)
        if utilitie == 'title':
            self.image = render("MarHess", mario_text_font, 'red', 'white', 6) # render an outlined text
            self.rect = self.image.get_rect(center=(550,150))
        elif utilitie == 'over':
            # for the game over
            self.image = render("Game Over", mario_text_font, 'white', 'black', 6) # render an outlined text
            self.rect = self.image.get_rect(center = (1100 // 2, 600 // 2))  # create a centered rectangle

def title_text():
    title_text = Text('title')
    group = pygame.sprite.GroupSingle()
    group.add(title_text)
    return group

def gameOver_text():
    title_text = Text('over')
    group = pygame.sprite.GroupSingle()
    group.add(title_text)
    return group
