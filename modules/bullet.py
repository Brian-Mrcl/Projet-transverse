##### new from git #####
import pygame
import math

g = 9.8
radius = 160

def radian_convert(theta):
    return theta * math.pi / 180

def degrees_convert(theta):
    return theta * 180 / math.pi

def get_gradient(p1, p2):
    if p1[0] == p2[0]:
        m = radian_convert(90)
    else:
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    return m

def get_angleFromGradient(gradient):
    return math.atan(gradient)

def get_angle(pos, origin):
    m = get_gradient(pos, origin)
    thetaRad = get_angleFromGradient(m)
    theta = round(degrees_convert(thetaRad), 2)
    return theta

def get_posOnCircumeference(theta, origin):
    theta = radian_convert(theta)
    x = origin[0] + radius * math.cos(theta)
    y = origin[1] + radius * math.sin(theta)
    return (x, y)



class Bullet(pygame.sprite.Sprite):
    def __init__(self, u, theta, screen, player_sp, shift_map):
        super(Bullet, self).__init__()
        self.win = screen
        self.map_origin = shift_map

        self.u = u
        self.theta = radian_convert(abs(theta))
        self.origin = player_sp.rect.center
        self.x, self.y = self.origin

        self.ch = 0
        self.dx = 6

        self.f = self.get_traj()
        self.range = self.x + abs(self.get_range())

        self.path = []

        self.image = pygame.image.load("graphics/projectile.png")
        self.image = pygame.transform.scale(self.image, (50, 50))  # changer la taille du projectile
        self.rect = self.image.get_rect()  # avoir les coordonnées du projectile
        self.origin_image = self.image  # car quand il tourne on va modifier l'image
        self.angle = 0  # l'angle pour faire tourner le projectile


    def get_range(self):
        range_ = ((self.u ** 2) * 2 * math.sin(self.theta) * math.cos(self.theta)) / g
        return round(range_, 2)

    def get_traj(self):
        return round(g / (2 * (self.u ** 2) * (math.cos(self.theta) ** 2)), 4)

    def getProjectilePos(self, x):
        return x * math.tan(self.theta) - self.f * x ** 2

    def rotate(self):
        # faire tourner le projectile
        self.angle += 5
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(
            center=self.rect.center)  # une rotation par rapport au centre car sinon sautillment car tout les spites sont représenté avec un rectangle

    def update(self, map_shift):

        #To stop the projectle before x = 0
        #if self.x >= self.range:
            #self.dx = 0
        self.x += self.dx
        self.ch = self.getProjectilePos(self.x - self.origin[0])

        #self.path.append((self.x, self.y - abs(self.ch)))
        self.path.append((self.x, self.y - self.ch))
        self.path = self.path[-50:]

        # display the stonne
        self.rotate()
        x_display = self.path[-1][0] + self.map_origin - map_shift
        self.rect.center = x_display, self.path[-1][1]
        self.win.blit(self.image,self.rect)

        # display the points following the trajectory
        for pos in self.path[:-1:5]:
            x_display = pos[0] + self.map_origin - map_shift
            pygame.draw.circle(self.win, 'white', (x_display, pos[1]), 1)

        if self.rect.top > 600 or self.rect.left > 1100 or self.rect.right < 0: #delete projectiles outside the screen area
            self.kill()