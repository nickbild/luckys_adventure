import pygame
from player import Player


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

        # Initialize player.
        self.player1 = Player("chewie.jpg")


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        # Handle keyboard input.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player1.move_left()
            if event.key == pygame.K_RIGHT:
                self.player1.move_right()
            if event.key == pygame.K_UP:
                self.player1.move_up()
            if event.key == pygame.K_DOWN:
                self.player1.move_down()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.player1.move_left_off()
            if event.key == pygame.K_RIGHT:
                self.player1.move_right_off()
            if event.key == pygame.K_UP:
                self.player1.move_up_off()
            if event.key == pygame.K_DOWN:
                self.player1.move_down_off()


    def on_loop(self):
        # Adjust player position.
        self.player1.reposition_player()

        # Add elements to display surface.
        self._display_surf.fill((255,255,255))
        self.player1.display_player(self._display_surf)


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