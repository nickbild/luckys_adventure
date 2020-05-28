import pygame


class Missile(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img)
        self.img = img
        self.rect = self.image.get_rect()

        self.rect.left = x
        self.rect.top = y

        # Throwing
        self.is_throwing = False


    def throw_in_progress(self):
        return self.is_throwing


    def throw_start(self, x, y, direction):
        self.is_throwing = True

        if direction == "L":
            self.rect.left = x - 25
        else:
            self.rect.left = x

        self.rect.top = y

        self.throw_direction = direction


    def reposition(self):
        if not self.is_throwing:
            return

        if self.throw_direction == "L":
            self.rect.left -= 10
        else:
            self.rect.left += 10

        self.rect.top += 3

        if self.rect.bottom >= 600:
            # Explode here
            self.rect.top = -1000
            self.is_throwing = False


    def set_image(self, img):
        self.image = pygame.image.load(img)


    def display(self, dsp_surface):
        dsp_surface.blit(self.image, (self.rect.left, self.rect.top))
