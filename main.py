import pgzrun
from settings import *

from lib.pgzgamemanager import GameManager
from lib.scene import Scene

from flappystates import MainMenuState, GameOverState, PlayState



def update():
    game.update()


def on_set_settings(var_name, value):
    globals()[var_name] = value


def on_key_down():
    game.on_key_down()


def draw():
    scene.screen = screen
    scene.draw()

#    bird.draw(screen)


scene = Scene(WIDTH, HEIGHT, TITLE, on_set_settings_fun=on_set_settings)
game = GameManager(scene, clock,  images, keyboard, music, sounds, tone)

state1 = MainMenuState(game)
state2 = PlayState(game)
state3 = GameOverState(game)

state1.nextstate = state2
state2.nextstate = state3
state3.nextstate = state1

game.play_music("theme")

game.run(state1)

pgzrun.go()
