
from lib.gamemanager import GameState
from lib.text import Label
from lib.sprite import Sprite

from flappyplay import Base, Bird, Pipes, Context

class MainMenuState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.scroll_pos = -1
        self.name = "Main menu"

        self.label = Label("PRESS ANY KEY TO START", color='white', pos=(
            10, self.game.scene.height // 2 + self.scroll_pos), fontsize=35)
        self.startscreen = Sprite('startscreen', (0, 0))

    def onEnter(self, prevstate):
        self.game.scene.layers[0].add_object(self.startscreen)
        self.game.scene.layers[0].add_object(self.label)

    def onExit(self):
        self.game.scene.layers.clear()

    def update(self):
        self.scroll_pos *= -1
        self.label.pos = (10, self.game.scene.height // 2 + self.scroll_pos)

    def on_key_down(self):
        self.next()


class GameOverState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.scroll_pos = -1
        self.name = "Game over"
        self.label = Label("PRESS ANY KEY TO CONTINUE", color='white', pos=(
            10, self.game.scene.height // 2 + self.scroll_pos), fontsize=35)
        self.gameoverscreen = Sprite('gameover', (0, 0))

    def onEnter(self, prevstate):
        self.game.scene.layers[0].add_object(self.gameoverscreen)
        self.game.scene.layers[0].add_object(self.label)

    def onExit(self):
        self.game.scene.layers.clear()

    def update(self):
        self.scroll_pos *= -1
        self.label.pos = (10, self.game.scene.height // 2 + self.scroll_pos)

    def on_key_down(self):
        self.next()


class PlayState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.name = "Play"

        self.context = Context()

        self.bird = Bird(game)
        self.pipes = Pipes(game)
        self.base = Base(self.game.scene.height-112)

        self.birdsc = Label(str(self.context.score),
                            color='white', pos=(self.game.scene.width // 2, 10), fontsize=70)
        self.bestsc = Label("Best: {}".format(self.context.HIGH_SCORE), color='white', pos=(
            self.game.scene.width // 2, self.game.scene.height - 40), fontsize=30)
        self.background = Sprite('background', (0, 0))

        self.pipes.reset()  # Set initial pipe positions.

    def onEnter(self, prevstate):
        self.context.reset()
        self.bird.reset()
        self.pipes.reset()  # Set initial pipe positions.
        self.game.scene.layers[0].add_object(self.background)

        self.game.scene.layers[1].add_object(self.pipes)

        self.game.scene.layers[2].add_object(self.base)
        self.game.scene.layers[2].add_object(self.bird)

        self.game.scene.layers[3].add_object(self.birdsc)
        self.game.scene.layers[3].add_object(self.bestsc)

    def onExit(self):
        self.game.scene.layers.clear()

    def update(self):
        self.pipes.update(self.context)
        self.base.update()
        self.bird.update()

        if self.pipes.checkcollision(self.bird) or self.base.checkcollision(self.bird):
            self.bird.set_dead_state()
            self.context.dead = True

        if self.context.dead and (self.bird.y > self.game.scene.height - 20):
            self.next()

        self.birdsc.text = str(self.context.score)
        self.bestsc.text = "Best: {}".format(self.context.HIGH_SCORE)

    def on_key_down(self):
        if not self.bird.dead:
            self.bird.move()
