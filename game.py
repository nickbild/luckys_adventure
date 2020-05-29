import pygame
from player import Player
from background import Background
from enemy import Enemy
from missile import Missile
import time


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
        self.info_font = pygame.font.SysFont('mrrobototf', 35)
        self.score = 0
        self.update_score(self.score)

        self.init_level_1()
        self.update_lives(self.player.get_lives_left())

        self.game_over = False


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False


    def on_loop(self):
        if not self.game_over:
            if self.player.is_destroyed():
                time.sleep(1)
                self.player.revive()
                self.bomb.set_throw_state(False)
                if self.player.get_lives_left() < 0:
                    self.game_over = True
                self.init_level_1(False)
                self.update_lives(self.player.get_lives_left())

            # Handle keyboard input.
            self.keyboard_input()

            # Adjust character positions.
            self.move_characters()

            # Check for collisions.
            if pygame.sprite.spritecollide(self.player, self.pipe_group, True):
                self.level_1_complete()

            for self.enemy_defeated_by_missile in self.enemy_defeated_by_missile_group:
                if pygame.sprite.spritecollide(self.enemy_defeated_by_missile, self.missile_group, False):
                    if not self.enemy_defeated_by_missile.is_destroyed():
                        self.score = self.player.add_score(100)
                        self.update_score(self.score)
                        if self.enemy_defeated_by_missile in self.axe_group:
                            self.bomb.set_image("graphics/axe.png")
                    if self.enemy_defeated_by_missile in self.axe_group:
                        self.enemy_defeated_by_missile.blow_up("graphics/explosion_axe.png")
                    elif self.enemy_defeated_by_missile in self.tree_group:
                        self.enemy_defeated_by_missile.blow_up("graphics/explosion_big.png")
                    else:
                        self.enemy_defeated_by_missile.blow_up("graphics/explosion.png")

            if pygame.sprite.spritecollide(self.player, self.enemy_group, False):
                self.player.blow_up("graphics/explosion.png")

            # Add elements to display surface.
            self.background.display(self._display_surf)
            for enemy in self.enemy_group:
                enemy.display(self._display_surf)
            for missile in self.missile_group:
                missile.display(self._display_surf)
            self.player.display(self._display_surf)

            # Info display.
            self._display_surf.blit(self.score_surface,(550,10))
            self._display_surf.blit(self.lives_surface,(50,10))

        else:
            self._display_surf.blit(pygame.image.load("graphics/game_over.jpg"), (0, 0))
            self._running = False


    def on_render(self):
        # Redraw screen.
        pygame.display.flip()


    def on_cleanup(self):
        # Wait for a keypress before ending game.
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    wait = False

        self._running = False
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


    def update_score(self, score):
        self.score_surface = self.info_font.render("Score: {0}".format(str(score)), False, (255, 0, 0))


    def update_lives(self, lives):
        self.lives_surface = self.info_font.render("Lives: {0}".format(str(lives)), False, (255, 0, 0))


    def keyboard_input(self):
        k = pygame.key.get_pressed()

        if k[pygame.K_LEFT]:
            self.player.set_image(self.player.get_player_left_img())
            if self.player.rect.left <= 0:
                self.player.move_left_off()
                for enemy in self.enemy_group:
                    enemy.move_right_off()
            else:
                self.player.move_left()

        if k[pygame.K_RIGHT]:
            self.player.set_image(self.player.get_player_right_img())
            if self.player.rect.left >= (self.width * 0.4):
                for enemy in self.enemy_group:
                    enemy.move_left(self.player.jump_in_progress())
                self.background.move_left(self.player.jump_in_progress())
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


    def move_characters(self):
        self.background.reposition()
        self.player.jump()
        self.player.reposition()

        for enemy in self.enemy_group:
            enemy.reposition()

        for missile in self.missile_group:
            missile.reposition()


    def add_enemy_to_group(self, img, x, y, display_group, other_groups):
        self.enemy = Enemy(img, x, y)
        display_group.add(self.enemy)

        for other_group in other_groups:
            other_group.add(self.enemy)


    def init_level_1(self, reset_player=True):
        # Initialize characters and associated sprites.
        if reset_player:
            self.player = Player("graphics/blocky_right_1.png", 25, 472,
                ["graphics/blocky_right_0.png", "graphics/blocky_right_1.png", "graphics/blocky_right_2.png", "graphics/blocky_right_1.png"],
                ["graphics/blocky_left_0.png", "graphics/blocky_left_1.png", "graphics/blocky_left_2.png", "graphics/blocky_left_1.png"])
        else:
            self.player.set_position(25, 472)

        self.bomb = Missile("graphics/bomb.png", -100, -1000)

        # Initialize sprite groups.
        self.enemy_group = pygame.sprite.Group()
        self.enemy_defeated_by_missile_group = pygame.sprite.Group()
        self.missile_group = pygame.sprite.Group()
        self.axe_group = pygame.sprite.Group()
        self.tree_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()

        # Add sprites to groups.
        self.add_enemy_to_group("graphics/snake.png", 300, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 600, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 1200, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 1300, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 1700, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 2200, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 2900, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 3500, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 4000, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 4100, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 4200, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 5000, 529, self.enemy_group, [self.enemy_defeated_by_missile_group, self.axe_group])
        self.add_enemy_to_group("graphics/snake.png", 5500, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 5600, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])
        self.add_enemy_to_group("graphics/snake.png", 6000, 529, self.enemy_group, [self.enemy_defeated_by_missile_group])

        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 375, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 395, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 415, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 875, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 895, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 1450, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 1470, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 1490, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 1510, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 1710, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 1730, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 1750, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 1900, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 1920, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 1940, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 2300, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 2500, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 2700, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 3500, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 3520, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 3540, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 3700, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 3900, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 4500, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 4900, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 5300, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 5320, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 5340, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 6000, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 6200, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 6400, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 7000, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 7020, 570, self.enemy_group, [])
        self.add_enemy_to_group("graphics/poison_grapes_sm.png", 7040, 570, self.enemy_group, [])

        self.add_enemy_to_group("graphics/tree.png", 8000, 100, self.enemy_group, [self.enemy_defeated_by_missile_group, self.tree_group])
        self.add_enemy_to_group("graphics/pipe.png", 8700, 336, self.enemy_group, [self.pipe_group])

        self.missile_group.add(self.bomb)

        # Initialize background.
        self.background = Background("graphics/background.jpg", 0, 0, 2)

    def level_1_complete(self):
        self.background = Background("graphics/level_1_complete.png", 0, 0, 2)
        self.player.set_position(-100, -15000)
        self._running = False

if __name__ == "__main__" :
    while True:
        game_loop = GameLoop()
        game_loop.on_execute()
