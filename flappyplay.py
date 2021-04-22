from pgzero.actor import Actor
from lib.animatedactor import AnimatedActor
from lib.text import Label
from lib.sprite import Sprite
import random


# These constants control the difficulty of the game


class Context:
    HIGH_SCORE = 0
    _score = 0
    lives = 1
    dead = False

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        if self._score > self.HIGH_SCORE:
            self.HIGH_SCORE = self._score

    def reset(self):
        self._score = 0
        self.lives = 1
        self.dead = False


class Bird(AnimatedActor):
    GRAVITY = 0.3
    FLAP_STRENGTH = 6.5

    def __init__(self, game):
        super().__init__("bird", dimension=(40, 30), pingpong=True, duration=100)
        self.reset()
        self.game = game

    def reset(self):
        self.dead = False
        self.score = 0
        self.vy = 0
        self.y = 200
        self.set_move_state()

    def set_move_state(self):
        self.set_sequence(0, 2)
        self.pingpong = True

    def set_dead_state(self):
        
        if not self.dead: 
            self.game.play_sound("eagle")
            
        self.dead = True
        self.pingpong = False
        self.current_frame = 3

    def move(self):
        if not self.dead:
            self.vy = -self.FLAP_STRENGTH

    def update(self):
        uy = self.vy
        self.vy += self.GRAVITY
        self.y += (uy + self.vy) / 2
        self.x = 100

    def checkcollision(self, sprite):
        return self.colliderect(sprite)


class Pipes:
    GAP = 130
    SPEED = 3

    def __init__(self, game):
        self.game = game
        self.pipe_top = Actor('top', anchor=('left', 'bottom'))
        self.pipe_bottom = Actor('bottom', anchor=('left', 'top'))

    def reset(self):
        pipe_gap_y = random.randint(200, self.game.scene.height - 200)
        self.pipe_top.pos = (self.game.scene.width, pipe_gap_y - self.GAP // 2)
        self.pipe_bottom.pos = (self.game.scene.width,
                                pipe_gap_y + self.GAP // 2)

    def checkcollision(self, sprite):
        return sprite.colliderect(self.pipe_top) or sprite.colliderect(self.pipe_bottom)

    def draw(self):
        self.pipe_top.draw()
        self.pipe_bottom.draw()

    def update(self, con):
        self.pipe_top.left -= self.SPEED
        self.pipe_bottom.left -= self.SPEED
        if self.pipe_top.right < 0:
            self.reset()
            if not con.dead:
                con.score += 1


class Base:

    # Represnts the moving floor of the game

    VEL = 3
    WIDTH = 336

    def __init__(self, y):

        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

        self.baseimage = Actor('base2', anchor=(0, 0))
        self.baseimage2 = Actor('base2', anchor=(0, 0))

        self.baseimage.pos = (self.x1, self.y)
        self.baseimage2.pos = (self.x2, self.y)

    def update(self):
        # move floor so it looks like its scrolling

        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

        self.baseimage.pos = (self.x1, self.y)
        self.baseimage2.pos = (self.x2, self.y)

    def draw(self):
        # Draw the floor. This is two images that move together.
        self.baseimage.draw()
        self.baseimage2.draw()

    def checkcollision(self, sprite):
        return sprite.colliderect(self.baseimage) or sprite.colliderect(self.baseimage2)
