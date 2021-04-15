from pgzero.actor import Actor
from time import time


class AnimatedActor(Actor):
    def __init__(self, *args, dimension, pingpong=False, duration=100,  **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = duration
        self._stopped = False
        self._frames = []
        self.pingpong = pingpong

        self.set_image(self.image, dimension)

    def start(self):
        self._stopped = False

    def stop(self):
        self._stopped = True

    def set_image(self, image, dimension):
        px, py = self.pos
        tx, ty = self.topleft
        self.image = image
        self.width, self.height = dimension
        self._frames = []

        # counting that sprites will be same size
        self.pos = (px, py)
        self.topleft = (tx, ty)

        for x_offset in range(int(self._orig_surf.get_width() / self.width)):
            surface = self._orig_surf.subsurface(
                (x_offset * self.width, 0, self.width, self.height))
            self._frames.append(surface)

        # frame config
        self.set_sequence(0, len(self._frames), self.pingpong)

    @property
    def current_frame(self):
        return self._current_frame

    @current_frame.setter
    def current_frame(self, index):
        if 0 < index < len(self._frames) - 1:
            raise 'Frame index out of range.'
        self._current_frame = index

    def is_seqence_end(self):
        return (self._current_frame >= self.end_anim_index) and not self.pingpong

    def restart_sequence(self):
        self._current_frame = self.start_anim_index

    def set_sequence(self, start_index, end_index, pingpong=False):

        self.pingpong = pingpong

        # frame config
        self.current_frame = start_index

        if start_index < 0 or start_index > len(self._frames):
            start_index = 0
        else:
            self.start_anim_index = start_index

        if end_index > len(self._frames) or end_index < 0:
            self.end_anim_index = len(self._frames)
        else:
            self.end_anim_index = end_index

        self.frame_duration = self.duration / end_index
        self.last_frame_update = time() * 1000
        self._next_frame_dx = 1


    def _update_frame(self):

        if self._stopped or self.is_seqence_end():
            return

        now = time() * 1000
        if now - self.last_frame_update > self.frame_duration:
            self.last_frame_update = now
            self._current_frame += self._next_frame_dx

            if self.pingpong:
                if (self._next_frame_dx == 1 and self._current_frame >= self.end_anim_index - 1) or (self._next_frame_dx == -1 and self._current_frame <= 0):
                    self._next_frame_dx *= -1

            if self._current_frame > self.end_anim_index:
                self._current_frame = self.end_anim_index

    def draw(self, surf):
        self._update_frame()
        # print(self._current_frame)
        surf.blit(self._frames[self._current_frame], self.topleft)
