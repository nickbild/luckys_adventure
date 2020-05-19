import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()

        self.rect.left = x
        self.rect.top = y

        # Movement
        self.move_l = 0
        self.move_r = 0
        self.move_d = 0
        self.move_u = 0

        # Jumping
        self.v_init = 7
        self.m_init = 1

        self.is_jumping = False
        self.start_jump = self.rect.top
        self.F = 0
        self.v = self.v_init
        self.m = self.m_init


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


    def jump_in_progress(self):
        return self.is_jumping


    def jump_start(self):
        self.is_jumping = True
        self.start_jump = self.rect.top


    def jump(self):
        if not self.is_jumping:
            return

        # Calculate force (F). F = 1 / 2 * mass * velocity ^ 2.
        self.F = (1 / 2) * self.m * (self.v ** 2)

        self.rect.top -= self.F

        # Decreasing velocity while going up; becomes negative while coming down.
        self.v = self.v - 1

        # Sprite at max height...
        if self.v <= 0:
            # Negative sign is added to counter negative velocity.
            self.m =- 1

        # Object reaches its original state.
        if self.v < (self.v_init * -1):
            # Reset state.
            self.is_jumping = False
            self.rect.top = self.start_jump
            self.v = self.v_init
            self.m = self.m_init


    def reposition_player(self):
        self.rect.left += self.move_l + self.move_r
        self.rect.top += self.move_u + self.move_d


    def display_player(self, dsp_surface):
        dsp_surface.blit(self.image, (self.rect.left, self.rect.top))
