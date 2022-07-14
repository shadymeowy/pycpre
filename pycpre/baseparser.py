class BaseParser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.ll = len(self.tokens)

    def peek(self):
        if self.i < self.ll:
            return self.tokens[self.i]
        else:
            return None

    def inc(self):
        self.i += 1

    def read(self):
        r = self.peek()
        self.inc()
        return r

    def last(self):
        return self.tokens[self.i - 1]

    def peekm(self, value):
        return self.peek() == value

    def peekim(self, value):
        r = self.peekm(value)
        if r:
            self.inc()
        return r

    def readm(self, value):
        return self.read() == value

    def peekrm(self, value):
        if not self.peekm(value):
            raise Exception()

    def peekirm(self, value):
        if not self.peekim(value):
            raise Exception()

    def readrm(self, value):
        if not self.readm(value):
            raise Exception()

    def peeknm(self, value):
        return not self.peekm(value)

    def peekinm(self, value):
        return not self.peekim(value)

    def readnm(self, value):
        return not self.readm(value)

    def peekrnm(self, value):
        if not self.peeknm(value):
            raise Exception()

    def peekrnm(self, value):
        if not self.peekinm(value):
            raise Exception()

    def readrnm(self, value):
        if not self.readnm(value):
            raise Exception()

    def readwhile(self, value):
        r = []
        while self.peekm(value):
            r.append(self.read())
        return r

    def readnwhile(self, value):
        r = []
        while self.peeknm(value):
            r.append(self.read())
        return r

    def readwhilef(self, f):
        r = []
        while f(self.peek()):
            r.append(self.read())
        return r

    def readrawparans(self, parans, include=False):
        r = []
        self.readrm(parans[0])
        if include:
            r.append(self.last())
        s = 1
        while True:
            if self.peekm(parans[0]):
                s += 1
            elif self.peekm(parans[1]):
                s -= 1
            elif self.peekm(None):
                raise Exception()
            if s == 0:
                self.inc()
                if include:
                    r.append(self.last())
                return r
            elif s < 0:
                raise Exception()
            else:
                r.append(self.read())

    def _parse(self):
        raise NotImplementedError()

    @classmethod
    def parse(cls, tokens, *args, **kwargs):
        return cls(tokens)._parse(*args, **kwargs)
