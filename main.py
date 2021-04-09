import pgzrun
from settings import *

from pgzgamemanager import GameManager
from flappystates import MainMenuState,GameOverState
from flappyplay import PlayState


def update():
    game.update()

def on_key_down():
    game.on_key_down()

def draw():
    game.draw(screen)


game = GameManager(clock, images, keyboard, music, sounds, tone)
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
