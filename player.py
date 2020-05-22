import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, img, x, y, right_images, left_images):
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

        self.right_images = right_images
        self.right_img_index = 0
        self.right_img_slowdown = 0

        self.left_images = left_images
        self.left_img_index = 0
        self.left_img_slowdown = 0

        # Jumping
        self.v_init = 8
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


    def reposition(self):
        self.rect.left += self.move_l + self.move_r
        self.rect.top += self.move_u + self.move_d


    def set_image(self, img):
        self.image = pygame.image.load(img)


    def get_player_initial_image(self):
        return self.img


    def get_player_right_img(self):
        self.right_img_slowdown += 1
        if self.right_img_slowdown == 5:
            self.right_img_slowdown = 0
            self.right_img_index += 1
        if self.right_img_index == len(self.right_images):
            self.right_img_index = 0

        return self.right_images[self.right_img_index]


    def get_player_left_img(self):
          self.left_img_slowdown += 1
          if self.left_img_slowdown == 5:
              self.left_img_slowdown = 0
              self.left_img_index += 1
          if self.left_img_index == len(self.left_images):
              self.left_img_index = 0

          return self.left_images[self.left_img_index]


    def display(self, dsp_surface):
        dsp_surface.blit(self.image, (self.rect.left, self.rect.top))
