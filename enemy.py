import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img)
        self.img = img
        self.rect = self.image.get_rect()

        self.rect.left = x
        self.rect.top = y

        # Movement
        self.move_l = 0
        self.move_r = 0
        self.move_d = 0
        self.move_u = 0


    def move_left(self):
        self.move_l = -5


    def move_right(self):
        self.move_r = 5


    def move_left_off(self):
        self.move_l = 0


    def move_right_off(self):
        self.move_r = 0


    def reposition(self):
        self.rect.left += self.move_l + self.move_r
        self.rect.top += self.move_u + self.move_d


    def set_image(self, img):
        self.image = pygame.image.load(img)


    def get_initial_image(self):
        return self.img


    def display(self, dsp_surface):
        dsp_surface.blit(self.image, (self.rect.left, self.rect.top))