from settings import *
from gamemanager import GameState

class MainMenuState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.scroll_pos = -1
        self.name = "Main menu"

    def draw(self,surf):

        surf.blit('startscreen', (0, 0))

        surf.draw.text(
            "PRESS ANY KEY TO START",
            color='white',
            midtop=(WIDTH // 2, HEIGHT // 2 + self.scroll_pos),
            fontsize=35,
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
        self.name = "Game over"

    def draw(self, surf):
        surf.blit("gameover", (0, 0))

        surf.draw.text(
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