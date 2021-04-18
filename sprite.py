class Sprite:

    def __init__(self,image,layer=None,pos=(0,0)):
        self.layer = layer
        self.image = image
        self.pos = pos

    def draw (self):
        surf = self.layer.screen
        surf.blit(self.image,self.pos)