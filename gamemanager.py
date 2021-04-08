from pygame import mixer
from random import randint
from pgzero import music

from pgzero import loaders


class GameState:

    # Initialise the Game state class. Each sub-type must call this method. Takes one parameter, which
    # is the game instance.

    def __init__(self, game_fsm_manager, state=None):
        self.game = game_fsm_manager
        self.nextstate = state

    # Called by the game when entering the state for the first time.

    def onEnter(self, previousState):
        pass

    # Called by the game when leaving the state.

    def onExit(self):
        pass

    # Called by the game allowing the state to update itself. The game time (in milliseconds) since
    # the last call is passed.

    def update(self):
        pass

    # Called by the game allowing the state to draw itself. The surface that is passed is the
    # current drawing surface.
    def draw(self, surf):
        pass

    # Called by the game on key down
    def on_key_down(self):
        pass

    def next(self):
        self.game.changeState(self.nextstate)


class GameFSM:

    # Initialise the FSM manager class.
    def __init__(self):
        self.currentState = None

    # Change the current state. If the newState is 'None' then the game will terminate.
    def changeState(self, newState):
        if (self.currentState != None):
            self.currentState.onExit()

        if (newState == None):
            self.onExit()

        oldState = self.currentState
        self.currentState = newState
        newState.onEnter(oldState)

    # Run the game. Initial state must be supplied.
    def run(self, initialState):
        self.changeState(initialState)

    # Called by the game when leaving the state.

    def onExit(self):
        pass

    # Called by the game allowing the state to update itself. The game time (in milliseconds) since
    # the last call is passed.

    def update(self):
        pass

    # Called by the game allowing the state to draw itself. The surface that is passed is the
    # current drawing surface.

    def draw(self, surf):
        pass


class GameFSMWSounds(GameFSM):

    def __init__(self):
        super().__init__()
        self.looped_sounds = {}
        self.reset_mixer()

    def play_music(self, name):
        music.play(name)
        music.set_volume(1)

    def play_sound(self, name, count=1):

        sound = getattr(loaders.sounds, name + str(randint(0, count - 1)))
        sound.play()

    def loop_sound(self, name, count, volume):
        if volume > 0 and not name in self.looped_sounds:
            full_name = name + str(randint(0, count - 1))
            # see play_sound method above for explanation
            sound = getattr(loaders.sounds, full_name)
            sound.play(-1)  # -1 means sound will loop indefinitely
            self.looped_sounds[name] = sound

        if name in self.looped_sounds:
            sound = self.looped_sounds[name]
            if volume > 0:
                sound.set_volume(volume)
            else:
                sound.stop()
                del self.looped_sounds[name]

    def stop_looped_sounds(self):
        for sound in self.looped_sounds.values():
            sound.stop()
        self.looped_sounds.clear()

    def reset_mixer(self):
        # Set up sound system
        try:
            mixer.quit()
            mixer.init(44100, -16, 2, 512)
            mixer.set_num_channels(16)
        except:
            # If an error occurs, just ignore it
            pass


class GameManager(GameFSMWSounds):

    def __init__(self):
        super().__init__()

    def update(self):
        if (self.currentState != None):
            self.currentState.update()

    def draw(self,surf):
        if (self.currentState != None):
            self.currentState.draw(surf)

   # Called by the game on key down
    def on_key_down(self):
        if (self.currentState != None):
            self.currentState.on_key_down()
