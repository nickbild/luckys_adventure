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

        self.destroyed = False
        self.remain_after_destroy = 25


    def move_left(self, speed_up):
        self.move_l = -5
        if speed_up:
            self.move_l = self.move_l * 2


    def move_right(self, speed_up):
        self.move_r = 5
        if speed_up:
            self.move_r = self.move_r * 2


    def move_left_off(self):
        self.move_l = 0


    def move_right_off(self):
        self.move_r = 0


    def reposition(self):
        self.rect.left += self.move_l + self.move_r
        self.rect.top += self.move_u + self.move_d

        if self.destroyed:
            self.remain_after_destroy -= 1
            if self.remain_after_destroy <= 0:
                self.rect.top = -1200


    def set_image(self, img):
        self.image = pygame.image.load(img)


    def get_initial_image(self):
        return self.img


    def blow_up(self, img):
        self.image = pygame.image.load(img)
        self.destroyed = True


    def is_destroyed(self):
        return self.destroyed


    def display(self, dsp_surface):
        dsp_surface.blit(self.image, (self.rect.left, self.rect.top))
