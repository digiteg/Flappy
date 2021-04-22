from .gamemanager import GameFSM
from random import randint


class GameSounds:

    def __init__(self, _music, _sounds, _tone):
        super().__init__()
        self.looped_sounds = {}
        self.reset_mixer()

        self.music = _music
        self.sounds = _sounds
        self.tone = _tone

    def play_music(self, name):
        self.music.play(name)
        self.music.set_volume(1)

    def play_sound(self, name, count=1):

        sound = getattr(self.sounds, name + str(randint(0, count - 1)))
        sound.play()

    def loop_sound(self, name, count, volume):
        if volume > 0 and not name in self.looped_sounds:
            full_name = name + str(randint(0, count - 1))
            # see play_sound method above for explanation
            sound = getattr(self.sounds, full_name)
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
            self.music.mixer.quit()
            self.music.mixer.init(44100, -16, 2, 512)
            self.music.mixer.set_num_channels(16)
        except:
            # If an error occurs, just ignore it
            pass


class GameManager(GameSounds, GameFSM):

    def __init__(self, _scene, _clock, _images, _keyboard,  _music, _sounds, _tone):
        GameSounds.__init__(self,_music, _sounds, _tone)
        self.clock = _clock
        self.images = _images
        self.keyboard = _keyboard
        self.scene = _scene
    
    def update(self):
        if (self.currentState != None):
            self.currentState.update()

    # def draw(self, surf=None):
    #    if (self.currentState != None):
    #        if (surf is None):
    #            self.currentState.draw(self.screen)
    #        else:
    #            self.currentState.draw(surf)

   # Called by the game on key down
    def on_key_down(self):
        if (self.currentState != None):
            self.currentState.on_key_down()
