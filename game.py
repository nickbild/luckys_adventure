import pygame
from player import Player
from background import Background
from enemy import Enemy
from missile import Missile


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

        pygame.font.init()
        self.info_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.score = 0
        self.score_surface = self.info_font.render("Score: {0}".format(str(self.score)), False, (255, 0, 0))

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
        for self.enemy_defeated_by_missile in self.enemy_defeated_by_missile_group:
            if pygame.sprite.spritecollide(self.enemy_defeated_by_missile, self.missile_group, False):
                if not self.enemy_defeated_by_missile.is_destroyed():
                    self.score = self.player.add_score(100)
                    self.score_surface = self.info_font.render("Score: {0}".format(str(self.score)), False, (255, 0, 0))
                self.enemy_defeated_by_missile.blow_up("graphics/explosion.png")

        # Add elements to display surface.
        self.background.display(self._display_surf)
        for enemy in self.enemy_group:
            enemy.display(self._display_surf)
        for missile in self.missile_group:
            missile.display(self._display_surf)
        self.player.display(self._display_surf)

        self._display_surf.blit(self.score_surface,(650,0))


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

        if k[pygame.K_a]:
            if not self.player.jump_in_progress():
                self.player.jump_start()

        if k[pygame.K_s]:
            if not self.bomb.throw_in_progress():
                if k[pygame.K_LEFT]:
                    self.bomb.throw_start(self.player.get_player_left(), self.player.get_player_top(), "L")
                else:
                    self.bomb.throw_start(self.player.get_player_right(), self.player.get_player_top(), "R")

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

        for missile in self.missile_group:
            missile.reposition()


    def init_level_1(self):
        # Initialize characters.
        self.player = Player("graphics/blocky_front.png", 25, 472,
            ["graphics/blocky_right_0.png", "graphics/blocky_right_1.png", "graphics/blocky_right_2.png", "graphics/blocky_right_1.png"],
            ["graphics/blocky_left_0.png", "graphics/blocky_left_1.png", "graphics/blocky_left_2.png", "graphics/blocky_left_1.png"])

        self.enemy1 = Enemy("graphics/snake.png", 300, 529)
        self.enemy2 = Enemy("graphics/poison_grapes.png", 375, 529)
        self.enemy3 = Enemy("graphics/tree.png", 700, 100)

        self.bomb = Missile("graphics/bomb.png", -100, 529)

        # Initialize sprite groups.
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.enemy1)
        self.enemy_group.add(self.enemy2)
        self.enemy_group.add(self.enemy3)

        self.missile_group = pygame.sprite.Group()
        self.missile_group.add(self.bomb)

        self.enemy_defeated_by_missile_group = pygame.sprite.Group()
        self.enemy_defeated_by_missile_group.add(self.enemy1)

        # Initialize background.
        self.background = Background("graphics/background.jpg", 0, 0, 2)


if __name__ == "__main__" :
    game_loop = GameLoop()
    game_loop.on_execute()
