import pygame
from player import Player
from background import Background


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

        # Initialize characters.
        self.player1 = Player("graphics/blocky_front.png", 25, 472)
        self.enemy1 = Player("graphics/snake.png", 300, 529)
        self.enemy2 = Player("graphics/poison_grapes.png", 375, 529)
        self.enemy3 = Player("graphics/tree.png", 700, 100)

        # Initialize sprite groups.
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.enemy1)
        self.enemy_group.add(self.enemy2)
        self.enemy_group.add(self.enemy3)

        self.background1 = Background("graphics/background.jpg", 0, 0, 1)


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False


    def on_loop(self):
        # Handle keyboard input.
        self.keyboard_input()

        # Adjust character positions.
        self.move_characters()

        # Check for collisions.
        if pygame.sprite.spritecollide(self.player1, self.enemy_group, False):
            #print("collision")
            pass

        # Add elements to display surface.
        self.background1.display(self._display_surf)

        for enemy in self.enemy_group:
            enemy.display(self._display_surf)

        self.player1.display(self._display_surf)


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

        if k[pygame.K_LEFT]:
            if self.player1.rect.left <= 0:
                self.player1.move_left_off()
                for enemy in self.enemy_group:
                    enemy.move_right_off()
            else:
                self.player1.move_left()

        if k[pygame.K_RIGHT]:
            if self.player1.rect.left >= (self.width * 0.4):
                for enemy in self.enemy_group:
                    enemy.move_left()
                self.background1.move_left()
            if self.player1.rect.left < (self.width * 0.4):
                self.player1.move_right()
            else:
                self.player1.move_right_off()

        if k[pygame.K_SPACE]:
            if not self.player1.jump_in_progress():
                self.player1.jump_start()

        if not k[pygame.K_LEFT]:
            self.player1.move_left_off()

        if not k[pygame.K_RIGHT]:
            for enemy in self.enemy_group:
                enemy.move_left_off()
            self.background1.move_left_off()
            self.player1.move_right_off()


    def move_characters(self):
        self.background1.reposition()
        self.player1.jump()
        self.player1.reposition()
        for enemy in self.enemy_group:
            enemy.reposition()


if __name__ == "__main__" :
    game_loop = GameLoop()
    game_loop.on_execute()
