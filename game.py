import pygame
from player import Player
from background import Background
from enemy import Enemy


class GameLoop:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 800, 600


    def on_init(self):
        # Initialize pygame.
        pygame.init()
        pygame.display.set_caption("Lucky's Adventure")
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        self.init_level_1()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False


    def on_loop(self):
        # Handle keyboard input.
        self.keyboard_input()

        # Adjust character positions.
        self.move_characters()

        # Check for collisions.
        if pygame.sprite.spritecollide(self.player, self.enemy_group, False):
            #print("collision")
            pass

        # Add elements to display surface.
        self.background.display(self._display_surf)
        for enemy in self.enemy_group:
            enemy.display(self._display_surf)
        self.player.display(self._display_surf)


    def on_render(self):
        # Redraw screen.
        pygame.display.flip()


    def on_cleanup(self):
        pygame.quit()


    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


    def keyboard_input(self):
        k = pygame.key.get_pressed()

        show_front = True

        if k[pygame.K_LEFT]:
            self.player.set_image(self.player.get_player_left_img())
            show_front = False
            if self.player.rect.left <= 0:
                self.player.move_left_off()
                for enemy in self.enemy_group:
                    enemy.move_right_off()
            else:
                self.player.move_left()

        if k[pygame.K_RIGHT]:
            self.player.set_image(self.player.get_player_right_img())
            show_front = False
            if self.player.rect.left >= (self.width * 0.4):
                for enemy in self.enemy_group:
                    enemy.move_left()
                self.background.move_left()
            if self.player.rect.left < (self.width * 0.4):
                self.player.move_right()
            else:
                self.player.move_right_off()

        if k[pygame.K_SPACE]:
            if not self.player.jump_in_progress():
                self.player.jump_start()

        if not k[pygame.K_LEFT]:
            self.player.move_left_off()

        if not k[pygame.K_RIGHT]:
            for enemy in self.enemy_group:
                enemy.move_left_off()
            self.background.move_left_off()
            self.player.move_right_off()

        if show_front:
            self.player.set_image(self.player.get_player_initial_image())

    def move_characters(self):
        self.background.reposition()
        self.player.jump()
        self.player.reposition()
        for enemy in self.enemy_group:
            enemy.reposition()


    def init_level_1(self):
        # Initialize characters.
        self.player = Player("graphics/blocky_front.png", 25, 472,
            ["graphics/blocky_right_0.png", "graphics/blocky_right_1.png", "graphics/blocky_right_2.png", "graphics/blocky_right_1.png"],
            ["graphics/blocky_left_0.png", "graphics/blocky_left_1.png", "graphics/blocky_left_2.png", "graphics/blocky_left_1.png"])

        self.enemy1 = Enemy("graphics/snake.png", 300, 529)
        self.enemy2 = Enemy("graphics/poison_grapes.png", 375, 529)
        self.enemy3 = Enemy("graphics/tree.png", 700, 100)

        # Initialize sprite groups.
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.enemy1)
        self.enemy_group.add(self.enemy2)
        self.enemy_group.add(self.enemy3)

        # Initialize background.
        self.background = Background("graphics/background.jpg", 0, 0, 2)


if __name__ == "__main__" :
    game_loop = GameLoop()
    game_loop.on_execute()
