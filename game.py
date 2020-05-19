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

        # Handle keyboard input.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for enemy in self.enemy_group:
                    enemy.move_right()
                self.background1.move_right()
            if event.key == pygame.K_RIGHT:
                for enemy in self.enemy_group:
                    enemy.move_left()
                self.background1.move_left()
            if event.key == pygame.K_SPACE:
                if not self.player1.jump_in_progress():
                    self.player1.jump_start()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                for enemy in self.enemy_group:
                    enemy.move_right_off()
                self.background1.move_right_off()
            if event.key == pygame.K_RIGHT:
                for enemy in self.enemy_group:
                    enemy.move_left_off()
                self.background1.move_left_off()


    def on_loop(self):
        # Adjust character positions.
        self.background1.reposition()
        self.player1.jump()
        self.player1.reposition()
        for enemy in self.enemy_group:
            enemy.reposition()

        # Check for collisions.
        if pygame.sprite.spritecollide(self.player1, self.enemy_group, False):
            print("collision")

        # Add elements to display surface.
        self._display_surf.fill((52, 235, 235))  # Background

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


if __name__ == "__main__" :
    game_loop = GameLoop()
    game_loop.on_execute()
