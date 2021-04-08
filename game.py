import pgzrun
import random

from gamemanager import GameManager, GameState

TITLE = 'Flappy Bird'
WIDTH = 400
HEIGHT = 708

# These constants control the difficulty of the game
GAP = 130
GRAVITY = 0.3
FLAP_STRENGTH = 6.5
SPEED = 3

HIGH_SCORE = 0


class PlayState(GameState):

    bird = Actor('bird1', (75, 200))

    pipe_top = Actor('top', anchor=('left', 'bottom'))
    pipe_bottom = Actor('bottom', anchor=('left', 'top'))

    def __init__(self, game):
        super().__init__(game)
      
        self.reset_bird()
        self.reset_pipes()  # Set initial pipe positions.

    def update_pipes(self):
        global HIGH_SCORE
        self.pipe_top.left -= SPEED
        self.pipe_bottom.left -= SPEED
        if self.pipe_top.right < 0:
            self.reset_pipes()
            if not self.bird.dead:
                self.bird.score += 1
                if self.bird.score > HIGH_SCORE:
                    HIGH_SCORE = self.bird.score

    def reset_pipes(self):
        pipe_gap_y = random.randint(200, HEIGHT - 200)
        self.pipe_top.pos = (WIDTH, pipe_gap_y - GAP // 2)
        self.pipe_bottom.pos = (WIDTH, pipe_gap_y + GAP // 2)

    def reset_bird(self):
        self.bird.dead = False
        self.bird.score = 0
        self.bird.vy = 0
        self.bird.y = 0
        self.bird.image = 'bird1'

    def update_bird(self):
        uy = self.bird.vy
        self.bird.vy += GRAVITY
        self.bird.y += (uy + self.bird.vy) / 2
        self.bird.x = 75

        if not self.bird.dead:
            if self.bird.vy < -3:
                self.bird.image = 'bird2'
            else:
                self.bird.image = 'bird1'

        if self.bird.colliderect(self.pipe_top) or self.bird.colliderect(self.pipe_bottom) or (self.bird.y > HEIGHT -20):
            self.bird.dead = True
            self.bird.image = 'birddead'

        if not 0 < self.bird.y < 720:
            self.bird.y = 200
            self.bird.dead = False
            self.bird.score = 0
            self.bird.vy = 0
            self.reset_pipes()

    def onEnter(self,prevstate):
        self.reset_bird()
        self.reset_pipes()  # Set initial pipe positions.



    def draw(self):
        screen.blit('background', (0, 0))
        self.pipe_top.draw()
        self.pipe_bottom.draw()
        self.bird.draw()

        screen.draw.text(
            str(self.bird.score),
            color='white',
            midtop=(WIDTH // 2, 10),
            fontsize=70,
            shadow=(1, 1)
        )
        screen.draw.text(
            "Best: {}".format(HIGH_SCORE),
            color=(200, 170, 0),
            midbottom=(WIDTH // 2, HEIGHT - 10),
            fontsize=30,
            shadow=(1, 1)
        )

    def update(self):
        self.update_pipes()
        self.update_bird()

        if self.bird.dead  and (self.bird.y > HEIGHT -20):
            self.next()

    def on_key_down(self):
        if not self.bird.dead:
            self.bird.vy = -FLAP_STRENGTH


class MainMenuState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.scroll_pos = -1

    def draw(self):

        screen.blit('startscreen', (0, 0))

        screen.draw.text(
            "PRESS A KEY TO START",
            color='white',
            midtop=(WIDTH // 2, HEIGHT // 2 + self.scroll_pos),
            fontsize=40,
            shadow=(1, 1)
        )

    def update(self):
        self.scroll_pos *= -1

    def on_key_down(self):
        self.next()


class GameOverState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.scroll_pos = -1

    def draw(self):
        screen.blit("gameover", (0, 0))

        screen.draw.text(
            "PRESS ANY KEY TO CONTINUE",
            color='white',
            midtop=(WIDTH // 2, HEIGHT - 140 + self.scroll_pos),
            fontsize=35,
            shadow=(1, 1)
        )

    def update(self):
        self.scroll_pos *= -1

    def on_key_down(self):
        self.next()


def update():
    game.update()


def on_key_down():
    game.on_key_down()


def draw():
    game.draw()


game = GameManager()
state1 = MainMenuState(game)
state2 = PlayState(game)
state3 = GameOverState(game)

state1.nextstate = state2
state2.nextstate = state3
state3.nextstate = state1

game.play_music("theme")
game.play_sound("eagle")
game.run(state1)
pgzrun.go()
