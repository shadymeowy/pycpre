from .special import cembed, cbuild, cdeps


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


class Namespace(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    def __hash__(self):
        return hash(self.proxy)

    def __cembed__(self):
        return cembed(self.proxy)

    def __cbuild__(self):
        return cbuild(self.proxy)

    def __cdeps__(self):
        return cdeps(self.proxy)


def generic(fun):
    return Generic(fun)


def generic_space(fun):
    def r(*args, **kargs):
        S = Namespace()
        S.proxy = fun(S, *args, **kargs)
        return S
    return Generic(r)
