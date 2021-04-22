
class Layer:
    def __init__(self,  group):

        self.group = group

        self.visible = True
        self.objects = set()

    def clear(self):
        # Remove everything from the layer.
        self.objects.clear()

    def _draw(self):
        # Render the layer.
        if not self.visible:
            return
        self._draw_inner()

    def _draw_inner(self):
        for o in self.objects:
            o.draw()

    def add_object(self, obj):
        obj.layer = self
        self.objects.add(obj)

    @property
    def scene(self):
        return self.group.scene

    @property
    def screen(self):
        return self.group.scene.screen


class LayerGroup(dict):

    def __init__(self, scene):
        super().__init__()
        self.scene = scene

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls)

    def __missing__(self, k):
        if not isinstance(k, (float, int)):
            raise TypeError("Layer indices must be numbers")
        layer = self[k] = Layer(self)
        return layer

    def clear(self):
        # Clear the layer group.
        # We override this to explicitly release resources.

        for val in self.values():
            val.clear()
        super().clear()

    def draw(self):
        for key in sorted(self):
            self[key]._draw()
