
from .layers import LayerGroup

import pygame


class Scene:
    # Top-level interface for renderable objects.
    # :param width: The width of the window to create, in pixels.
    # :param height: The height of the window to create, in pixels.
    # :param title: The initial window title.
    # :param icon: The icon for the window, as an image name without extension.
    # :param background: An initial setting for the :py:attr:`.background`.

    def __init__(
            self,
            width=800,
            height=600,
            title="game",
            icon=None,
            background=None,
            on_set_settings_fun=None):

        # on_set_settings (variable_name, value) - sets value
        self.on_set_settings = on_set_settings_fun

        self.width = width
        self.height = height
        self._fullscreen = False
        self.screen = None

        self.title = title
        self.icon = icon

        self.layers = LayerGroup(self)
        self.background = background

    def release(self):
        self.layers.clear()
        # gc.collect()

    def __del__(self):
        self.release()

    def toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        pygame.display.toggle_fullscreen()

       # if value:
       #     pygame.display.set_mode((self._width, self._height), pygame.FULLSCREEN)
       # else:
       #     pygame.display.set_mode((self._width, self._height),0)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        # Set the window WIDTH.
        self._width = width
        if self.on_set_settings is not None:
            self.on_set_settings("WIDTH", width)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        # Set the window HEIGHT.
        self._height = height
        if self.on_set_settings is not None:
            self.on_set_settings("HEIGHT", height)

    @property
    def background(self):
        # Get the background colour for the whole scene.
        return self._background

    @background.setter
    def background(self, v):
        # Set the background colour for the whole scene.
        self._background = v  # convert_color_rgb(v)

    @property
    def title(self):
        # Get the window TITLE.
        return self._title

    @title.setter
    def title(self, title):
        # Set the window TITLE.
        self._title = title
        if self.on_set_settings is not None:
            self.on_set_settings("TITLE", title)

    @property
    def icon(self):
        # Get the window ICON.
        return self._icon

    @icon.setter
    def icon(self, icon):
        # Set the window TITLE.
        self._icon = icon
        if self.on_set_settings is not None:
            self.on_set_settings("ICON", icon)

    @property
    def fullscreen(self):
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value):
        if self._fullscreen == value:
            return
        self.toggle_fullscreen()

    def draw(self):
        if self.background is None:
            self.screen.clear()
        else:
            self.screen.fill(self._background)

        self.layers.draw()
