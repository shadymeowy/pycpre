class Generic():
    def __init__(self, fun):
        self.fun = fun
        self.cache = {}

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.fun(*args)
        return self.cache[args]

    def __getitem__(self, args):
        if isinstance(args, tuple):
            return self(*args)
        else:
            return self(args)


def generic(fun):
    return Generic(fun)
