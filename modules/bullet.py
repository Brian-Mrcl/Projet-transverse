import pygame


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
        self.position = player.rect.x + 20+shift_map
        self.rect.y = player.rect.y + 20
        self.origin_image = self.image  # car quand il tourne on va modifier l'image
        self.angle = 0 # l'angle pour faire tourner le projectile


    def rotate(self):
        #faire tourner le projectile
        self.angle += 5
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center) # une rotation par rapport au centre car sinon sautillment car tout les spites sont représenté avec un rectangle

    def update(self, shift_map):
        self.position += self.velocity
        # thanks to shift_map the bullet move also when the player move
        self.rect.x = self.position - shift_map
        self.rotate()

        # J'AI MIS CA EN COMMENTAIRE

        # #verifier si projectile est en collision avec un monstre
        # for monster in self.player.game.check_collision(self, self.player.game.all_monsters) :
        #     self.remove()
        #     #infliger des degats
        #     monster.damage(self.player.attack)



        #condition pour supp le prjectile si il est en dehors de l'ecran
        if self.rect.x > 1080 :
            self.kill()