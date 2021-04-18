from pgzero.actor import Actor
from settings import *
from gamemanager import GameState
from animatedactor import AnimatedActor
from text import Label
from sprite import Sprite
import random


# These constants control the difficulty of the game


GRAVITY = 0.3
FLAP_STRENGTH = 6.5
GAP = 130
SPEED = 3

HIGH_SCORE = 0

class Bird(AnimatedActor):
    
    def __init__(self, game):
        super().__init__("bird",dimension=(40,30),pingpong=True,duration=100)
        self.reset()

    def reset(self):
        self.dead = False
        self.score = 0
        self.vy = 0
        self.y = 200
        self.set_move_state()

    def set_move_state(self):
        self.set_sequence(0,2)
        self.pingpong= True

    def set_dead_state(self):
        self.dead = True
        self.pingpong= False
        self.current_frame=3

    def move(self):
        if not self.dead:
            self.vy = -FLAP_STRENGTH

    def update(self):
        uy = self.vy
        self.vy += GRAVITY
        self.y += (uy + self.vy) / 2
        self.x = 75

    def checkcollision(self, sprite):
        return self.colliderect(sprite)


"""
        if self.colliderect(self.pipe_top) or self.bird.colliderect(self.pipe_bottom) or (self.bird.y > HEIGHT - 20):
            self.dead = True
            self.image = 'birddead'

        if not 0 < self.y < 720:
            self.y = 200
            self.dead = False
            self.score = 0
            self.vy = 0
            self.reset_pipes()
"""

class Pipes:
    pipe_top = Actor('top', anchor=('left', 'bottom'))
    pipe_bottom = Actor('bottom', anchor=('left', 'top'))

    def reset(self):
        pipe_gap_y = random.randint(200, HEIGHT - 200)
        self.pipe_top.pos = (WIDTH, pipe_gap_y - GAP // 2)
        self.pipe_bottom.pos = (WIDTH, pipe_gap_y + GAP // 2)

    
    def checkcollision(self, sprite):
        return sprite.colliderect(self.pipe_top) or sprite.colliderect(self.pipe_bottom)

    def draw(self):
        self.pipe_top.draw()
        self.pipe_bottom.draw()

    def update(self):
        global HIGH_SCORE
        self.pipe_top.left -= SPEED
        self.pipe_bottom.left -= SPEED
        if self.pipe_top.right < 0:
            self.reset()

           # if not self.bird.dead:
           #     self.bird.score += 1
           #     if self.bird.score > HIGH_SCORE:
           #         HIGH_SCORE = self.bird.score


class PlayState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.name = "Play"

        self.bird = Bird(game)
        self.pipes = Pipes()

        self.birdsc = Label (  str(self.bird.score), color='white',pos = (WIDTH // 2, 10),fontsize=70)
        self.bestsc = Label (  "Best: {}".format(HIGH_SCORE), color='white',pos = (WIDTH // 2, HEIGHT - 10),fontsize=30)
        self.background = Sprite ('background', (0, 0))

        self.pipes.reset()  # Set initial pipe positions.
  
    def onEnter(self, prevstate):
        self.bird.reset()
        self.pipes.reset()  # Set initial pipe positions.
        self.game.scene.layers[0].add_object(self.background)
        
        self.game.scene.layers[1].add_object(self.pipes)
        self.game.scene.layers[1].add_object(self.bird)

        self.game.scene.layers[2].add_object(self.birdsc)
        self.game.scene.layers[2].add_object(self.bestsc)

    def onExit(self):
        self.game.scene.layers.clear()


    def update(self):
        self.pipes.update()
        self.bird.update()

        if self.pipes.checkcollision(self.bird):
            self.bird.set_dead_state()

        if self.bird.dead and (self.bird.y > HEIGHT - 20):
            self.next()

        self.birdsc.text = str(self.bird.score)

    def on_key_down(self):
        if not self.bird.dead:
            self.bird.move()
