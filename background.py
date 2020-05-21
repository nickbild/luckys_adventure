import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, img, x, y, step):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image1 = pygame.image.load(img)
        self.rect1 = self.image.get_rect()

        self.rect.left = x
        self.rect.top = y
        self.rect1.left = x + self.rect.width
        self.rect1.top = y

        # Movement
        self.position_x = 0
        self.move_l = 0
        self.move_r = 0
        self.step = step


    def move_left(self):
        self.move_l = self.step * -1


    def move_right(self):
        self.move_r = self.step


    def move_left_off(self):
        self.move_l = 0


    def move_right_off(self):
        self.move_r = 0


    def reposition(self):
        self.position_x += -1 * (self.move_l + self.move_r)

        self.rect.left += self.move_l + self.move_r
        self.rect1.left += self.move_l + self.move_r

        self.coords = [self.rect.left, self.rect1.left]
        self.coords.sort()
        print("{} - {}".format(self.coords, self.position_x))

        if abs(self.rect.left - self.position_x) > (self.rect.width + (self.rect.width * 0.25)):
            self.rect.left = self.coords[1] + self.rect.width
        if abs(self.rect1.left - self.position_x) > (self.rect.width + (self.rect.width * 0.25)):
            self.rect1.left = self.coords[1] + self.rect.width


    def display(self, dsp_surface):
        dsp_surface.blit(self.image, (self.rect.left, self.rect.top))
        dsp_surface.blit(self.image1, (self.rect1.left, self.rect1.top))
