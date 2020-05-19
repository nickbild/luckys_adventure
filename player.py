import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Initialize player variables.
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()

        self.rect.left = x
        self.rect.top = y

        self.move_l = 0
        self.move_r = 0
        self.move_d = 0
        self.move_u = 0


    def move_left(self):
        self.move_l = -5


    def move_right(self):
        self.move_r = 5


    def move_up(self):
        self.move_u = -5


    def move_down(self):
        self.move_d = 5


    def move_left_off(self):
        self.move_l = 0


    def move_right_off(self):
        self.move_r = 0


    def move_up_off(self):
        self.move_u = 0


    def move_down_off(self):
        self.move_d = 0


    def reposition_player(self):
        self.rect.left += self.move_l + self.move_r
        self.rect.top += self.move_u + self.move_d


    def display_player(self, dsp_surface):
        dsp_surface.blit(self.image, (self.rect.left, self.rect.top))
