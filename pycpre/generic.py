from .special import cembed, cbuild, cdeps


class Generic():
    def __init__(self, fun):
        self.fun = fun
        self.cache = {}

    def instantiate(self, *args):
        if args not in self.cache:
            self.cache[args] = self.fun(*args)
        return self.cache[args]

    def __getitem__(self, args):
        if isinstance(args, tuple):
            return self.instantiate(*args)
        else:
            return self.instantiate(args)

    def __cembed__(self):
        return cembed(self.instantiate())

    def __cbuild__(self):
        return cbuild(self.instantiate())

    def __cdeps__(self):
        return cdeps(self.instantiate())

    def __getattr__ (self, key):
        return getattr(self.instantiate(), key)


class GenericCallable(Generic):
    def __call__(self, *args):
        return self.instantiate(*args)


def generic(fun):
    return Generic(fun)

def generic_callable(fun):
    return GenericCallable(fun)