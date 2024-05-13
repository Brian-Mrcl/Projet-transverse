import pygame
import math
from modules import functions

u = 50
g = 9.8


def calculate_bullets_position(angle_rad, vitesse_initiale, temps, gravite=-9.81):
    x = vitesse_initiale * math.cos(angle_rad) * temps
    y = vitesse_initiale * math.sin(angle_rad) * temps - 0.5 * gravite * temps ** 2
    return x, y

class Bullet(pygame.sprite.Sprite) :
    def __init__(self, player, shift_map):     #on a récupéré le player grâce au self dans la classe player sur prjectiles
        super().__init__() #super class
        self.velocity = 5
        self.player = player
        self.image = pygame.image.load("graphics/projectile.png")
        self.image = pygame.transform.scale(self.image, (50, 50)) #changer la taille du projectile
        self.rect = self.image.get_rect() # avoir les coordonnées du projectile
        self.rect.y = player.rect.y + 20
        self.origin_image = self.image  # car quand il tourne on va modifier l'image
        self.angle = 0 # l'angle pour faire tourner le projectile


    def rotate(self):
        #faire tourner le projectile
        self.angle += 5
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center) # une rotation par rapport au centre car sinon sautillment car tout les spites sont représenté avec un rectangle

    def update(self, shift_map):
        # Mettre à jour les coordonnées du projectile
        self.rect.x = self.x - shift_map
        self.rect.y = self.y

        # # Condition pour supprimer le projectile s'il est en dehors de l'écran
        # if self.rect.x > 1080:
        #     self.kill()

        #if self.rect.y > 600:  # Taille de l'écran en y
            #self.kill()


    ##### NEEEEEEEEEEEEEEEEEEEEEEEWWWWWWWWWWWWWWWWW #####
        if self.x >= self.range:
            self.dx = 0
        self.x += self.dx
        self.ch = self.getProjectilePos(self.x - self.origin[0])

        self.path.append((self.x, self.y - abs(self.ch)))
        self.path = self.path[-50:]

        self.x,self.y = self.path[-1]

    def timeOfFlight(self):
        return round((2 * self.u * math.sin(self.theta)) / g, 2)

    def getRange(self):
        range_ = ((self.u ** 2) * 2 * math.sin(self.theta) * math.cos(self.theta)) / g
        return round(range_, 2)

    def getMaxHeight(self):
        h = ((self.u ** 2) * (math.sin(self.theta)) ** 2) / (2 * g)
        return round(h, 2)

    def getTrajectory(self):
        return round(g / (2 * (self.u ** 2) * (math.cos(self.theta) ** 2)), 4)

    def getProjectilePos(self, x):
        return x * math.tan(self.theta) - self.f * x ** 2










