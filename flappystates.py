from settings import *
from gamemanager import GameState
from text import Label
from sprite import Sprite

class MainMenuState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.scroll_pos = -1
        self.name = "Main menu"

        self.label = Label (  "PRESS ANY KEY TO START", color='white',pos = (10, HEIGHT // 2 + self.scroll_pos),fontsize=35)
        self.startscreen = Sprite ('startscreen', (0, 0))
      
    def onEnter(self, prevstate):
        self.game.scene.layers[0].add_object(self.startscreen)
        self.game.scene.layers[0].add_object(self.label)

    def onExit(self):
        self.game.scene.layers.clear()

    def update(self):
        self.scroll_pos *= -1
        self.label.pos =  (10, HEIGHT // 2 + self.scroll_pos)

    def on_key_down(self):
        self.next()


class GameOverState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.scroll_pos = -1
        self.name = "Game over"
        self.label = Label (  "PRESS ANY KEY TO CONTINUE", color='white',pos = (10, HEIGHT // 2 + self.scroll_pos),fontsize=35)
        self.gameoverscreen = Sprite ('gameover', (0, 0))
    
    
    def onEnter(self, prevstate):
        self.game.scene.layers[0].add_object(self.gameoverscreen)
        self.game.scene.layers[0].add_object(self.label)

    def onExit(self):
        self.game.scene.layers.clear()

    def update(self):
        self.scroll_pos *= -1
        self.label.pos =  (10, HEIGHT // 2 + self.scroll_pos)

    def on_key_down(self):
        self.next()