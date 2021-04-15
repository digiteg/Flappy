class State():
    def __init__(self):
        self.name = "state"
        self.image = ""

    def update(self, key):
        pass

    def __str__(self):
        return self.name

class ActorStanding(State):
    def __init__(self, actor):
        self.name = "standing"
        self.image = "dizzy"
        self.actor = actor
        self.actor.set_image(self.image, dimension=(25, 25))

    def update(self, key):
        if key.left:
            self.actor.state = ActorMoving(self.actor)
        elif key.space:
            print("jumping")
        elif key.right:
            self.actor.state = ActorMoving(self.actor)

class ActorMoving(State):
    def __init__(self, actor):
        self.name = "moving"
        self.image = "dizzy"
        self.actor = actor
        self.actor.set_image(self.image, dimension=(25, 25))

    def update(self, key):
        if key.left:
            self.actor.x -= 1
        elif key.right:
            self.actor.x += 1
        else:
            self.actor.state = ActorStanding(self.actor)

class ActorJumping(State):
    def __init__(self, actor):
        self.name = "jumping"
        self.image = "dizzy"
        self.actor = actor
        self.actor.set_image(self.image, dimension=(25, 25))

    def update(self, key):
        if key.left:
            self.actor.x -= 1
        elif key.right:
            self.actor.x += 1
        else:
            self.actor.state = ActorStanding(self.actor)
