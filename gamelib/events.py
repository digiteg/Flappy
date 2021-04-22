

class EventsException(Exception):
    pass


class Events:
    def __init__(self, events=None):

        if events is not None:
            try:
                for _ in events:
                    break
            except:
                raise AttributeError("type object {} is not iterable".format(type(events)))
            else:
                self.__events__ = events

    # firts time get non existing attr
    def __getattr__(self, name):
        print(name)
        if name.startswith('__'):
            raise AttributeError("type object '{}' has no attribute '{}'".format(self.__class__.__name__, name))

        # restrict to only declared events
        if hasattr(self, '__events__'):
            if name not in self.__events__:
                raise EventsException("Event '{}' is not declared".format(name))

        elif hasattr(self.__class__, '__events__'):
            if name not in self.__class__.__events__:
                raise EventsException("Event '{}' is not declared".format(name))

        # create attribute
        self.__dict__[name] = ev = EventSlot(name)
        return ev

    # format string
    def __repr__(self):
        return "<{}.{} object at {}>".format(self.__class__.__module__, self.__class__.__name__,hex(id(self)))

    __str__ = __repr__

    def __len__(self):
        return len(self.__dict__.items())

    def __iter__(self):
        def gen(dictitems=self.__dict__.items()):
            for attr, val in dictitems:
                if isinstance(val, EventSlot):
                    yield val
        return gen()


class EventSlot:
    def __init__(self, name):
        self.targets = []
        self.__name__ = name

    def __repr__(self):
        return "event '{}'".format(self.__name__)

    def __call__(self, *a, **kw):
        for f in tuple(self.targets):
            f(*a, **kw)

    def __iadd__(self, f):
        self.targets.append(f)
        return self

    def __isub__(self, f):
        while f in self.targets:
            self.targets.remove(f)
        return self

    def __len__(self):
        return len(self.targets)

    def __iter__(self):
        def gen():
            for target in self.targets:
                yield target
        return gen()

    def __getitem__(self, key):
        return self.targets[key]
 