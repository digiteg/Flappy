from layers import LayerGroup


class Scene:
    """Top-level interface for renderable objects.
    :param width: The width of the window to create, in pixels.
    :param height: The height of the window to create, in pixels.
    :param title: The initial window title.
    :param icon: The icon for the window, as an image name without extension.
    :param background: An initial setting for the :py:attr:`.background`.
    """

    def __init__(
            self,
            width=800,
            height=600,
            title="game",
            fullscreen=False,
            icon=None,
            background='black'):

        self.width = width
        self.height = height
        self.fullscreen = fullscreen
        self.screen = None

        self.title = title

        self.layers = LayerGroup(self)
        self.background = background

    def release(self):
        self.layers.clear()
        # gc.collect()

    def __del__(self):
        self.release()

    @property
    def background(self):
        """Get the background colour for the whole scene."""
        return self._background

    @background.setter
    def background(self, v):
        """Set the background colour for the whole scene."""
        self._background = v  # convert_color_rgb(v)

    @property
    def title(self):
        """Get the window title."""
        return self._title

    @title.setter
    def title(self, title):
        """Set the window title."""

        self._title = title

        # pygame.display.set_caption(title)

    def draw(self):
        self.layers.draw()
