
class GameState:

    # Initialise the Game state class. Each sub-type must call this method. Takes one parameter, which
    # is the game instance.

    def __init__(self, game_fsm_manager, nxtstate=None):
        self.game = game_fsm_manager
        self.nextstate = nxtstate
        self.name = "GameState"

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

    def __str__(self):
        return self.name


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

