class Label:

    def __init__(self,
            text,
            layer=None,
            align='left',
            fontsize=20,
            pos=(0, 0),
            color=(1, 1, 1, 1)):

        self.layer = layer
        self.align = align
        self.fontsize = fontsize
        self.pos = pos
        self.color = color
        self.text = text  # trigger layout

    def draw(self):
        surf = self.layer.screen
        surf.draw.text(
            self.text,self.pos,color=self.color,
            fontsize=self.fontsize
        )
